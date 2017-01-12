import collections

Stats = collections.namedtuple('Stats', [
    'hp', 'attack', 'defense', 'special', 'speed'])

Species = collections.namedtuple('Species', [
    'national_pokedex_number', 'name', 'types', 'base_stats'])

Move = collections.namedtuple('Move', [
    'name', 'type_', 'category', 'power', 'accuracy', 'max_pp'])

TypeEffectiveness = collections.namedtuple('TypeEffectiveness', [
    'attack', 'defend', 'effectiveness'])
