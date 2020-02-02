import logging
from itertools import product

LOG = logging.getLogger(__name__)


class Team:

    def __init__(self, name, gladiators):
        self.name = name
        self.gladiators = gladiators


class Stadium:

    def __init__(self, teams=None, size=(20, 20)):
        self.size = size
        self.teams = teams
        self._map = None
        self.init_map()
        self.init_positions()

    def __getitem__(self, x_y):
        x, y = x_y
        return self._map[x][y]

    def __setitem__(self, x_y, val):
        x, y = x_y
        if hasattr(val, 'pos'):
            val.pos = x_y
        self._map[x][y] = val

    def init_map(self):
        # List of columns, so you can get it by self._map[x][y]
        self._map = [
            [None for _ in range(self.size[1])]
            for _ in range(self.size[0])
        ]

    def init_positions(self):
        team1, team2 = self.teams
        start_y_1 = (self.size[1] // 2) - (len(team1) // 2)
        start_y_2 = (self.size[1] // 2) - (len(team2) // 2)
        for i, glad in enumerate(team1.gladiators):
            pos = (0, start_y_1 + i)
            self[pos] = glad
        for i, glad in enumerate(team2.gladiators):
            pos = (self.size[0] - 1, start_y_2 + i)
            self[pos] = glad

    def cleanup(self):
        # Clean out map by reinitializing.
        self.init_map()
        for team in self.teams:
            for glad in team.gladiators:
                # Heals HP, and removes pos.
                glad.cleanup()

    def neighbors(self, pos):
        '''
        Given a position, return the position of all neighbor cells.
        For A* algorithm.
        '''
        neighbors = []
        deltas = list(product([-1, 0, 1], [-1, 0, 1]))
        # Don't return the same cell.
        deltas.remove((0, 0))
        for dx, dy in deltas:
            posx, posy = pos[0] + dx, pos[1] + dy
            # Filter out illegal positions.
            if posx < 0 or posx >= self.size[0]:
                continue
            if posy < 0 or posy >= self.size[1]:
                continue
            neighbors.append((posx, posy))
        return neighbors

    def empty_neighbors(self, pos):
        '''
        Find all neighboring positions that are open to be moved on.
        For A* algorithm.
        '''
        neighbors = self.neighbors(pos)
        for n in neighbors[:]:
            if self[n] is not None:
                neighbors.remove(n)
        return neighbors