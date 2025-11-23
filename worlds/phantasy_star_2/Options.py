from Options import PerGameCommonOptions, Range, Choice
from dataclasses import dataclass

from .Goals import GOAL_MOTHER_BRAIN


class Goal(Choice):
    """
    Mother Brain: Finish the whole game.
    """
    display_name = "Goal"
    default = GOAL_MOTHER_BRAIN
    option_mother_brain = GOAL_MOTHER_BRAIN


class MesetaMultiplier(Range):
    """
    Multiplier applied to meseta earned from battle.
    """
    display_name = "Meseta Multiplier"
    range_start = 1
    range_end = 100
    default = 2


class XPMultiplier(Range):
    """
    Multiplier applied to experience earned from battle.
    """
    display_name = "XP Multiplier"
    range_start = 1
    range_end = 100
    default = 2


class UsefulItems(Range):
    """
    Percentage of items in the pool that are 'useful'.
    """
    display_name = "Useful Items"
    range_start = 0
    range_end = 100
    default = 75


# TODO shuffle instead of random items

# TODO death link lol


@dataclass
class PhSt2Options(PerGameCommonOptions):
    goal: Goal
    meseta_multi: MesetaMultiplier
    xp_multi: XPMultiplier
    useful_items: UsefulItems
