import pokemon
# taken from http://bulbapedia.bulbagarden.net/wiki/Damage#Example
# NOTE: this is a generation 1 library so:
# - critical hits deal 2x damage, not 1.5x
# - we will have to manually create Pokemon and Moves that are not gen1 (see example/damage.py for how to leverage built-in Pokemon and moves)
# NOTE: some values are generated randomly so your results may vary a bit

# first let's make ice_fang since its not a built-in (read: not gen1) move
ice_fang = pokemon.Move(
    name='ice fang', type_='ice', category='physical', power=65, accuracy=.65, pp=15)

# similarily, we will have to make glaceon since its not gen1
glaceon = pokemon.Pokemon(
    pokemon.Species(
        national_pokedex_number=471, name='glaceon', types=['ice'],
        base_stats=pokemon.Stats(
            hp=65, attack=60, defense=110, special=130, speed=65)),
    level=75, moves=[ice_fang])

# hard-code stats as given in the example on bulbapedia
glaceon._stats = pokemon.Stats(
    hp=201, attack=123, defense=181,
    special=glaceon.stats.special, speed=glaceon.stats.speed)
print('glaceon stats', glaceon.stats)
# example: prints => glaceon stats Stats(hp=201, attack=123, defense=181, special=221, speed=110)

# again, have to manually construct garchomp since its not gen1
garchomp = pokemon.Pokemon(
    pokemon.Species(
        national_pokedex_number=445, name='garchomp', types=['dragon', 'ground'],
        base_stats=pokemon.Stats(
            hp=108, attack=130, defense=95, special=85, speed=102)),
        level=78, moves=[])

# again, hard-code stats to match example given by bulbapedia
garchomp._stats = pokemon.Stats(
    hp=270, attack=210, defense=163,
    special=garchomp.stats.special, speed=garchomp.stats.speed)
print('garchomp stats', garchomp.stats)
# example: prints => garchomp stats Stats(hp=270, attack=210, defense=163, special=156, speed=176)

# do some damage!
dmg = pokemon.formulas.damage(glaceon, glaceon.moves['ice fang'], garchomp)
print(dmg)
# example: prints => Damage(damage=180, luck=0.8999687147313562, critical_hit=False, effectiveness=4)

