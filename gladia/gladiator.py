import math
import logging
from dataclasses import dataclass

from .ai import AI
from .rand import roll, rand_name, attempt_with_bonus
from .gear import Weapon, Armor

CRITICAL_CHANCE = 0.05
CRITICAL_COEF = 1.5

LOG = logging.getLogger(__name__)


@dataclass
class AttackResult:
    hit: bool
    crit: bool
    dmg: int

    def __str__(self):
        if self.hit:
            if self.crit:
                return f'Critical Hit for {self.dmg} damage!'
            else:
                return f'Hit for {self.dmg} damage'
        else:
            return f'Miss'


@dataclass
class Gladiator:
    name: str
    hp: int
    max_hp: int
    _atk: int
    _def: int
    _agi: int
    _int: int
    pos: (int, int)
    weapon: Weapon
    armor: Armor
    ai: AI

    def __init__(self):
        self.name = rand_name()
        self.hp = 100
        self.max_hp = 100
        self._atk = roll(4, 6, top=3)
        self._def = roll(4, 6, top=3)
        self._agi = roll(4, 6, top=3)
        self._int = roll(4, 6, top=3)
        self.pos = (None, None)
        self.weapon = Weapon.fist()
        self.armor = Armor.skin()
        self.ai = AI(self)

    def blocks(self):
        return True

    def show(self, win):
        for i, msg in enumerate([
            f'Gladiator {self.name}',
            f'HP:       {self.hp}/{self.max_hp}',
            f'Atk:      {self._atk}',
            f'Def:      {self._def}',
            f'Agi:      {self._agi}',
            f'Int:      {self._int}',
            f'Wpn:      {self.weapon!r}',
            f'Arm:      {self.armor!r}',
        ]):
            win.write(msg, pos=(0, i))
        if self.pos[0] is not None:
            # If they're in the stadium, write their position.
            win.write(f'Pos:      {self.pos!r}', pos=(0, i + 1))

    def hit_or_miss(self, enemy):
        diff = self._agi - enemy._agi
        return attempt_with_bonus(self.weapon.acc, bonus=diff)

    def check_critical(self, enemy):
        diff = self._atk - enemy._def
        return attempt_with_bonus(CRITICAL_CHANCE, bonus=diff)

    def attack(self, enemy):
        LOG.info(f'{self.name} attacking {enemy.name}')
        if not self.hit_or_miss(enemy):
            LOG.info(f'{self.name} missed!')
            return AttackResult(hit=False, crit=False, dmg=0)
        dmg_result = self.weapon.damage()
        dmg_result.subtract_armor(enemy.armor)
        dmg_type, dmg = dmg_result.max()
        crit = self.check_critical(enemy)
        if crit:
            dmg = math.ceil(dmg * CRITICAL_COEF)
            LOG.debug(f'attack is critical!')
        enemy.take_damage(dmg)
        LOG.info(f'{self.name} did {dmg_type} damage for {dmg}')
        return AttackResult(hit=True, crit=crit, dmg=dmg)

    def take_damage(self, amt):
        self.hp -= amt
        LOG.debug(f'{self.name} HP at {self.hp}/{self.max_hp}')
        if self.is_dead():
            LOG.info(f'{self.name} was defeated!')
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0

    def cleanup(self):
        self.pos = (None, None)
        self.hp = self.max_hp

    def char(self):
        return 'G'

    def act(self, stadium, enemy_team):
        action, goal = self.ai.act(stadium, enemy_team)
        return action, goal
