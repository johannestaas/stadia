import logging

from .gladiator import Gladiator

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
