from .rand import roll


class Gladiator:

    def __init__(self):
        self.name = 'Rollo'
        self.hp = 100
        self.attack = roll(4, 6, top=3)
        self.defense = roll(4, 6, top=3)
        self.agility = roll(4, 6, top=3)
        self.intel = roll(4, 6, top=3)

    def show(self, win):
        for i, msg in enumerate([
            f'Gladiator {self.name}',
            f'HP:       {self.hp}',
            f'Atk:      {self.attack}',
            f'Def:      {self.defense}',
            f'Agi:      {self.agility}',
            f'Int:      {self.intel}',
        ]):
            win.write(msg, pos=(0, i))
