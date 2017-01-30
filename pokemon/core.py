import collections
import maps

Stats = collections.namedtuple('Stats', [
    'hp', 'attack', 'defense', 'special', 'speed'])

# TODO differentiate between persistent and volitile status conditions
# for persistent, turns is only applicable in batte
StatusCondition = maps.namedfixedkey('StatusCondition', [
    'name', 'turns'])

