import collections

Stats = collections.namedtuple('Stats', [
    'hp', 'attack', 'defense', 'special', 'speed'])

Species = collections.namedtuple('Species', [
    'national_pokedex_number', 'name', 'types', 'base_stats'])

Move = collections.namedtuple('Move', [
    'name', 'type_', 'category', 'power', 'accuracy', 'max_pp', 'priority',
    'effect', 'high_critical_hit_ratio'])

def move(priority=0, effect=None, high_critical_hit_ratio=False, **kwargs):
    return Move(priority=priority, effect=effect,
        high_critical_hit_ratio=high_critical_hit_ratio, **kwargs)

MoveEffect = collections.namedtuple('MoveEffect', [
    'chance', 'status_condition', 'stat', 'stages'])

def move_effect(chance=1.0, status_condition=None, stat=None, stages=None, **kwargs):
    return MoveEffect(
        chance=chance, status_condition=status_condition, stat=stat,
        stages=stages, **kwargs)

TypeEffectiveness = collections.namedtuple('TypeEffectiveness', [
    'attack', 'defend', 'effectiveness'])
