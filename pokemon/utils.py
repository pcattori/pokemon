import pokemon.pokedex as pokedex

def species(species_name):
    return pokedex.POKEDEX.by_name(species_name)

def move(move_name):
    return pokedex.MOVEDEX.by_name(move_name)
