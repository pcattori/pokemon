import pokemon
charmander = pokemon.Pokemon(pokemon.species('charmander'), level=3, moves=[
    pokemon.move(move) for move in ('scratch', 'growl', 'ember', 'leer')])
# print('species', charmander.species)
# print('level', charmander.level)
# print('ivs', charmander.ivs)
# print('evs', charmander.evs)
# print('stats', charmander.stats)
# print('moves', charmander.moves)
squirtle = pokemon.Pokemon(pokemon.species('squirtle'), level=3, moves=[
    pokemon.move(move) for move in ('tackle', 'tail whip', 'bubble', 'water gun')])

dmg = pokemon.formulas.damage(squirtle, squirtle.moves[2], charmander)
print(dmg)
