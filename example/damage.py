import pokemon
# NOTE: ivs are generated as if these pokemon were wild
# NOTE: evs are zeroed out
# NOTE: damage formula is non-deterministic so your results may vary
charmander = pokemon.Pokemon(pokemon.find_species('charmander'), level=3, moves=[
    pokemon.find_move(move) for move in ('scratch', 'growl', 'ember', 'leer')])

squirtle = pokemon.Pokemon(pokemon.find_species('squirtle'), level=3, moves=[
    pokemon.find_move(move) for move in ('tackle', 'tail whip', 'bubble', 'water gun')])

dmg = pokemon.formulas.damage(squirtle, squirtle.moves['bubble'], charmander)
print(dmg)
# example: prints => Damage(damage=13, luck=0.9900914399158687, critical_hit=False, effectiveness=2)
