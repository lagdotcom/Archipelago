from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range

from .goals import GOAL_DARK_SOL, GOAL_STRENGTH, GOAL_TRIALS


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


DIST_SHUFFLE = 0
DIST_RANDO = 1


class ItemDistribution(Choice):
    """
    Shuffle: Shuffle vanilla item placement.
    Rando: Randomly add items to the game.
    """

    display_name = "Item Distribution"
    default = DIST_SHUFFLE
    option_shuffle = DIST_SHUFFLE
    option_rando = DIST_RANDO


class UsefulItems(Range):
    """
    Percentage of items in the pool that are 'useful'.
    """

    display_name = "Useful Items"
    range_start = 0
    range_end = 100
    default = 75


class MimicItems(Range):
    """
    Percentage of items in the pool that are 'mimics'.
    """

    display_name = "Mimic Items"
    range_start = 0
    range_end = 100
    default = 10


# TODO death link lol


@dataclass
class SITDOptions(PerGameCommonOptions):
    goal: Goal
    gold_multi: GoldMultiplier
    xp_multi: XPMultiplier
    item_distribution: ItemDistribution
    useful_items: UsefulItems
    mimic_items: MimicItems
