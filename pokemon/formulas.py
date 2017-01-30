import collections
import math
import pokemon.core as core
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
    ivs = core.Stats(**ivs)
    return ivs

def hp_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:HP_calc.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + level + 10

def stat_calc(base, iv, ev, level):
    '''http://bulbapedia.bulbagarden.net/wiki/File:Statcalc_gen12.png'''
    base_iv_level = (base + iv) * 2 + math.floor(math.sqrt(ev) / 4)
    return math.floor(base_iv_level * level / 100) + 5

# TODO should not depend on battle
def damage(fighter, move, target, critical_hit=None, luck=None):
    '''http://bulbapedia.bulbagarden.net/wiki/Damage#Damage_formula'''
    import pokemon.battle.fighter as battlefighter
    if not isinstance(fighter, battlefighter.Fighter):
        fighter = battlefighter.Fighter(fighter)

    if not isinstance(target, battlefighter.Fighter):
        target = battlefighter.Fighter(target)

    # Same Type Attack Bonus (STAB)
    stab = 1
    if move.type_ in fighter.species.types:
        stab = 1.5

    effectiveness = 1
    if move.type_: # ignore effectiveness for type-less attacks
        for type_ in target.species.types:
            effectiveness *= data.TYPE_CHART[move.type_][type_]

    # http://bulbapedia.bulbagarden.net/wiki/Critical_hit#In_Generation_I
    if critical_hit is None:
        high_ratio_factor = 1
        if move.high_critical_hit_ratio:
            high_ratio_factor = 64
        critical_hit = (
            fighter.species.base_stats.speed * high_ratio_factor / 512 > random.random())
    critical = 2 if critical_hit else 1

    if luck is None:
        luck = random.uniform(0.85, 1)

    # modifier without `other` for 1st generation
    modifier = stab * effectiveness * critical * luck

    # level
    level = fighter.level

    # attack and defense
    if move.category == 'physical':
        attack = fighter.stats.attack * fighter.stage_multipliers.attack
        defense = target.stats.defense * target.stage_multipliers.defense
    elif move.category == 'special':
        attack = fighter.stats.special * fighter.stage_multipliers.special
        defense = target.stats.special * target.stage_multipliers.special
    else:
        raise ValueError(f"Move category '{move.category}' cannot deal direct damage")

    # base power
    base = move.power

    dmg = math.floor(
        (((2 * level + 10) / 250) * (attack / defense) * base + 2) * modifier)
    return DamageResult(
        damage=dmg, luck=luck, critical_hit=critical_hit,
        effectiveness=effectiveness)

def accuracy_check(fighter, move, target):
    '''http://bulbapedia.bulbagarden.net/wiki/Statistic#Formula_for_accuracy_and_evasion'''
    return (
        move.accuracy * fighter.stage_multipliers.accuracy /
        target.stage_multipliers.evasion) > random.random()

# http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers
STAGE_MULTIPLIERS = (1, 1.5, 2, 2.5, 3, 3.5, 4, .25, .28, .33, .4, .5, .66)

