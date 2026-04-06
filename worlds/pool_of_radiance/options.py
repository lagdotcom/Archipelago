from dataclasses import dataclass

from Options import (
    Choice,
    OptionGroup,
    PerGameCommonOptions,
    Range,
)

from .goals import GOAL_SLUMS, GOAL_TYRANTHRAXUS


class Goal(Choice):
    """
    Tyranthraxus: Finish the whole game.
    Slums: Clear the slums and get your reward from the clerk.
    """

    display_name = "Goal"
    default = GOAL_TYRANTHRAXUS
    option_tyranthraxus = GOAL_TYRANTHRAXUS
    option_slums = GOAL_SLUMS


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


class XPMultiplier(Range):
    """
    Multiplier applied to experience earned from battle.
    """

    display_name = "XP Multiplier"
    range_start = 1
    range_end = 100
    default = 2


@dataclass
class PROptions(PerGameCommonOptions):
    goal: Goal
    item_distribution: ItemDistribution
    xp_multi: XPMultiplier


option_groups = [
    OptionGroup("Gameplay Options", [Goal]),
    OptionGroup("Randomisation", [ItemDistribution]),
    OptionGroup("Quality of Life", [XPMultiplier]),
]

options_presets = {
    "vanilla": {
        "goal": GOAL_TYRANTHRAXUS,
        "item_distribution": DIST_SHUFFLE,
        "xp_multi": 1,
    },
    "quick slums": {
        "goal": GOAL_SLUMS,
        "item_distribution": DIST_SHUFFLE,
        "xp_multi": 2,
    },
}
