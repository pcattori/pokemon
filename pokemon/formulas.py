import collections
import json
import math
import pkg_resources
import pokemon.core as pokemon
import random

Damage = collections.namedtuple('Damage', [
    'damage', 'luck', 'critical_hit', 'effectiveness'])

def _load_type_effectivenesses():
    type_effectiveness_json = pkg_resources.resource_filename(
        'pokemon', 'data/type_effectiveness.json')
    with open(type_effectiveness_json) as f:
        for line in f:
            type_effectiveness = json.loads(line)
            yield pokemon.TypeEffectiveness(**type_effectiveness)

TYPE_EFFECTIVENESSES = _load_type_effectivenesses()
effectiveness = {
    (te.attack, te.defend): te.effectiveness
    for te in TYPE_EFFECTIVENESSES
}

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

def damage(pokemon, move, opponent):
    '''http://bulbapedia.bulbagarden.net/wiki/Damage#Damage_formula'''
    # TODO allow for critical, luck injection?

    # Same Type Attack Bonus (STAB)
    stab = 1
    if move.type_ in pokemon.species.types:
        stab = 1.5

    type_effectiveness = 1
    for type_ in opponent.species.types:
        type_effectiveness *= effectiveness[(move.type_, type_)]

    # http://bulbapedia.bulbagarden.net/wiki/Critical_hit#In_Generation_I
    # TODO http://bulbapedia.bulbagarden.net/wiki/Category:Moves_with_a_high_critical-hit_ratio
    critical = 1
    if random.random() < pokemon.species.base_stats.speed / 512:
        critical = 2

    # modifier without `other` for 1st generation
    luck = random.uniform(0.85, 1)
    modifier = stab * type_effectiveness * critical * luck

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
        return None

    # base power
    base = move.power

    dmg = math.floor((((2 * level + 10) / 250) * (attack / defense) * base + 2) * modifier)
    # TODO effectiveness and critical messages
    return Damage(
        damage=dmg, luck=luck, critical_hit=critical == 2,
        effectiveness=type_effectiveness)
