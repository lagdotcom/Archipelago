from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

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


class StartingMeseta(Range):
    """
    How many mesetas you start the game with.
    """

    display_name = "Starting Meseta"
    default = 200
    range_start = 0
    range_end = 999999


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


class RandomiseTechs(Toggle):
    """
    Randomise the techs that each character learns. They will still learn them at the same levels.
    """

    display_name = "Randomise Techs"


ENCOUNTER_DOUBLE = 2
ENCOUNTER_NORMAL = 3
ENCOUNTER_HALF = 4
ENCOUNTER_QUARTER = 5
ENCOUNTER_EIGHTH = 6


class EncounterRate(Choice):
    display_name = "Encounter Rate"
    default = ENCOUNTER_HALF
    option_double = ENCOUNTER_DOUBLE
    option_normal = ENCOUNTER_NORMAL
    option_half = ENCOUNTER_HALF
    option_quarter = ENCOUNTER_QUARTER
    option_eighth = ENCOUNTER_EIGHTH


SPEED_NORMAL = 1
SPEED_DOUBLE = 2
SPEED_QUADRUPLE = 4


class MovementSpeed(Choice):
    display_name = "Movement Speed"
    default = SPEED_DOUBLE
    option_normal = SPEED_NORMAL
    option_double = SPEED_DOUBLE
    option_quadruple = SPEED_QUADRUPLE


@dataclass
class PhSt2Options(PerGameCommonOptions):
    goal: Goal
    starting_meseta: StartingMeseta
    item_distribution: ItemDistribution
    useful_items: UsefulItems
    randomise_techs: RandomiseTechs
    meseta_multi: MesetaMultiplier
    xp_multi: XPMultiplier
    encounter_rate: EncounterRate
    movement_speed: MovementSpeed


option_groups = [
    OptionGroup("Gameplay Options", [Goal, StartingMeseta]),
    OptionGroup("Randomisation", [ItemDistribution, UsefulItems, RandomiseTechs]),
    OptionGroup(
        "Quality of Life",
        [MesetaMultiplier, XPMultiplier, EncounterRate, MovementSpeed],
    ),
]

options_presets = {
    "vanilla": {
        "goal": GOAL_MOTHER_BRAIN,
        "starting_meseta": 200,
        "item_distribution": DIST_SHUFFLE,
        "useful_items": 0,
        "randomise_techs": 0,
        "meseta_multi": 1,
        "xp_multi": 1,
        "encounter_rate": ENCOUNTER_NORMAL,
        "movement_spped": SPEED_NORMAL,
    },
    "quick neifirst": {
        "goal": GOAL_NEIFIRST,
        "starting_meseta": 1000,
        "item_distribution": DIST_SHUFFLE,
        "useful_items": 0,
        "randomise_techs": 0,
        "meseta_multi": 3,
        "xp_multi": 5,
        "encounter_rate": ENCOUNTER_HALF,
        "movement_speed": SPEED_DOUBLE,
    },
}
