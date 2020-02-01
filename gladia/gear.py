from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    pierce: (int, int)
    blunt: (int, int)
    slash: (int, int)
    range: int
    speed: float
    acc: float

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'{self.name} ('
            f'Prc:{self.pierce!r}, '
            f'Blt:{self.blunt!r}, '
            f'Sla:{self.slash!r}, '
            f'Rg:{self.range}, '
            f'Spd:{self.speed:0.3}, '
            f'Acc:{self.acc:0.3}'
            f')'
        )

    @classmethod
    def fist(cls):
        return cls(
            name='fist',
            pierce=(0, 0), blunt=(2, 4), slash=(0, 0),
            range=1, speed=2.0, acc=0.9,
        )

    @classmethod
    def staff(cls):
        return cls(
            name='staff',
            pierce=(0, 0), blunt=(3, 5), slash=(0, 0),
            range=3, speed=1.5, acc=0.9,
        )

    @classmethod
    def knife(cls):
        return cls(
            name='knife',
            pierce=(3, 7), blunt=(0, 0), slash=(3, 5),
            range=1, speed=2.0, acc=0.9,
        )

    @classmethod
    def gladius(cls):
        return cls(
            name='gladius',
            pierce=(7, 15), blunt=(0, 0), slash=(5, 12),
            range=2, speed=1.7, acc=0.9,
        )


@dataclass
class Armor:
    name: str
    pierce: int
    blunt: int
    slash: int
    weight: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'{self.name} ('
            f'Prc:{self.pierce}, '
            f'Blt:{self.blunt}, '
            f'Sla:{self.slash}, '
            f'Wt:{self.weight}'
            f')'
        )

    @classmethod
    def skin(cls):
        return cls(
            name='skin',
            pierce=0, blunt=0, slash=0, weight=0,
        )

    @classmethod
    def leather_straps(cls):
        return cls(
            name='leather straps',
            pierce=0, blunt=1, slash=0, weight=1,
        )

    @classmethod
    def basic_leather(cls):
        return cls(
            name='basic leather',
            pierce=1, blunt=3, slash=3, weight=2,
        )

    @classmethod
    def full_leather(cls):
        return cls(
            name='full leather',
            pierce=2, blunt=7, slash=5, weight=3,
        )

    @classmethod
    def full_hardened_leather(cls):
        return cls(
            name='full hardened leather',
            pierce=5, blunt=10, slash=7, weight=5,
        )
