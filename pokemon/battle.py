import collections
import pokemon
import random

# http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers
STAGE_MULTIPLIERS = (1, 1.5, 2, 2.5, 3, 3.5, 4, .25, .28, .33, .4, .5, .66)

# TODO consolidate BattleStats and StatStages?

BattleStats = collections.namedtuple('BattleStats', [
    'attack', 'defense', 'special', 'speed', 'accuracy', 'evasion'])

class StatStages:
    def __init__(
            self, attack=0, defense=0, special=0,
            speed=0, accuracy=0, evasion=0):
        self.attack = attack
        self.defense = defense
        self.special = special
        self.speed = speed
        self.accuracy = accuracy
        self.evasion = evasion

class BattlePokemon(pokemon.Pokemon):
    def __init__(self, pokemon, stat_stages=None):
        self.pokemon = pokemon
        self.stat_stages = stat_stages or StatStages()

    @property
    def battle_stats(self):
        stats = self.stats._asdict()
        battle_stats = {
            stat: stats.get(stat, 1) * STAGE_MULTIPLIERS[stage]
            for stat, stage in self.stat_stages.__dict__.items()}
        return BattleStats(**base_stats)

    def __getattr__(self, attr):
        return getattr(self.pokemon, attr)

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

FightAction = collections.namedtuple('FightAction', ['pokemon', 'move', 'target'])
FightActionResult = collections.namedtuple('FightActionResult', [
    'action', 'miss', 'ko', 'damage'])

def fight(fight_actions):
    prioritized_fight_actions = sorted(
        fight_actions,
        key=lambda fight_action: fight_action.pokemon.stats.speed,
        reverse=True)
    for fight_action in prioritized_fight_actions:
        move = fight_action.pokemon.moves[fight_action.move]
        if move.pp <= 0:
            raise ValueError(f'{move.move.name} is out of PP!')
        move.pp -= 1
        miss = move.accuracy is not None and move.accuracy < random.random()
        if miss:
            yield FightActionResult(
                fight_action, miss=True, ko=False, damage=None)
        dmg = pokemon.formulas.damage(
            fight_action.pokemon, move, fight_action.target)
        opponent = fight_action.target
        opponent.pokemon.hp -= dmg.damage
        opponent.pokemon.hp = max(opponent.hp, 0)
        yield FightActionResult(
            fight_action, miss=False, ko=opponent.hp == 0, damage=dmg)
