import pokemon.core as pokemon
import pokemon.formulas as formulas
import pokemon.utils as utils

class DepletableMove(utils.FallbackWrapper):
    def __init__(self, move, pp=None):
        super().__init__(move)
        if pp is None:
            pp = move.max_pp
        self.pp = pp

class Pokemon:
    def __init__(self, species, level, moves=[], ivs=None, evs=None, nickname=None):
        self.species = species
        self.nickname = nickname
        self.level = level

        self.ivs = ivs or formulas.random_ivs()
        self.evs = evs or pokemon.Stats(0, 0, 0, 0, 0)

        self._stats = None
        self.hp = self.stats.hp # start at full hp
        self.moves = {
            move.name: DepletableMove(move)
            for move in moves}
        # TODO status condition

    @property
    def name(self):
        return self.nickname or self.species.name

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
