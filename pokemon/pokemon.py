import pokemon.core as pokemon
import pokemon.formulas as formulas
import pokemon.pokedex as pokedex

class Pokemon:
    def __init__(self, species, level, moves={}, ivs=None, evs=None):
        self.species = species
        self.level = level

        self.ivs = ivs or formulas.random_ivs()
        self.evs = evs or pokemon.Stats(0, 0, 0, 0, 0)

        self._stats = None
        self.hp = self.stats.hp # start at full hp
        self.moves = moves
        # TODO status condition

    @property
    def stats(self):
        if self._stats is None:
            values = zip(self.species.base_stats, self.ivs, self.evs)
            hp = formulas.hp_calc(*(next(values) + (self.level,)))
            others = tuple(
                formulas.stat_calc(base, iv, ev, self.level)
                for base, iv, ev in values)
            self._stats = pokemon.Stats(hp, *others)
        return self._stats
