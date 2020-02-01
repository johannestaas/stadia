import re
import logging
from enum import Enum


__all__ = (
    'Menu',
    'get_input',
)


LOG = logging.getLogger(__name__)

RE_MENU_ITEM = re.compile(
    r'(?P<prefix>[^\[]*)\[(?P<shortcut>\w)\](?P<suffix>.*)'
)


class Menu(Enum):

    @classmethod
    def show(cls, win):
        max_size = win.max_size()
        max_len = 0
        LOG.debug(f'showing menu from {cls!r}')
        _map = []
        msgs = []
        for item in list(cls):
            _map.append(item)
            groups = RE_MENU_ITEM.match(item.value).groupdict()
            shortcut = groups['shortcut']
            msg = f'{groups["prefix"]}{shortcut}{groups["suffix"]}'
            msgs.append((shortcut, msg.title()))
            max_len = max(3 + len(msg), max_len)
        orig = (
            (max_size[0] // 2) - (max_len // 2),
            (max_size[1] // 2) - (len(msgs) // 2),
        )
        item = win.get_menu_item(msgs, orig=orig)
        return _map[item]

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


def int_validator(val):
    if val is None:
        return None
    if val.strip().isdigit():
        return int(val.strip())
    return None


def pos_int_validator(val):
    if val is None:
        return None
    if val.strip().isdigit():
        val = int(val.strip())
        if val > 0:
            return val
    return None


def get_input(scr, msg, pos=None, color=None, validator=None, echo=True):
    if validator == 'int':
        validator = int_validator
    elif validator == 'pos_int':
        validator = pos_int_validator
    pos = pos or (0, 0)
    while True:
        scr.write(msg, pos=pos, color=color)
        val = scr.getstr(pos=(pos[0] + len(msg), pos[1]), echo=echo)
        if validator is not None:
            val = validator(val)
            if val is not None:
                return val
        else:
            return val


class Screen:

    def __init__(self, scr):
        self.scr = scr
        self.size = self.scr.max_size()
        self.win = self.scr.new_win(orig=(0, 0), size=self.size)
