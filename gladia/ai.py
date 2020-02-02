import logging
from enum import Enum

LOG = logging.getLogger(__name__)


def calc_distance(pos1, pos2):
    '''
    This is calculating by considering one diagonal spot costs the same as any
    other direction.
    '''
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    # Since you can go diagonal, it's really about just covering the max of
    # these. For example, if the enemy is 5 right and 3 up, you can cover the 3
    # up with 3 right/up diagonal moves, then go 2 more right.
    # ...so it's really just the max of the delta of the two directions.
    return max(dx, dy)


class Behavior(Enum):
    attack = 'attack'
    move = 'move'
    escape = 'escape'
    nop = 'nothing'


class Action(Enum):
    attack = 'attack'
    move = 'move'
    nop = 'nothing'


class AI:

    def __init__(self, gladiator):
        self.gladiator = gladiator
        self.target = None
        self.behave = Behavior.attack
        self.path = None

    def __repr__(self):
        return (
            f'AI('
            f'target={self.target!r}, '
            f'behave={self.behave.value}, '
            f'path={self.path!r}'
            f')'
        )

    def __str__(self):
        if self.target is None:
            return self.behave.value
        if hasattr(self.target, 'name'):
            return f'{self.behave.value} {self.target.name}'
        return f'{self.behave.value} {self.target!r}'

    def act(self, stadium, enemy_team):
        if self.behave is Behavior.attack:
            if self.target is None:
                self.target = self.find_target(stadium, enemy_team)
            dist = calc_distance(self.gladiator.pos, self.target.pos)
            if dist > self.gladiator.weapon.range:
                # Have to move closer.
                path = AI.a_star(self.gladiator.pos, stadium, self.target.pos)
                if path is None:
                    LOG.warning(
                        f'{self.gladiator!r} has no path to {self.target!r}'
                    )
                    return Action.nop, None
                return Action.move, path[0]
            else:
                # We can attack.
                return Action.attack, self.target
        else:
            raise NotImplementedError('no chill, only ATTACK')

    def find_target(self, stadium, enemy_team):
        dists = []
        for enemy in enemy_team.gladiators:
            dists.append((
                calc_distance(self.gladiator.pos, enemy.pos),
                enemy
            ))
        # Sort by distance, then pick the second element, the enemy.
        closest_enemy = sorted(dists, key=lambda x: x[0])[0][1]
        return closest_enemy

    @staticmethod
    def a_star_least_f(open_cells, goal):
        dists = []
        for open_cell in open_cells:
            dists.append((
                calc_distance(open_cell, goal),
                open_cell,
            ))
        dists = sorted(dists)
        return dists[0]

    @staticmethod
    def a_star_reconstruct_path(paths, goal):
        path = []
        current = goal
        while paths[current] is not None:
            path.append(paths[current])
            current = paths[current]
        # Reverse it, as it was goal to start
        return path[::-1]

    @staticmethod
    def a_star(start, stadium, goal):
        paths = {}
        closed_cells = []
        open_cells = {start}
        closed_cells = set()
        last = None
        while True:
            if not open_cells:
                # Failed. No path.
                return None
            dist, current = AI.a_star_least_f(open_cells, goal)
            paths[current] = last
            if current == goal:
                break
            closed_cells.add(current)
            neighbors = set(stadium.empty_neighbors(current))
            open_cells = (open_cells | neighbors) - closed_cells
            last = current
        return AI.a_star_reconstruct_path(paths, goal)
