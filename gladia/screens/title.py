import logging

from . import Menu, Screen

LOG = logging.getLogger(__name__)


class TitleMenu(Menu):
    new = '[n]ew game'
    load = '[l]oad game'
    quit = '[q]uit'


class TitleScreen(Screen):

    def run(self):
        item = TitleMenu.show(self.win)
        LOG.debug(f'selected {item!r}')
        if item is TitleMenu.new:
            LOG.info('new game')
            return item
        elif item is TitleMenu.load:
            raise NotImplementedError('cant load yet')
            return item
        else:
            return item
