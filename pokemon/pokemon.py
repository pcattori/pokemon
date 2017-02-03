import maps
import pokemon.core as core
import pokemon.data as data
import pokemon.formulas as formulas
import pokemon.utils as utils

DepletableMove = maps.namedfixedkey('DepletableMove', data.Move._fields + ('pp',))

class Pokemon:
    def __init__(
            self, species, level, moves=[], ivs=None, evs=None, nickname=None,
            status_condition=None):
        self.species = species
        self.nickname = nickname
        self.level = level

        self.ivs = ivs or formulas.random_ivs()
        self.evs = evs or core.Stats(*(5 * [0]))

        self.hp = self.stats.hp # start at full hp
        self.moves = {
            move.name: DepletableMove(pp=move.max_pp, **move)
            for move in moves}
        self.status_condition = status_condition

    @property
    def name(self):
        return self.nickname or self.species.name

    @property
    def stats(self):
        values = zip(self.species.base_stats, self.ivs, self.evs)
        hp = formulas.hp_calc(*(next(values) + (self.level,)))
        others = tuple(
            formulas.stat_calc(base, iv, ev, self.level)
            for base, iv, ev in values)
        return core.Stats(hp, *others)

    def __deepcopy__(self, _):
        return type(self)(
            species=self.species,
            nickname=self.nickname,
            level=self.level,
            ivs=self.ivs,
            evs=self.evs,
            hp=self.hp,
            moves={move.name: DepletableMove(**move) for move in self.moves},
            status_condition = self.status_condition)
