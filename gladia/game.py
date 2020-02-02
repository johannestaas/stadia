import logging

from ezcurses import Cursed

from .state import GameState
from .screens.title import TitleScreen, TitleMenu

LOG = logging.getLogger(__name__)


def start():
    LOG.debug('starting...')
    from .gladiator import Gladiator
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

    with Cursed() as scr:
        screen = TitleScreen(scr)
        selection = screen.run()
        if selection is TitleMenu.new:
            state = GameState()
            scr.clear()
            state.show_resources(scr)
            scr.getch()
            scr.clear()
            state.show_gladiators(scr)
        else:
            return
