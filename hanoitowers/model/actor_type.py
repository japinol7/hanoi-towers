"""Module actor_type."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum


class ActorBaseType(Enum):
    NONE = 0
    ITEM = 1


class ActorCategoryType(Enum):
    NONE = 0
    DISC = 1
    TOWER = 2
    CLOCK = 11
    SELECTOR = 53


class ActorType(Enum):
    DISC_1 = 1
    DISC_2 = 2
    DISC_3 = 3
    DISC_4 = 4
    DISC_5 = 5
    DISC_6 = 6
    DISC_7 = 7
    TOWER_1 = 15
    TOWER_2 = 16
    TOWER_3 = 17
    CLOCK_A = 21
    CLOCK_TIMER_A = 22
    CLOCK_STOPWATCH_A = 31
    SELECTOR_A = 5401
