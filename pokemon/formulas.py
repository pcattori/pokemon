import collections
import math
import pokemon.core as pokemon
import pokemon.data as data
import random

DamageResult = collections.namedtuple('DamageResult', [
    'damage', 'luck', 'critical_hit', 'effectiveness'])

def random_ivs():
    '''http://bulbapedia.bulbagarden.net/wiki/Individual_values#Generation_I_and_II'''
    stats = ('attack', 'defense', 'speed', 'special')
    ivs = {stat: random.randint(0, 15) for stat in stats}
    ivs['hp'] = sum(
        (ivs[stat] & 1) << i
        for i, stat in enumerate(reversed(stats)))
    ivs = pokemon.Stats(**ivs)
    return ivs

def hp_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:HP_calc.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + level + 10

def stat_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:Statcalc_gen12.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + 5

def damage(pokemon, move, opponent, critical_hit=None, luck=None):
    '''http://bulbapedia.bulbagarden.net/wiki/Damage#Damage_formula'''

    # Same Type Attack Bonus (STAB)
    stab = 1
    if move.type_ in pokemon.species.types:
        stab = 1.5

    effectiveness = 1
    for type_ in opponent.species.types:
        effectiveness *= data.TYPE_CHART[move.type_][type_]

    # http://bulbapedia.bulbagarden.net/wiki/Critical_hit#In_Generation_I
    # TODO http://bulbapedia.bulbagarden.net/wiki/Category:Moves_with_a_high_critical-hit_ratio
    if critical_hit is None:
        critical_hit = random.random() < pokemon.species.base_stats.speed / 512
    critical = 2 if critical_hit else 1

    if luck is None:
        luck = random.uniform(0.85, 1)

    # modifier without `other` for 1st generation
    modifier = stab * effectiveness * critical * luck

    # level
    level = pokemon.level

    # attack and defense
    if move.category == 'physical':
        attack = pokemon.stats.attack
        defense = opponent.stats.defense
    elif move.category == 'special':
        attack = pokemon.stats.special
        defense = opponent.stats.special
    else:
        raise ValueError(f"Move category '{move.category}' cannot deal direct damage")

    # base power
    base = move.power

    dmg = math.floor((((2 * level + 10) / 250) * (attack / defense) * base + 2) * modifier)
    return DamageResult(
        damage=dmg, luck=luck, critical_hit=critical_hit,
        effectiveness=effectiveness)
