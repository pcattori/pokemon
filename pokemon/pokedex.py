import collections.abc

class Pokedex(collections.abc.Sequence):
    def __init__(self, species):
        self.species = sorted(species, key=lambda s: s.national_pokedex_number)
        self._by_name = {species.name: species for species in self.species}

    def by_name(self, name):
        return self._by_name[name]

    def by_national_pokedex_number(self, national_pokedex_number):
        '''National Pokédex Number (NPN)'''
        return self[national_pokedex_number - 1]

    def __getitem__(self, index):
        return self.species[index]

    def __len__(self):
        return len(self.species)

class Movedex(collections.abc.Mapping):
    def __init__(self, moves):
        self.moves = {move.name: move for move in moves}

    def __getitem__(self, name):
        return self.moves[name]

    def __iter__(self):
        return iter(self.moves)

    def __len__(self):
        return len(self.moves)

