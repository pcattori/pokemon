import collections

class Pokedex(collections.Sequence):
    def __init__(self, species):
        self.species = sorted(species, key=lambda s: s.national_pokedex_number)
        self._by_name = {species.name: species for species in self.species}

    def by_name(self, name):
        return self._by_name[name]

    def by_npn(self, national_pokedex_number):
        '''National Pokédex Number (NPN)'''
        return self[national_pokedex_number - 1]

    def __getitem__(self, index):
        return self.species[index]

    def __len__(self):
        return len(self.species)

class Movedex(collections.Collection):
    def __init__(self, moves):
        self.moves = moves
        self._by_name = {move.name: move for move in self.moves}

    def by_name(self, name):
        return self._by_name[name]

    def __contains__(self, item):
        return item in self.moves

    def __iter__(self):
        return iter(self.moves)

    def __len__(self):
        return len(self.moves)

