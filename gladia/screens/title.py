import logging

from . import Menu

LOG = logging.getLogger(__name__)


class TitleMenu(Menu):
    new = '[n]ew game'
    load = '[l]oad game'
    quit = '[q]uit'


class TitleScreen:

    def __init__(self, scr):
        size = scr.max_size()
        self.win = scr.new_win(orig=(0, 0), size=size)
        item = TitleMenu.show(self.win)
        LOG.debug(f'selected {item!r}')
        if item is TitleMenu.new:
            LOG.info('new game')
        elif item is TitleMenu.load:
            raise NotImplementedError('cant load yet')
        else:
            return None
