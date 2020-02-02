import os
import math
import logging
from random import shuffle, randint, uniform

LOG = logging.getLogger(__name__)

DIRNAME = os.path.dirname(__file__)
with open(os.path.join(DIRNAME, 'data', 'names.txt')) as f:
    NAMES = [x.strip().title() for x in f.readlines() if x.strip()]
    shuffle(NAMES)

BONUS_COEF = 0.025
BONUS_CALC_COEF = 0.25


def sigmoid(x):
    return (
        1 /
        (1 + math.exp(-x))
    )


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


def calc_bonus_coef(bonus):
    coef = math.log(abs(bonus * BONUS_CALC_COEF) + math.e)
    LOG.debug(f'math.log(abs({bonus} * {BONUS_CALC_COEF}) + math.e) = {coef}')
    return coef


def calc_bonus_difficulty(base, bonus):
    # Use a logarithmic curve to determine the bonus.
    # The log value affects whether the difficulty is magnified or not.
    coef = calc_bonus_coef(bonus)
    diff = 1.0 - base
    new_diff = diff - (BONUS_COEF * coef)
    new_diff = max(new_diff, 0)
    LOG.debug(f'diff was: {diff} with bonus {bonus}: {new_diff}')
    return new_diff


def attempt_with_bonus(base, bonus=0):
    prob = rand_prob()
    if bonus <= 0:
        # If no bonus, just check the roll against the base.
        # If accuracy (base) is 0.9, then we're checking a 90% rate of hit.
        return prob <= base
    LOG.debug(
        f'attempt with bonus, base: {base}, bonus: {bonus}, prob: {prob}'
    )
    diff = calc_bonus_difficulty(base, bonus)
    return prob <= (1.0 - diff)


random_name = _name_randomizer()
