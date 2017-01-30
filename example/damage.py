import pokemon
import pokemon.battle
# NOTE: ivs are generated as if these pokemon were wild
# NOTE: evs are zeroed out
# NOTE: damage formula is non-deterministic so your results may vary
charmander = pokemon.pokemon('charmander', level=3, moves=[
    'scratch', 'growl', 'ember', 'leer'])

squirtle = pokemon.pokemon('squirtle', level=3, moves=[
    'tackle', 'tail whip', 'bubble', 'water gun'])

# deal damage
dmg = pokemon.formulas.damage(squirtle, squirtle.moves['bubble'], charmander)
print(dmg)
# example: prints => Damage(damage=13, luck=0.9900914399158687, critical_hit=False, effectiveness=2)
