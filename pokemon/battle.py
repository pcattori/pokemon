import collections
import pokemon
import pokemon.utils as utils
import random

# http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers
STAGE_MULTIPLIERS = (1, 1.5, 2, 2.5, 3, 3.5, 4, .25, .28, .33, .4, .5, .66)

BattleStats = collections.namedtuple('BattleStats', [
    'attack', 'defense', 'special', 'speed', 'accuracy', 'evasion'])

class StatStages:
    def __init__(
            self, attack=0, defense=0, special=0, speed=0, accuracy=0, evasion=0):
        self.attack = attack
        self.defense = defense
        self.special = special
        self.speed = speed
        self.accuracy = accuracy
        self.evasion = evasion

MoveChoice = collections.namedtuple('MoveChoice', ['fighter', 'move', 'target'])

class DeterministicMoveChoice(utils.FallbackWrapper):
    def __init__(self, move_choice, miss):
        super().__init__(move_choice)
        self.miss = miss

MoveResult = collections.namedtuple('MoveResult', ['move_choice', 'miss', 'ko', 'damage'])

class BattlePokemon(utils.FallbackWrapper):
    def __init__(self, pokemon, stat_stages=None):
        super().__init__(pokemon)
        self.stat_stages = stat_stages or StatStages()

    @property
    def battle_stats(self):
        '''http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers'''
        stats = self.stats._asdict()
        battle_stats = {
            stat: stats.get(stat, 1) * STAGE_MULTIPLIERS[stage]
            for stat, stage in self.stat_stages.__dict__.items()}
        return BattleStats(**battle_stats)

class Team(collections.Sequence):
    def __init__(self, members):
        self.members = tuple(members)
        self.fighter_index = 0
        self.fighter = BattlePokemon(self.members[self.fighter_index])

    @property
    def reserves(self):
        for i, member in enumerate(self.members):
            if i != self.fighter_index and member.hp > 0:
                yield i, member

    def blacked_out(self):
        return all([member.hp <= 0 for member in self.members])

    def switch(self, member_index):
        member = self.members[member_index]
        if member_index == self.fighter_index:
            raise ValueError(f'{member.name} is already in battle!')
        if member.hp < 0:
            raise ValueError(f'{member.name} is fainted!')
        self.fighter_index = member_index
        self.fighter = BattlePokemon(self.members[self.fighter_index])

    def __getitem__(self, index):
        return self.members[index]

    def __len__(self):
        return len(self.members)

def fight(move_choices):
    # priority check
    prioritized_move_choices = sorted(
        move_choices,
        key=lambda move_choice: move_choice.fighter.battle_stats.speed,
        reverse=True)

    for move_choice in prioritized_move_choices:
        fighter, move_name, target = move_choice[:3]
        move = fighter.moves[move_name]

        # power point check
        if move.pp <= 0:
            raise ValueError(f'{move.move.name} is out of PP!')
        move.pp -= 1

        # accuracy check
        miss = (
            move.accuracy is not None and
            move.accuracy * fighter.battle_stats.accuracy < random.random())
        if isinstance(move_choice, DeterministicMoveChoice):
            miss = move_choice.miss
        if miss:
            yield MoveResult(move_choice, miss=True, ko=False, damage=None)

        # deal damage
        dmg = pokemon.formulas.damage(fighter, move, target)
        target.hp -= min(dmg.damage, target.hp)

        # send result
        if target.hp == 0:
            yield MoveResult(move_choice, miss=False, ko=True, damage=dmg)
            # do not let KO'd opponent hit back -> return
            return
        yield MoveResult(move_choice, miss=False, ko=False, damage=dmg)
