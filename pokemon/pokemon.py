import math
import pokemon.core as pokemon
import pokemon.pokedex as pokedex
import random

def hp_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:HP_calc.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + level + 10

def stat_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:Statcalc_gen12.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + 5

def hp_iv(other_ivs):
    '''http://bulbapedia.bulbagarden.net/wiki/Individual_values#Generation_I_and_II'''
    stats = ('attack', 'defense', 'speed', 'special')
    hp_bits = (other_ivs[stat] & 1 for stat in stats)
    hp = 0
    for bit in hp_bits:
        hp = (hp << 1) | bit
    return hp

class Pokemon:
    def __init__(self, species, level, moves, ivs=None, evs=None):
        self.species = species
        self.level = level

        if ivs is None:
            stats = ('attack', 'defense', 'speed', 'special')
            ivs = {stat: random.randint(0, 15) for stat in stats}
            ivs['hp'] = hp_iv(ivs)
            ivs = pokemon.Stats(**ivs)
        self.ivs = ivs

        if evs is None:
            evs = pokemon.Stats(0, 0, 0, 0, 0)
        self.evs = evs

        self._stats = None
        self.hp = self.stats.hp # start at full hp
        self.moves = moves
        # TODO status condition

    @staticmethod
    def of_species(species_name, **kwargs):
        species = pokedex.POKEDEX.by_name(species_name)
        return Pokemon(species, **kwargs)

    @property
    def stats(self):
        if self._stats is None:
            values = zip(self.species.base_stats, self.ivs, self.evs)
            hp = hp_calc(*(next(values) + (self.level,)))
            others = tuple(
                stat_calc(base, iv, ev, self.level)
                for base, iv, ev in values)
            self._stats = pokemon.Stats(hp, *others)
        return self._stats
