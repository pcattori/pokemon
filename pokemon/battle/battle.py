import collections
import maps
import math
import numpy as np
import pokemon.core as core
import pokemon.data as data
import pokemon.formulas as formulas
import pokemon.battle.team as battleteam
import random

Switch = collections.namedtuple('Switch', ['team_index', 'new_fighter_index'])
MoveChoice = collections.namedtuple('MoveChoice', ['fighter', 'move_name'])
# with defaults, MoveChoice can absorb DeterministicMoveChoice:
# MoveChoice = maps.namedfrozen('MoveChoice', [
#     'fighter', 'move', ('miss', None)])

# Action Log
UnableToAttack = collections.namedtuple('UnableToAttack', [
    'team_index', 'reason'])
PowerPointDecrement = collections.namedtuple('PowerPointDecrement', [
    'team_index', 'move_name'])
MoveMiss = collections.namedtuple('MoveMiss', ['team_index', 'move_name'])
MoveHit = collections.namedtuple('MoveHit', [
    'team_index', 'move_name', 'opponent_team_index', 'damage_result'])
StatStageChange = collections.namedtuple('StatStageChange', [
    'team_index', 'stat', 'stage_delta', 'new_stage'])
AddStatusCondition = collections.namedtuple('AddStatusCondition', [
    'team_index', 'status_condition'])
RemoveStatusCondition = collections.namedtuple('RemoveStatusCondition', [
    'team_index', 'status_condition'])
StatusConditionDamage = collections.namedtuple('StatusConditionDamage', [
    'team_index', 'status_condition', 'damage'])
StatusConditionRecover = collections.namedtuple('StatusConditionRecover', [
    'team_index', 'status_condition', 'hp_recovered'])
Fainted = collections.namedtuple('Fainted', ['team_index'])

def stat_stage_change(who, stat, stages):
    '''Compute net stage change for specified stat'''
    original_stat_stage = who.stat_stages[stat]
    if stages > 0:
        return min(original_stat_stage + stages, 6) - original_stat_stage
    elif stages < 0:
        return max(original_stat_stage + stages, -6) - original_stat_stage

def status_condition_change(who, status_condition_name):
    if who.status_condition.name is not None:
        return None
    elif status_condition_name == 'burn' and 'fire' in who.species.types:
        return None
    elif status_condition_name == 'freeze' and 'ice' in who.species.types:
        return None

    turns = None
    if status_condition_name == 'sleep':
        turns = random.randint(1, 7)
    return core.StatusCondition(status_condition_name, turns)

def volitile_status_condition_change(who, status_condition_name):
    volitile_status_condition_names = frozenset([
        vsc.name for vsc in who.volitile_status_conditions])
    if status_condition_name in volitile_status_condition_names:
        return None

    turns = None
    # http://bulbapedia.bulbagarden.net/wiki/Status_condition#Generation_I
    if status_condition_name == 'bound':
        turns = np.random.choice(range(2, 6), p=[.375, .375, .125, .125])
    elif status_condition_name == 'confusion':
        turns = random.randint(1, 4)
    elif status_condition_name == 'flinch':
        turns = 1
    elif status_condition_name == 'leech seed':
        turns = None
    return core.StatusCondition(status_condition_name, turns)

