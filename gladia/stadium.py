import logging
from dataclasses import dataclass
from itertools import product

from .rand import rand_pos, shuffle
from .ai import Action

LOG = logging.getLogger(__name__)


@dataclass
class Wall:
    pos: (int, int)

    def char(self):
        return '#'

    def blocks(self):
        return True


@dataclass
class Marker:
    pos: (int, int)

    def char(self):
        return 'O'

    def blocks(self):
        return False


class Team:

    def __init__(self, name, gladiators):
        self.name = name
        self.gladiators = gladiators

    def is_alive(self):
        for glad in self.gladiators:
            if glad.hp > 0:
                return True
        return False


class Stadium:

    def __init__(self, teams=None, size=(20, 20)):
        self.size = size
        self.teams = teams
        self._map = None
        self.init_map()
        if teams is not None:
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
        start_y_1 = (self.size[1] // 2) - (len(team1.gladiators) // 2)
        start_y_2 = (self.size[1] // 2) - (len(team2.gladiators) // 2)
        for i, glad in enumerate(team1.gladiators):
            pos = (0, start_y_1 + i)
            self[pos] = glad
        for i, glad in enumerate(team2.gladiators):
            pos = (self.size[0] - 1, start_y_2 + i)
            self[pos] = glad

    def cleanup(self):
        # Clean out map by reinitializing.
        self.init_map()
        if self.teams is not None:
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

    def empty_neighbors(self, pos, goal=None):
        '''
        Find all neighboring positions that are open to be moved on.
        For A* algorithm.

        "goal" is so that it returns it as an empty neighbor.
        '''
        neighbors = self.neighbors(pos)
        for n in neighbors[:]:
            if n == goal:
                continue
            if self[n] is not None:
                neighbors.remove(n)
        return neighbors

    def show(self, win):
        raise NotImplementedError('cant show you SHIT')

    def gen_coords(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield x, y

    def logshow(self):
        last_y = 0
        s = 'STADIUM =>\n\n'
        for x, y in self.gen_coords():
            if y > last_y:
                s += '\n'
                last_y = y
            if self[x, y] is None:
                s += '_'
            else:
                s += self[x, y].char()
        s += '\n'
        LOG.info(s)

    def mark(self, pos):
        self[pos] = Marker(pos)

    def has_empty(self):
        for x, y in self.gen_coords():
            if self[x, y] is None:
                return True
        return False

    def rand_pos_empty(self):
        if not self.has_empty():
            return None
        while True:
            pos = rand_pos(self)
            if self[pos] is None:
                return pos

    def gen_shuffled_gladiators(self):
        team_indices = list(range(len(self.teams)))
        shuffle(team_indices)
        for i_t in team_indices:
            team = self.teams[i_t]
            glad_indices = list(range(len(team.gladiators)))
            shuffle(glad_indices)
            for i_g in glad_indices:
                yield team.gladiators[i_g]

    def get_enemy_team(self, gladiator):
        if gladiator in self.teams[0].gladiators:
            return self.teams[1]
        return self.teams[0]

    def dead_teams(self):
        dead = []
        for team in self.teams:
            if not team.is_alive():
                dead.append(team)
        return dead

    def act(self):
        for glad in self.gen_shuffled_gladiators():
            action, target = glad.act(self, self.get_enemy_team(glad))
            if action is Action.nop:
                LOG.info(f'{glad.name} is not doing anything')
            elif action is Action.move:
                LOG.info(f'{glad.name} is moving to {target}')
                self[glad.pos] = None
                self[target] = glad
            elif action is Action.attack:
                LOG.info(f'{glad.name} is attacking {target.name}')
                glad.attack(target)
            dead = self.dead_teams()
            if dead:
                LOG.info(f'battle is over! dead teams: {dead!r}')
                return False
            self.logshow()
        return True
