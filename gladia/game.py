import logging

from ezcurses import Cursed

from .screens.title import TitleScreen

LOG = logging.getLogger(__name__)


def start():
    LOG.debug('starting...')
    with Cursed() as scr:
        screen = TitleScreen(scr)
