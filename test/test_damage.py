import pokemon
import unittest

# NOTE: this is a generation 1 library so:
# - critical hits deal 2x damage, not 1.5x
# - manually create Pokemon and Moves that are not gen1

# first let's make ice_fang since its not a built-in (read: not gen1) move
ice_fang = pokemon.move(
    name='ice fang', type_='ice', category='physical',
    power=65, accuracy=.65, max_pp=15)

# similarily, have to make glaceon since its not gen1
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

class BulbapediaDamageTest(unittest.TestCase):
    '''http://bulbapedia.bulbagarden.net/wiki/Damage#Example'''

    def test_worst_luck(self):
        dmg = pokemon.formulas.damage(
            glaceon, glaceon.moves['ice fang'], garchomp, luck=0.85, critical_hit=False)
        self.assertEqual(dmg.damage, 170)

    def test_best_luck(self):
        dmg = pokemon.formulas.damage(
            glaceon, glaceon.moves['ice fang'], garchomp, luck=1.0, critical_hit=False)
        self.assertEqual(dmg.damage, 200)

    def test_nondeterministic_luck(self):
        dmg = pokemon.formulas.damage(
            glaceon, glaceon.moves['ice fang'], garchomp, critical_hit=False)
        self.assertIn(dmg.damage, range(170, 201))

if __name__ == '__main__':
    unittest.main()
