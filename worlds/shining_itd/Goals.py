from typing import NamedTuple

from BaseClasses import CollectionState

from .Names import ItemName as I, RegionName


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
    GoalData(GOAL_DARK_SOL, {
        RegionName.Lab1,
        RegionName.Lab1Str, RegionName.Str, RegionName.StrRope, RegionName.StrCell,
        RegionName.Lab1Cou, RegionName.Cou, RegionName.CouCell,
        RegionName.Lab1Tru, RegionName.Tru, RegionName.TruIdol, RegionName.TruCell,
        RegionName.Wis, RegionName.WisCell,
        RegionName.Lab2, RegionName.Lab2Cell,
        RegionName.Lab3, RegionName.Lab3Rope, RegionName.Lab3RopeOrCell, RegionName.Lab3Cell,
        RegionName.Lab4, RegionName.Lab4Orb, RegionName.Lab4Cell,
        RegionName.Lab5,
    }, {I.DarkSol}, {
        I.RoyalTiara, I.DwarfKey, I.RuneKey, I.OrbOfTruth, I.FalseIdol, I.MysticRope, I.CellKey, I.Medallion, I.MagicRing, I.VialOfTears,
        I.TrialOfStrength, I.TrialOfCourage, I.TrialOfTruth, I.TrialOfWisdom,
        I.Gila, I.Dai, I.Jessa, I.EnterLab3,
        I.KaiserKrab, I.Tortolyde, I.Doppler, I.ShellBeast, I.DarkSol,
    }),
    GoalData(GOAL_TRIALS, {
        RegionName.Lab1,
        RegionName.Lab1Str, RegionName.Str,
        RegionName.Lab1Cou, RegionName.Cou,
        RegionName.Lab1Tru, RegionName.Tru, RegionName.TruIdol,
        RegionName.Wis,
    }, {I.TrialOfCourage, I.TrialOfStrength, I.TrialOfTruth, I.TrialOfWisdom}, {
        I.RoyalTiara, I.DwarfKey, I.RuneKey, I.OrbOfTruth, I.FalseIdol,
        I.TrialOfStrength, I.TrialOfCourage, I.TrialOfTruth, I.TrialOfWisdom,
        I.Gila, I.Dai,
        I.KaiserKrab, I.Tortolyde, I.Doppler,
    }),
    GoalData(GOAL_STRENGTH, {
        RegionName.Lab1,
        RegionName.Lab1Str, RegionName.Str,
    }, {I.TrialOfStrength}, {
        I.DwarfKey,
        I.TrialOfStrength,
        I.Gila,
        I.KaiserKrab,
    }),
]

goals_by_id = {goal.id: goal for goal in all_goals}


def get_goal_data(id: int):
    if id in goals_by_id:
        return goals_by_id[id]
    raise Exception(f'invalid goal id: {id}')
