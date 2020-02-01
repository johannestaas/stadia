import os
from random import choice, randint

DIRNAME = os.path.dirname(__file__)
with open(os.path.join(DIRNAME, 'data', 'names.txt')) as f:
    NAMES = [x.strip().title() for x in f.readlines() if x.strip()]


def roll(n, sides, top=None):
    rolls = [randint(1, sides) for _ in range(n)]
    if top:
        return sum(sorted(rolls)[-top:])
    return sum(rolls)


def random_name():
    return choice(NAMES).title()
