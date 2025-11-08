from Options import PerGameCommonOptions, Range, Choice
from dataclasses import dataclass

from .Goals import GOAL_DARK_SOL, GOAL_TRIALS, GOAL_STRENGTH


class Goal(Choice):
    """
    Dark Sol: Finish the whole dungeon.
    Trials: Finish every Trial Cave.
    Strength: Finish the Trial of Strength.
    """
    display_name = "Goal"
    default = GOAL_DARK_SOL
    option_dark_sol = GOAL_DARK_SOL
    option_trials = GOAL_TRIALS
    option_strength = GOAL_STRENGTH


class GoldMultiplier(Range):
    """
    Multiplier applied to gold earned from battle.
    """
    display_name = "Gold Multiplier"
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


# TODO mimic percentage?

# TODO death link lol


@dataclass
class SITDOptions(PerGameCommonOptions):
    goal: Goal
    gold_multi: GoldMultiplier
    xp_multi: XPMultiplier
    useful_items: UsefulItems
