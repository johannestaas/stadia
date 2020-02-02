import os
import math
import logging
from random import shuffle, randint, uniform

LOG = logging.getLogger(__name__)

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
        global NAMES
        nonlocal name_idx
        name = NAMES[name_idx].title()
        name_idx += 1
        if name_idx >= len(NAMES):
            shuffle(NAMES)
            name_idx = 0
        return name

    return random_name


def rand_prob(mn=0, mx=1):
    return uniform(mn, mx)


def attempt_with_bonus(base, bonus=0):
    prob = rand_prob()
    LOG.debug(
        f'attempt with bonus, base: {base}, bonus: {bonus}, prob: {prob}'
    )
    if bonus <= 0:
        # If no bonus, just check the roll against the base.
        # If accuracy (base) is 0.9, then we're checking a 90% rate of hit.
        return prob <= base
    # Use a logarithmic curve to determine the bonus.
    # The log value affects whether the difficulty is magnified or not.
    val = math.log(abs(bonus) + math.e)
    LOG.debug(f'math.log(abs(bonus) + math.e) = {val}')
    # This calc is waaay too helpful.
    difficulty = (1.0 - base) / val
    LOG.debug(f'difficulty is now {1.0 - difficulty}')
    return prob <= (1.0 - difficulty)


random_name = _name_randomizer()
