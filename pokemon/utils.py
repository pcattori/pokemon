import pokemon.data as data

def find_species(species_name):
    return data.POKEDEX.by_name(species_name)

def find_move(move_name):
    return data.MOVEDEX.by_name(move_name)

class FallbackWrapper:
    def __init__(self, fallback):
        # hit __dict__ directly to avoid calling __setattr__ before `_fallback` is assigned
        self.__dict__['_fallback'] = fallback

    def __getattr__(self, attr):
        return getattr(self._fallback, attr)

    def __setattr__(self, attr, value):
        if attr not in self.__dict__ and hasattr(self._fallback, attr):
            setattr(self._fallback, attr, value)
        else:
            # default behavior
            super().__setattr__(attr, value)
