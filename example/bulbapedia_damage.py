import pokemon
# http://bulbapedia.bulbagarden.net/wiki/Damage#Example
# NOTE: this is a generation 1 library, so critical hits deal 2x damage
ice_fang = pokemon.Move(
    name='ice fang', type_='ice', category='physical', power=65, accuracy=.65, pp=15)

glaceon = pokemon.Pokemon(
    pokemon.Species(
        national_pokedex_number=471, name='glaceon', types=['ice'],
        base_stats=pokemon.Stats(
            hp=65, attack=60, defense=110, special=130, speed=65)),
    level=75, moves=[ice_fang])
glaceon._stats = pokemon.Stats(
    hp=201, attack=123, defense=181,
    special=glaceon.stats.special, speed=glaceon.stats.speed)
print('glaceon stats', glaceon.stats)

garchomp = pokemon.Pokemon(
    pokemon.Species(
        national_pokedex_number=445, name='garchomp', types=['dragon', 'ground'],
        base_stats=pokemon.Stats(
            hp=108, attack=130, defense=95, special=85, speed=102)),
        level=78, moves=[])
garchomp._stats = pokemon.Stats(
    hp=270, attack=210, defense=163,
    special=garchomp.stats.special, speed=garchomp.stats.speed)
print('garchomp stats', garchomp.stats)

dmg = pokemon.formulas.damage(glaceon, ice_fang, garchomp)
print(dmg)


