import pokemon.battle.fighter as fighter
import collections.abc

class BattleTeam(collections.abc.Sequence):
    def __init__(self, members):
        self.members = tuple(members)
        self.fighter_index = 0
        self.fighter = fighter.Fighter(self.members[self.fighter_index], self)

    @property
    def reserves(self):
        for i, member in enumerate(self.members):
            if i != self.fighter_index and member.hp > 0:
                yield i, member

    def blacked_out(self):
        return all([member.hp <= 0 for member in self.members])

    def switch(self, member_index):
        member = self.members[member_index]
        if member_index == self.fighter_index:
            raise ValueError(f'{member.name} is already in battle!')
        if member.hp < 0:
            raise ValueError(f'{member.name} is fainted!')
        self.fighter_index = member_index
        self.fighter = fighter.Fighter(self.members[self.fighter_index], self)

    def __getitem__(self, index):
        return self.members[index]

    def __len__(self):
        return len(self.members)

