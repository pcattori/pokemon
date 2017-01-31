import collections
import maps
import math
import numpy as np
import pokemon.data as data
import pokemon.formulas as formulas
import pokemon.battle.log as battlelog
import pokemon.battle.team as battleteam
import random

Switch = collections.namedtuple('Switch', ['team_index', 'new_fighter_index'])
MoveChoice = collections.namedtuple('MoveChoice', ['fighter', 'move_name'])
# with defaults, MoveChoice can absorb DeterministicMoveChoice:
# MoveChoice = maps.namedfrozen('MoveChoice', [
#     'fighter', 'move', ('miss', None)])

# determinism via NamedDict
# Determinism = collections.namedfrozen('Determinism', [
#     'hurt_in_confusion', 'paralyzed', 'missed', 'effected', 'critical_hit', 'luck'])

def stat_stage_change(who, stat, stages):
    '''Compute net stage change for specified stat'''
    original_stat_stage = who.stat_stages[stat]
    if stages > 0:
        return min(original_stat_stage + stages, 6) - original_stat_stage
    elif stages < 0:
        return max(original_stat_stage + stages, -6) - original_stat_stage

class Battle:
    # TODO handle fainting

    _CONFUSED = data.Move(
        name=None, category='physical', type_=None, power=40, accuracy=None,
        max_pp=None, priority=None, effect=None, high_critical_hit_ratio=None)

    def __init__(self, teams):
        self.teams = tuple(battleteam.BattleTeam(team) for team in teams)
        for index, team in enumerate(self.teams):
            team.index = index

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
            if move_choice.fighter.status_condition == 'paralysis':
                speed *= 0.25
            return speed

        return sorted(move_choices, key=move_speed, reverse=True)

    def next_turn(self, turn_actions, determinism={}):
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
        yield from Battle._fight_phase(self.teams, move_choices)

    @staticmethod
    def _fight_phase(teams, move_choices):
        already_effected = set() # only apply status condition effects once per team per turn
        for action in Battle._prioritize_moves(move_choices):
            fighter, move_name = action
            move = fighter.moves[move_name]
            opponent = teams[(fighter.team.index + 1) % 2].fighter

            # pre-attack effects
            pre_attack_log = list(Battle._pre_attack(fighter, determinism))
            yield from pre_attack_log

            # check if pre-attack effects prevent pokemon from attacking
            unable_to_attack = any(
                action_result for action_result in pre_attack_log
                if isinstance(action_result, battlelog.UnableToAttack))
            if unable_to_attack:
                continue

            # execute move
            attack_log = Battle._attack(fighter, move, opponent, determinism)
            yield from attack_log
            miss = any(
                action for action in attack_log
                if isinstance(action, battlelog.MoveMiss))
            # TODO handle multi-turn effects via battle queue

            # post-attack effects
            post_attack_log = list(
                Battle._post_attack(fighter, move, opponent, miss))
            yield from post_attack_log

            # register post-attack status condition damage so pokemon are not hurt 2x
            already_effected.update(
                action_result for action_result in post_attack_log
                if isinstance(action_result, battlelog.StatusConditionDamage))

        # post-turn effects
        yield from Battle._post_turn(teams, already_effected)

    @staticmethod
    def _attack(fighter, move, opponent, determinism):
        # power point check
        if move.pp <= 0:
            raise ValueError(f'{move.name} is out of PP!')
        move.pp -= 1
        yield battlelog.PowerPointDecrement(fighter.team.index, move.name)

        # accuracy check
        missed = determinism.get('missed', all([
            move.accuracy is not None,
            not formulas.accuracy_check(fighter, move, opponent)])
        if missed:
            yield battlelog.MoveMiss(fighter.team.index, move.name)

        # deal damage
        if move.category in {'physical', 'special'}:
            dmg = formulas.damage(fighter, move, opponent)
            opponent.hp -= min(dmg.damage, opponent.hp)
            yield battlelog.MoveHit(
                fighter.team.index, move.name, opponent.team.index, dmg)

        # effect check
        if move.effect:
            effected = determinism.get('effected' , move.effect.chance > random.random())
            if effected:
                who = fighter if move.effect.who == 'user' else opponent
                yield from Battle._apply_effect(who, move.effect)

    @staticmethod
    def _apply_effect(who, effect):
        if effect.stat and effect.stages:
            delta = stat_stage_change(who, effect.stat, effect.stages)
            who.stat_stages[effect.stat] += delta
            yield battlelog.StatStageChange(
                who.team.index, effect.stat, delta, who.stat_stages[effect.stat])

        elif effect.status_condition:
            non_volatile_status_conditions = {
                'burn', 'freeze', 'paralysis', 'poison', 'sleep'}
            if effect.status_condition in non_volatile_status_conditions:
                yield from Battle._apply_status_condition(
                    who, effect.status_condition)
            else:
                yield from Battle._apply_volitile_status_condition(
                    who, effect.status_condition)

        else:
            raise ValueError((
                "Effect must have either ('stat', 'stages')"
                f" or ('status_condition'): {effect}"))

    @staticmethod
    def _pre_attack_non_volitile_status_conditions(fighter, determinism):
        if fighter.status_condition == 'freeze':
            yield battlelog.UnableToAttack(fighter.team.index, status_condition)
        elif fighter.status_condition == 'paralysis':
            paralyzed = determinism.get('paralysis', random.random() < 0.5)
            if paralyzed:
                yield battlelog.UnableToAttack(fighter.team.index, status_condition)
        elif fighter.status_condition == 'sleep':
            yield battlelog.UnableToAttack(fighter.team.index, status_condition)

    @staticmethod
    def _pre_attack_volitile_status_conditions(fighter, determinism):
        if 'flinch' in fighter.volitile_status_conditions:
            yield battlelog.UnableToAttack(fighter.team.index, flinch.name)

        elif 'bound' in fighter.volitile_status_conditions:
            yield battlelog.UnableToAttack(fighter.team.index, bound.name)

        elif 'confusion' in fighter.volitile_status_conditions:
            hurt_in_confusion = determinism.get(
                'hurt_in_confusion', random.random() < 0.25)
            if hurt_in_confusion:
                dmg = formulas.damage(
                    fighter, Battle._CONFUSED, fighter, critical_hit=False)
                fighter.hp -= min(dmg.damage, fighter.hp)
                yield battlelog.StatusConditionDamage(
                    fighter.team.index, 'confusion', dmg.damage)
                yield battlelog.UnableToAttack(fighter.team.index, 'confusion')

    @staticmethod
    def _pre_attack(fighter, determinism):
        # non-volatile status conditions
        yield from Battle._pre_attack_non_volitile_status_conditions(fighter, determinism)

        # volatile status conditions
        yield from Battle._pre_attack_volitile_status_conditions(fighter, determinism)

        # decrement status condition timers
        for name, turns in list(fighter.status_condition_timers.items()):
            turns -= 1
            fighter.status_condition_timers[name] = turns
            if turns == 0:
                if name == 'sleep':
                    fighter.status_condition = None
                else:
                    fighter.volitile_status_conditions.remove(name)
                del fighter.status_condition_timers[name]
                yield battlelog.RemoveStatusCondition(fighter.team.index, name)

    @staticmethod
    def _post_attack(fighter, move, opponent, miss):
        # http://bulbapedia.bulbagarden.net/wiki/Freeze_(status_condition)#Generation_I
        if not miss:
            if opponent.status_condition == 'freeze' and move.type == 'fire':
                opponent.status_condition = None # thaw
                yield battlelog.RemoveStatusCondition(opponent.team.index, 'freeze')

        # http://bulbapedia.bulbagarden.net/wiki/Burn_(status_condition)#Generation_I
        if fighter.status_condition == 'burn':
            burn_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
            fighter.hp -= burn_damage
            yield battlelog.StatusConditionDamage(
                fighter.team.index, fighter.status_condition, burn_damage)

        # http://bulbapedia.bulbagarden.net/wiki/Poison_(status_condition)#Generation_I
        elif fighter.status_condition == 'poison':
            poison_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
            fighter.hp -= poison_damage
            yield battlelog.StatusConditionDamage(
                fighter.team.index, fighter.status_condition, poison_damage)

    @staticmethod
    def _post_turn(teams, already_effected):
        already_effected_teams = frozenset(ae.team_index for ae in already_effected)
        for team_index, team in enumerate(teams):
            fighter = team.fighter
            opponent = teams[(team_index + 1) % 2].fighter
            if team_index not in already_effected_teams:

                if fighter.status_condition == 'burn':
                    burn_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                    fighter.hp -= burn_damage
                    yield battlelog.StatusConditionDamage(
                        fighter.team.index, status_condition, burn_damage)

                elif fighter.status_condition == 'poison':
                    poison_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                    fighter.hp -= poison_damage
                    yield battlelog.StatusConditionDamage(
                        fighter.team.index, status_condition, poison_damage)

            if 'leech seed' in fighter.volitile_status_conditions:
                leech_seed_damage = min(math.ceil(fighter.stats.hp / 16), fighter.hp)
                fighter.hp -= leech_seed_damage
                yield battlelog.StatusConditionDamage(
                    fighter.team.index, 'leech seed', leech_seed_damage)

                leech_seed_health = min(leech_seed_damage, opponent.stats.hp - opponent.hp)
                opponent.hp += leech_seed_health
                yield battlelog.StatusConditionRecover(
                    opponent.team.index, 'leech seed', leech_seed_health)

    @staticmethod
    def _apply_status_condition(who, status_condition):
        if who.status_condition is not None:
            return
        elif status_condition == 'burn' and 'fire' in who.species.types:
            return
        elif status_condition == 'freeze' and 'ice' in who.species.types:
            return

        who.status_condition = status_condition
        if status_condition == 'sleep':
            who.status_condition_timers[status_condition] = formulas.sleep_turns()
        turns = who.status_condition_timers.get(status_condition, None)
        yield battlelog.AddStatusCondition(who.team.index, status_condition, turns)

    @staticmethod
    def _apply_volitile_status_condition(who, status_condition):
        if status_condition in who.volitile_status_conditions:
            return

        who.volitile_status_conditions.add(status_condition)
        turns = formulas.volitile_status_condition_turns(status_condition)
        if turns:
            who.status_condition_timers[status_condition] = turns
        yield battlelog.AddStatusCondition(who.team.index, status_condition, turns)

