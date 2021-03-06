import logging

from ezcurses import Cursed

from .state import GameState
from .screens.title import TitleScreen, TitleMenu

LOG = logging.getLogger(__name__)


def start():
    LOG.debug('starting...')
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
