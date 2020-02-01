from random import randint


def roll(n, sides, top=None):
    rolls = [randint(1, sides) for _ in range(n)]
    if top:
        return sum(sorted(rolls)[-top:])
    return sum(rolls)
