import logging
from dataclasses import dataclass

from .rand import roll, random_name, attempt_with_bonus
from .gear import Weapon, Armor

LOG = logging.getLogger(__name__)


@dataclass
class AttackResult:
    hit: bool
    dmg: int

    def __str__(self):
        if self.hit:
            return f'Hit for {self.dmg} damage'
        else:
            return f'Miss'


@dataclass
class Gladiator:
    name: str
    hp: int
    max_hp: int
    _attack: int
    _agility: int
    _intel: int
    weapon: Weapon
    armor: Armor

    def __init__(self):
        self.name = random_name()
        self.hp = 100
        self.max_hp = 100
        self._attack = roll(4, 6, top=3)
        self._agility = roll(4, 6, top=3)
        self._intel = roll(4, 6, top=3)
        self.weapon = Weapon.fist()
        self.armor = Armor.skin()

    def show(self, win):
        for i, msg in enumerate([
            f'Gladiator {self.name}',
            f'HP:       {self.hp}/{self.max_hp}',
            f'Atk:      {self._attack}',
            f'Agi:      {self._agility}',
            f'Int:      {self._intel}',
            f'Wpn:      {self.weapon!r}',
            f'Arm:      {self.armor!r}',
        ]):
            win.write(msg, pos=(0, i))

    def hit_or_miss(self, enemy):
        diff = self._agility - enemy._agility
        return attempt_with_bonus(self.weapon.acc, bonus=diff)

    def attack(self, enemy):
        LOG.debug(f'{self.name} attacking {enemy.name}')
        if not self.hit_or_miss(enemy):
            LOG.debug(f'{self.name} missed!')
            return AttackResult(hit=False, dmg=0)
        LOG.debug(f'{self.name} hit!')
        dmg_result = self.weapon.damage()
        LOG.debug(f'result: {dmg_result!r}')
        dmg_result.subtract_armor(enemy.armor)
        LOG.debug(f'after subtracting enemy armor: {dmg_result!r}')
        dmg_type, dmg = dmg_result.max()
        enemy.take_damage(dmg)
        LOG.debug(f'{self.name} did {dmg_type} damage for {dmg}')
        return AttackResult(hit=True, dmg=dmg)

    def take_damage(self, amt):
        self.hp -= amt
        LOG.debug(f'{self.name} HP at {self.hp}/{self.max_hp}')
        if self.is_dead():
            LOG.debug(f'{self.name} was defeated!')
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0
