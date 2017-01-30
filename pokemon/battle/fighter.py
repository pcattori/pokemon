import collections
import maps
import pokemon.formulas as formulas
import pokemon.utils as utils

BattleStats = collections.namedtuple('BattleStats', [
    'attack', 'defense', 'special', 'speed', 'accuracy', 'evasion'])

StatStages = maps.namedfixedkey('StatStages', BattleStats._fields)

class Fighter(utils.FallbackWrapper):
    def __init__(self, pokemon, stat_stages=None):
        super().__init__(pokemon)
        self.stat_stages = stat_stages or StatStages(*(6 * [0]))
        self.volitile_status_conditions = {}

    @property
    def stage_multipliers(self):
        '''http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers'''
        return BattleStats(**{
            stat: formulas.STAGE_MULTIPLIERS[stage]
            for stat, stage in self.stat_stages.items()})

