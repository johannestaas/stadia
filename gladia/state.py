class Resources:

    def __init__(self):
        self.denari = 0
        self.food = 100
        self.water = 100
        self.wine = 100
        self.bronze = 0
        self.leather = 0

    def show(self, win):
        win.write(f'denari:  {self.denari}', pos=(0, 0))
        win.write(f'food:    {self.food}', pos=(0, 1))
        win.write(f'water:   {self.water}', pos=(0, 2))
        win.write(f'wine:    {self.wine}', pos=(0, 3))
        win.write(f'bronze:  {self.bronze}', pos=(0, 4))
        win.write(f'leather: {self.leather}', pos=(0, 5))


class GameState:

    def __init__(self):
        self.gladiators = []
        self.res = Resources()

    def show_resources(self, win):
        self.res.show(win)
