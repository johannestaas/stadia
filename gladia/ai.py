from enum import Enum


class Behavior(Enum):
    attack = 'attack'
    move = 'move'
    escape = 'escape'


class AI:

    def __init__(self):
        self.target = None
        self.behave = Behavior.attack

    def __repr__(self):
        return f'AI(target={self.target!r}, behave={self.behave.value})'

    def __str__(self):
        if self.target is None:
            return self.behave.value
        if hasattr(self.target, 'name'):
            return f'{self.behave.value} {self.target.name}'
        return f'{self.behave.value} {self.target!r}'
