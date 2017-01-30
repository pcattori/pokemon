from pokemon.data import MOVEDEX, POKEDEX, TYPE_CHART, find_move, find_species
from pokemon.pokemon import Pokemon

def pokemon(species_name, level, moves, ivs=None, evs=None, nickname=None):
    return Pokemon(
        find_species(species_name), level,
        [find_move(move_name) for move_name in moves],
        ivs=ivs, evs=evs, nickname=nickname)
