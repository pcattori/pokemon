import collections
import maps

Stats = collections.namedtuple('Stats', [
    'hp', 'attack', 'defense', 'special', 'speed'])

BattleStats = collections.namedtuple('BattleStats', [
    'attack', 'defense', 'special', 'speed', 'accuracy', 'evasion'])

