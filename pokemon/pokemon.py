import maps
import pokemon.core as core
import pokemon.data as data
import pokemon.formulas as formulas
import pokemon.utils as utils

DepletableMove = maps.namedfixedkey('DepletableMove', data.Move._fields + ('pp',))

class Pokemon:
    def __init__(self, species, level, moves=[], ivs=None, evs=None, nickname=None):
        self.species = species
        self.nickname = nickname
        self.level = level

        self.ivs = ivs or formulas.random_ivs()
        self.evs = evs or core.Stats(*(5 * [0]))

        self._stats = None
        self.hp = self.stats.hp # start at full hp
        self.moves = {
            move.name: DepletableMove(pp=move.max_pp, **move)
            for move in moves}
        self.status_condition = None

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
            self._stats = core.Stats(hp, *others)
        return self._stats
