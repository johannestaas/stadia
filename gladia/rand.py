import os
from random import shuffle, randint

DIRNAME = os.path.dirname(__file__)
with open(os.path.join(DIRNAME, 'data', 'names.txt')) as f:
    NAMES = [x.strip().title() for x in f.readlines() if x.strip()]
    shuffle(NAMES)


def roll(n, sides, top=None):
    rolls = [randint(1, sides) for _ in range(n)]
    if top:
        return sum(sorted(rolls)[-top:])
    return sum(rolls)


def _name_randomizer():
    name_idx = 0

    def random_name():
        nonlocal name_idx
        name = NAMES[name_idx].title()
        name_idx += 1
        name_idx %= len(NAMES)
        return name

    return random_name


random_name = _name_randomizer()
