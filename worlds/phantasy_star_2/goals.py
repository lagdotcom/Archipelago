from typing import NamedTuple

from BaseClasses import CollectionState

from .Data import area_name as a
from .Data import item_name as i


class GoalData(NamedTuple):
    id: int
    region_names: set[str]
    completion_item_names: set[str]
    required_item_names: list[str]

    def has_region(self, name: str):
        return name in self.region_names

    def get_completion_function(self, player: int):
        def check_all(state: CollectionState):
            return state.has_all(self.completion_item_names, player)

        return check_all


GOAL_MOTHER_BRAIN = 0
GOAL_NEIFIRST = 1


all_goals = [
    GoalData(
        GOAL_MOTHER_BRAIN,
        {
            a.Motavia,
            a.Shure,
            a.ShureLockedChests,
            a.Nido,
            a.Oputa,
            a.BioSystemsLab,
            a.BioSystemsLabBasement,
            a.Roron,
            a.Kueri,
            a.MotavianWater,
            a.Uzo,
            a.Climatrol,
            a.ControlTower,
            a.RedDam,
            a.YellowDam,
            a.BlueDam,
            a.GreenDam,
            a.Gaira,
            a.Dezolis,
            a.DezolisDungeons,
            a.Noah,
        },
        {i.WinTheGameFlag},
        [
            i.SmallKey,
            i.Letter,
            i.Dynamite,
            i.Teim,
            i.Dynamite,
            i.Dynamite,
            i.Recorder,
            i.KeyTube,
            i.JetScooterFlag,
            i.MarueraLeaf,
            i.MarueraGum,
            i.NeifirstFlag,
            i.MusikFlag,
            i.RedCard,
            i.YellowCard,
            i.BlueCard,
            i.GreenCard,
            i.RedDamFlag,
            i.YellowDamFlag,
            i.BlueDamFlag,
            i.GreenDamFlag,
            i.SpaceshipFlag,
            i.Prism,
            i.NeiCrown,
            i.NeiMet,
            i.NeiShot,
            i.NeiSlasher,
            i.NeiCape,
            i.NeiArmor,
            i.NeiShield,
            i.NeiEmel,
            i.NeiSword,
            i.WinTheGameFlag,
        ],
    ),
    GoalData(
        GOAL_NEIFIRST,
        {
            a.Motavia,
            a.Shure,
            a.ShureLockedChests,
            a.Nido,
            # A.Oputa, no need to learn MUSIK
            a.BioSystemsLab,
            a.BioSystemsLabBasement,
            a.Roron,
            a.Kueri,
            a.MotavianWater,
            a.Uzo,
            a.Climatrol,
        },
        {i.NeifirstFlag},
        [
            i.SmallKey,
            i.Letter,
            i.Dynamite,
            i.Teim,
            i.Dynamite,
            i.Dynamite,
            i.Recorder,
            i.KeyTube,
            i.JetScooterFlag,
            i.MarueraLeaf,
            i.MarueraGum,
            i.NeifirstFlag,
        ],
    ),
]


goals_by_id = {goal.id: goal for goal in all_goals}


def get_goal_data(id: int):
    if id in goals_by_id:
        return goals_by_id[id]
    raise Exception(f"invalid goal id: {id}")
