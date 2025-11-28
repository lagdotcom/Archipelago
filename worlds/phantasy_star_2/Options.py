from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice

from .Goals import GOAL_MOTHER_BRAIN, GOAL_NEIFIRST


class Goal(Choice):
    """
    Mother Brain: Finish the whole game.
    Neifirst: Beat Neifirst at Climatrol.
    """

    display_name = "Goal"
    default = GOAL_MOTHER_BRAIN
    option_mother_brain = GOAL_MOTHER_BRAIN
    option_neifirst = GOAL_NEIFIRST


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
    (only applies to Item Distribution = Rando)
    Percentage of items in the pool that are 'useful'.
    """

    display_name = "Useful Items"
    range_start = 0
    range_end = 100
    default = 75


@dataclass
class PhSt2Options(PerGameCommonOptions):
    goal: Goal
    meseta_multi: MesetaMultiplier
    xp_multi: XPMultiplier
    item_distribution: ItemDistribution
    useful_items: UsefulItems
