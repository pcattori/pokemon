import collections
import json
import pkg_resources
import pokemon.core as pokemon
import pokemon.pokedex as pokedex

# type chart
############

def stream_type_effectivenesses():
    type_effectiveness_json = pkg_resources.resource_filename(
        'pokemon', 'data/type_effectiveness.json')
    with open(type_effectiveness_json) as f:
        for line in f:
            type_effectiveness = json.loads(line)
            yield pokemon.TypeEffectiveness(**type_effectiveness)

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
            species['base_stats'] = pokemon.Stats(**species.pop('baseStats'))
            yield pokemon.Species(**species)

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
        move['effect'] = pokemon.move_effect(**effect)
    return pokemon.move(**move)

def stream_moves():
    moves_json = pkg_resources.resource_filename('pokemon', 'data/moves.json')
    with open(moves_json) as f:
        for line in f:
            move = move_from_json(line)
            if move:
                yield move

MOVEDEX = pokedex.Movedex(stream_moves())
