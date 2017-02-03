import collections
import collections.abc
import maps
import pokemon.core as core
import pokemon.formulas as formulas
import pokemon.utils as utils

StatStages = maps.namedfixedkey('StatStages', core.BattleStats._fields)

class Fighter(utils.Wrapper):
    def __init__(
            self, pokemon, stat_stages=None,
            volitile_status_conditions=None, status_condition_timers=None):
        super().__init__(pokemon) # wrapper for pokemon
        self.stat_stages = stat_stages or StatStages(*(6 * [0]))
        self.volitile_status_conditions = volitile_status_conditions or set()
        self.status_condition_timers = status_condition_timers or {}

        if self.status_condition == 'sleep':
            self.status_condition_timers['sleep'] = formulas.sleep_turns()

    @property
    def stage_multipliers(self):
        '''http://bulbapedia.bulbagarden.net/wiki/Statistic#Stage_multipliers'''
        return core.BattleStats(**{
            stat: formulas.STAGE_MULTIPLIERS[stage]
            for stat, stage in self.stat_stages.items()})

class Team(collections.abc.Sequence):
    def __init__(self, members, fighter_index=0, fighter_kwargs={}):
        self.members = tuple(members)
        self.fighter_index = fighter_index
        self.fighter = Fighter(self.members[self.fighter_index], **fighter_kwargs)
        self.fighter.team = self

    @property
    def reserves(self):
        for i, member in enumerate(self.members):
            if i != self.fighter_index and member.hp > 0:
                yield i, member

    def blacked_out(self):
        return all([member.hp <= 0 for member in self.members])

    def switch_in(self, member_index):
        if member_index == self.fighter_index:
            raise ValueError(f'{member.name} is already in battle!')

        member = self.members[member_index]
        if member.hp < 0:
            raise ValueError(f'{member.name} is fainted!')
        self.fighter_index = member_index
        self.fighter = Fighter(self, self.members[self.fighter_index])
        self.fighter.team = self

    def __getitem__(self, index):
        return self.members[index]

    def __len__(self):
        return len(self.members)

    def __deepcopy__(self, _):
        fighter_kwargs = dict(
            stat_stages=StatStages(**self.fighter.stat_stages),
            volitile_status_conditions=set(volitile_status_conditions),
            status_condition_timers=dict(status_condition_timers))

        return type(self)(
            members=[copy.deepcopy(member) for member in self.members],
            fighter_index=self.fighter_index,
            fighter_kwargs=fighter_kwargs)
