import collections
import json
import pkg_resources
import pokemon.core as pokemon

def _load_pokedex():
    species_json = pkg_resources.resource_filename('pokemon', 'data/species.json')
    with open(species_json) as f:
        for line in f:
            species = json.loads(line)
            species['base_stats'] = pokemon.Stats(**species.pop('baseStats'))
            yield pokemon.Species(**species)

def _load_moves():
    moves_json = pkg_resources.resource_filename('pokemon', 'data/moves.json')
    with open(moves_json) as f:
        for line in f:
            move = json.loads(line)
            move['type_'] = move.pop('type')
            yield pokemon.Move(**move)

class Pokedex(collections.Sequence):
    def __init__(self):
        self._pokedex = sorted(
            _load_pokedex(),
            key=lambda species: species.national_pokedex_number)
        self._by_name = {species.name: species for species in self._pokedex}

    def by_name(self, name):
        return self._by_name[name]

    def by_npn(self, national_pokedex_number):
        '''National Pokédex Number (NPN)'''
        return self[national_pokedex_number - 1]

    def __getitem__(self, index):
        return self._pokedex[index]

    def __len__(self):
        return len(self._pokedex)

class Movedex(collections.Collection):
    def __init__(self):
        self._moves = frozenset(_load_moves())
        self._by_name = {move.name: move for move in self._moves}

    def by_name(self, name):
        return self._by_name[name]

    def __contains__(self, item):
        return item in self._moves

    def __iter__(self):
        return iter(self._moves)

    def __len__(self):
        return len(self._moves)

POKEDEX = Pokedex()
MOVEDEX = Movedex()

