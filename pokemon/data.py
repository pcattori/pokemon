import collections
import json
import maps
import pkg_resources
import pokemon.core as core
import pokemon.pokedex as pokedex
import pokemon.utils as utils

Species = collections.namedtuple('Species', [
    'national_pokedex_number', 'name', 'types', 'base_stats'])

TypeEffectiveness = collections.namedtuple('TypeEffectiveness', [
    'attack', 'defend', 'effectiveness'])

Move = maps.namedfrozen('Move', [
    'name', 'type_', 'category', 'power', 'accuracy', 'max_pp', 'priority',
    'effect', 'high_critical_hit_ratio'])

MoveEffect = collections.namedtuple('MoveEffect', [
    'who', 'chance', 'status_condition', 'stat', 'stages'])

def move_effect(chance=1.0, status_condition=None, stat=None, stages=None, **kwargs):
    return MoveEffect(
        chance=chance, status_condition=status_condition, stat=stat,
        stages=stages, **kwargs)

# type chart
############

def stream_type_effectivenesses():
    type_effectiveness_json = pkg_resources.resource_filename(
        'pokemon', 'data/type_effectiveness.json')
    with open(type_effectiveness_json) as f:
        for line in f:
            type_effectiveness = json.loads(line)
            yield TypeEffectiveness(**type_effectiveness)

def load_type_chart():
    type_chart = collections.defaultdict(dict)
    for entry in stream_type_effectivenesses():
        type_chart[entry.attack][entry.defend] = entry.effectiveness
    return type_chart

TYPE_CHART = load_type_chart()

# pokedex
#########

def stream_species():
    species_json = pkg_resources.resource_filename('pokemon', 'data/species.json')
    with open(species_json) as f:
        for line in f:
            species = json.loads(line)
            species['base_stats'] = core.Stats(**species.pop('baseStats'))
            yield Species(**species)

POKEDEX = pokedex.Pokedex(stream_species())

# movedex
#########

def move_from_json(move_json):
    move = json.loads(move_json)
    if 'effects' in move:
        del move['effects']
    if 'changes' in move:
        del move['changes']
    # rename
    move['type_'] = move.pop('type')
    move['max_pp'] = move.pop('pp')
    move['high_critical_hit_ratio'] = move.pop('highCriticalHitRatio', False)
    effect = move.pop('effect', None)
    if effect:
        effect['status_condition'] = effect.pop('statusCondition', None)
        effect['who'] = effect.pop('who', None)
        move['effect'] = move_effect(**effect)
    else:
        move['effect'] = None
    move['priority'] = move.pop('priority', 0)
    return Move(**move)

def stream_moves():
    moves_json = pkg_resources.resource_filename('pokemon', 'data/moves.json')
    with open(moves_json) as f:
        for line in f:
            move = move_from_json(line)
            if move:
                yield move

MOVEDEX = pokedex.Movedex(stream_moves())

def find_species(species_name):
    return POKEDEX.by_name(species_name)

def find_move(move_name):
    return MOVEDEX.by_name(move_name)

