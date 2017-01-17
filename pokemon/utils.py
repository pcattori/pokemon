import pokemon.data as data

def find_species(species_name):
    return data.POKEDEX.by_name(species_name)

def find_move(move_name):
    return data.MOVEDEX.by_name(move_name)