class Battle:
    # TODO handle fainting

    _CONFUSED = data.Move(
        name=None, category='physical', type_=None, power=40, accuracy=None,
        max_pp=None, priority=None, effect=None, high_critical_hit_ratio=None)

    def __init__(self, teams):
        self.teams = tuple(battleteam.BattleTeam(team) for team in teams)

        # access via actions[team_index][relative_turn_number]
        self.actions = tuple(collections.deque() for team in teams)

    @property
    def ended(self):
        return any(team.blacked_out() for team in self.teams)

    @staticmethod
    def _prioritize_moves(move_choices):
        def move_speed(move_choice):
            speed = move_choice.fighter.stats.speed
            speed *= move_choice.fighter.stage_multipliers.speed
            status_condition = move_choice.fighter.status_condition
            if status_condition and status_condition.name == 'paralysis':
                speed *= 0.25
            return speed

        return sorted(
            enumerate(move_choices),
            key=lambda move_choice: move_speed(move_choice[1]),
            reverse=True)

    def next_turn(self, turn_actions):
        if self.ended:
            raise StopIteration('Battle has already ended')

        # if there is space in queue, add actions
        for team_index, action in enumerate(turn_actions):
            team_actions = self.actions[team_index]
            if len(team_actions) == 0:
                team_actions.append(action)
        # TODO what about interrupts?
        turn_actions = [team_actions.popleft() for team_actions in self.actions]

        # switch phase
        switches = [
            action for action in turn_actions
            if isinstance(action, Switch)]
        for action in switches:
            self.teams[action.team_index].switch(action.new_fighter_index)
            yield action

        # TODO item phase here??

        # fight phase
        move_choices = [
            action for action in turn_actions
            if isinstance(action, MoveChoice)]
        already_effected = set() # only apply status condition effects once per team per turn
        for team_index, action in Battle._prioritize_moves(move_choices):
            fighter, move_name = action
            move = fighter.moves[move_name]
            opponent = self.teams[(team_index + 1) % 2].fighter

            pre_attack_log = list(Battle._pre_attack(team_index, fighter))
            yield from pre_attack_log

            unable_to_attack = any(
                action_result for action_result in pre_attack_log
                if isinstance(action_result, UnableToAttack))
            if unable_to_attack:
                continue

            attack_log = Battle._attack(team_index, fighter, move, opponent)
            yield from attack_log
            miss = any(action for action in attack_log if isinstance(action, MoveMiss))
            # TODO handle multi-turn effects via battle queue

            # post-attack effects
            post_attack_log = list(
                Battle._post_attack(team_index, fighter, move, opponent, miss))
            yield from post_attack_log

            already_effected.update(
                action_result for action_result in post_attack_log
                if isinstance(action_result, StatusConditionDamage))

        # post-turn effects
        yield from Battle._post_turn(self.teams, already_effected)

    @staticmethod
    def _attack(team_index, fighter, move, opponent, missed=None, effected=None):
        opponent_team_index = (team_index + 1) % 2
        # power point check
        if move.pp <= 0:
            raise ValueError(f'{move.name} is out of PP!')
        move.pp -= 1
        yield PowerPointDecrement(team_index, move.name)

        # accuracy check
        if missed is None:
            missed = (
                move.accuracy is not None and
                not formulas.accuracy_check(fighter, move, opponent))
        if missed:
            yield MoveMiss(team_index, move.name)

        # deal damage
        if move.category in {'physical', 'special'}:
            dmg = formulas.damage(fighter, move, opponent)
            opponent.hp -= min(dmg.damage, opponent.hp)
            yield MoveHit(team_index, move.name, opponent_team_index, dmg)

        # effect
        if move.effect and effected is None:
            effected = move.effect.chance > random.random()
        if move.effect and effected:
            if move.effect.who == 'user':
                yield from Battle._apply_effect(
                    team_index, fighter, move.effect)
            else:
                yield from Battle._apply_effect(
                    opponent_team_index, opponent, move.effect)

    @staticmethod
    def _apply_effect(who_team_index, who, effect):
        if effect.stat and effect.stages:
            delta = stat_stage_change(who, effect.stat, effect.stages)
            who.stat_stages[effect.stat] += delta
            yield StatStageChange(
                who_team_index, effect.stat, delta, who.stat_stages[effect.stat])
        elif effect.status_condition:
            non_volatile_status_conditions = {
                'burn', 'freeze', 'paralyze', 'poison', 'sleep'}
            if effect.status_condition in non_volatile_status_conditions:
                new_status = status_condition_change(who, effect.status_condition)
                if new_status:
                    who.status_condition = new_status
                    yield AddStatusCondition(who_team_index, new_status.name)
            else:
                new_status = volitile_status_condition_change(who, status_condition)
                if new_status:
                    who.volitile_status_conditions[new_status.name] = new_status
                    yield AddStatusCondition(who_team_index, new_status.name)

    @staticmethod
    def _pre_attack_non_volitilte_status_conditions(team_index, fighter):
        status_condition_name = fighter.status_condition.name
        if status_condition_name == 'freeze':
            yield UnableToAttack(team_index, status_condition_name)
        elif status_condition_name == 'paralysis':
            if random.random() < 0.5:
                yield UnableToAttack(team_index, status_condition_name)
        elif fighter.status_condition.name == 'sleep':
            yield UnableToAttack(team_index, status_condition_name)

    @staticmethod
    def _pre_attack_volitilte_status_conditions(team_index, fighter):
        flinch = fighter.volitile_status_conditions.get('flinch', None)
        if flinch:
            yield UnableToAttack(team_index, flinch.name)

        bound = fighter.volitile_status_conditions.get('bound', None)
        if bound:
            yield UnableToAttack(team_index, bound.name)

        confusion = fighter.volitile_status_conditions.get('confusion', None)
        if confusion and not unable:
            if random.random() < 0.25:
                dmg = formulas.damage(
                    fighter, Battle._CONFUSED, fighter, critical_hit=False)
                fighter.hp -= min(dmg.damage, fighter.hp)
                yield StatusConditionDamage(team_index, 'confusion', dmg.damage)
                yield UnableToAttack(team_index, 'confusion')

    @staticmethod
    def _pre_attack(team_index, fighter):
        # non-volatile status conditions
        yield from Battle._pre_attack_non_volitilte_status_conditions(team_index, fighter)

        # volatile status conditions
        yield from Battle._pre_attack_volitilte_status_conditions(team_index, fighter)

        # decrement sleep counter!
        if fighter.status_condition.name == 'sleep':
            fighter.status_condition.turns -= 1
            if fighter.status_condition.turns == 0:
                fighter.status_condition = core.StatusCondition(None, None)
                yield RemoveStatusCondition(team_index, 'sleep')

        # decrement vsc counters!
        for name, turns in list(fighter.volitile_status_conditions.items()):
            turns -= 1
            fighter.volitile_status_conditions[name] = turns
            if turns == 0:
                del fighter.volitile_status_conditions[name]
                yield RemoveStatusCondition(team_index, name)

    @staticmethod
    def _post_attack(team_index, fighter, move, opponent, miss):
        opponent_team_index = (team_index + 1) % 2
        # http://bulbapedia.bulbagarden.net/wiki/Freeze_(status_condition)#Generation_I
        if not miss:
            if opponent.status_condition.name == 'freeze' and move.type == 'fire':
                opponent.status_condition = core.StatusCondition(None, None) # thaw
                yield RemoveStatusCondition(opponent_team_index, 'freeze')

        status_condition_name = fighter.status_condition.name
        # http://bulbapedia.bulbagarden.net/wiki/Burn_(status_condition)#Generation_I
        if status_condition_name == 'burn':
            burn_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
            fighter.hp -= burn_damage
            yield StatusConditionDamage(
                team_index, status_condition_name, burn_damage)

        # http://bulbapedia.bulbagarden.net/wiki/Poison_(status_condition)#Generation_I
        elif status_condition_name == 'poison':
            poison_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
            fighter.hp -= poison_damage
            yield StatusConditionDamage(
                team_index, status_condition_name, poison_damage)

    @staticmethod
    def _post_turn(teams, already_effected):
        already_effected_teams = frozenset(ae.team_index for ae in already_effected)
        for team_index, team in enumerate(teams):
            fighter = team.fighter
            opponent_team_index = (team_index + 1) % 2
            opponent = teams[opponent_team_index].fighter
            if team_index not in already_effected_teams:

                status_condition_name = fighter.status_condition.name
                if status_condition_name == 'burn':
                    burn_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                    fighter.hp -= burn_damage
                    yield StatusConditionDamage(
                        team_index, status_condition_name, burn_damage)

                elif status_condition_name == 'poison':
                    poison_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                    fighter.hp -= poison_damage
                    yield StatusConditionDamage(
                        team_index, status_condition_name, poison_damage)

            if 'leech seed' in fighter.volitile_status_conditions:
                leech_seed_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                fighter.hp -= leech_seed_damage
                yield StatusConditionDamage(
                    team_index, 'leech seed', leech_seed_damage)

                leech_seed_health = min(leech_seed_damage, opponent.stats.hp - opponent.hp)
                opponent.hp += leech_seed_health
                yield StatusConditionRecover(
                    opponent_team_index, 'leech seed', leech_seed_health)
