from typing import NamedTuple

from BaseClasses import CollectionState

from .Names import item_name as i
from .Names import region_name


class GoalData(NamedTuple):
    id: int
    region_names: set[str]
    completion_item_names: set[str]
    required_item_names: set[str]

    def has_region(self, name: str):
        return name in self.region_names

    def get_completion_function(self, player: int):
        def check_all(state: CollectionState):
            return state.has_all(self.completion_item_names, player)

        return check_all


GOAL_DARK_SOL = 0
GOAL_TRIALS = 1
GOAL_STRENGTH = 2

all_goals = [
    GoalData(
        GOAL_DARK_SOL,
        {
            region_name.Lab1,
            region_name.Lab1Str,
            region_name.Str,
            region_name.StrRope,
            region_name.StrCell,
            region_name.Lab1Cou,
            region_name.Cou,
            region_name.CouCell,
            region_name.Lab1Tru,
            region_name.Tru,
            region_name.TruIdol,
            region_name.TruCell,
            region_name.Wis,
            region_name.WisCell,
            region_name.Lab2,
            region_name.Lab2Cell,
            region_name.Lab3,
            region_name.Lab3Rope,
            region_name.Lab3RopeOrCell,
            region_name.Lab3Cell,
            region_name.Lab4,
            region_name.Lab4Orb,
            region_name.Lab4Cell,
            region_name.Lab5,
        },
        {i.DarkSol},
        {
            i.RoyalTiara,
            i.DwarfKey,
            i.RuneKey,
            i.OrbOfTruth,
            i.FalseIdol,
            i.MysticRope,
            i.CellKey,
            i.Medallion,
            i.MagicRing,
            i.VialOfTears,
            i.TrialOfStrength,
            i.TrialOfCourage,
            i.TrialOfTruth,
            i.TrialOfWisdom,
            i.Gila,
            i.Dai,
            i.Jessa,
            i.EnterLab3,
            # i.KaiserKrab,
            # i.Tortolyde,
            # i.Doppler,
            # i.ShellBeast,
            # i.DarkSol,
        },
    ),
    GoalData(
        GOAL_TRIALS,
        {
            region_name.Lab1,
            region_name.Lab1Str,
            region_name.Str,
            region_name.Lab1Cou,
            region_name.Cou,
            region_name.Lab1Tru,
            region_name.Tru,
            region_name.TruIdol,
            region_name.Wis,
        },
        {i.TrialOfCourage, i.TrialOfStrength, i.TrialOfTruth, i.TrialOfWisdom},
        {
            i.RoyalTiara,
            i.DwarfKey,
            i.RuneKey,
            i.OrbOfTruth,
            i.FalseIdol,
            i.TrialOfStrength,
            i.TrialOfCourage,
            i.TrialOfTruth,
            i.TrialOfWisdom,
            i.Gila,
            i.Dai,
            # i.KaiserKrab,
            # i.Tortolyde,
            # i.Doppler,
        },
    ),
    GoalData(
        GOAL_STRENGTH,
        {
            region_name.Lab1,
            region_name.Lab1Str,
            region_name.Str,
        },
        {i.TrialOfStrength},
        {
            i.DwarfKey,
            i.TrialOfStrength,
            i.Gila,
            # i.KaiserKrab,
        },
    ),
]

goals_by_id = {goal.id: goal for goal in all_goals}


def get_goal_data(id: int):
    if id in goals_by_id:
        return goals_by_id[id]
    raise Exception(f"invalid goal id: {id}")
