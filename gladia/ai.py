from enum import Enum


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
                pass
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
        closest_enemy = sorted(dists)[0][1]
        return closest_enemy

    def a_star(self, stadium, target_pos):
        paths = {}
        closed_cells = []
        pos = self.gladiator.pos
        open_cells = set(stadium.empty_neighbors(pos))
        closed_cells = set()
        while True:
            if not open_cells:
                return None
            dists = []
            for open_cell in open_cells:
                dists.append((
                    calc_distance(open_cell, target_pos),
                    open_cell,
                ))
            dists = sorted(dists)
            neighbors = set(stadium.empty_neighbors(pos)) - closed_cells
            if not neighbors:
                closed_cells.add(pos)

