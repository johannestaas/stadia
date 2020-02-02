import logging

from .gladiator import Gladiator
from .stadium import Stadium, Wall
from .ai import AI
from .rand import rand_pos

LOG = logging.getLogger(__name__)


def debug_fight():
    glad1 = Gladiator()
    LOG.debug(repr(glad1))
    glad2 = Gladiator()
    LOG.debug(repr(glad2))

    while True:
        glad1.attack(glad2)
        if glad2.is_dead():
            LOG.debug(f'{glad1!r} defeated {glad2!r}')
            break
        glad2.attack(glad1)
        if glad1.is_dead():
            LOG.debug(f'{glad2!r} defeated {glad1!r}')
            break


def debug_a_star():
    stadium = Stadium(size=(20, 20))
    for i in range(100):
        wall_pos = rand_pos(stadium)
        if stadium[wall_pos] is None:
            stadium[wall_pos] = Wall(pos=wall_pos)
    start = stadium.rand_pos_empty()
    goal = stadium.rand_pos_empty()
    path = AI.a_star(start, stadium, goal)
    if path is None:
        LOG.warning(f'no path from {start} to {goal}!')
    else:
        for pos in path:
            stadium.mark(pos)
        LOG.info(f'path from {start} to {goal}: {path!r}')
    stadium.logshow()
