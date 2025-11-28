from typing import NamedTuple

from BaseClasses import CollectionState

from .Data import Area as A, Item as I


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
            A.Motavia,
            A.Shure,
            A.ShureLockedChests,
            A.Nido,
            A.Oputa,
            A.BioSystemsLab,
            A.BioSystemsLabBasement,
            A.Roron,
            A.Kueri,
            A.Uzo,
            A.Climatrol,
            A.MotaviaAfterNeifirst,
            A.ControlTower,
            A.RedDam,
            A.YellowDam,
            A.BlueDam,
            A.GreenDam,
            A.Gaira,
            A.Dezolis,
            A.DezolisDungeons,
            A.Noah,
        },
        {I.WinTheGameFlag},
        [
            I.SmallKey,
            I.Letter,
            I.Dynamite,
            I.Teim,
            I.Dynamite,
            I.Dynamite,
            I.Recorder,
            I.KeyTube,
            I.JetScooterFlag,
            I.MarueraLeaf,
            I.MarueraGum,
            I.NeifirstFlag,
            I.MusikFlag,
            I.RedCard,
            I.YellowCard,
            I.BlueCard,
            I.GreenCard,
            I.RedDamFlag,
            I.YellowDamFlag,
            I.BlueDamFlag,
            I.GreenDamFlag,
            I.SpaceshipFlag,
            I.Prism,
            I.NeiCrown,
            I.NeiMet,
            I.NeiShot,
            I.NeiSlasher,
            I.NeiCape,
            I.NeiArmor,
            I.NeiShield,
            I.NeiEmel,
            I.NeiSword,
            I.WinTheGameFlag,
        ],
    ),
    GoalData(
        GOAL_NEIFIRST,
        {
            A.Motavia,
            A.Shure,
            A.ShureLockedChests,
            A.Nido,
            # A.Oputa, no need to learn MUSIK
            A.BioSystemsLab,
            A.BioSystemsLabBasement,
            A.Roron,
            A.Kueri,
            A.Uzo,
            A.Climatrol,
        },
        {I.NeifirstFlag},
        [
            I.SmallKey,
            I.Letter,
            I.Dynamite,
            I.Teim,
            I.Dynamite,
            I.Dynamite,
            I.Recorder,
            I.KeyTube,
            I.JetScooterFlag,
            I.MarueraLeaf,
            I.MarueraGum,
            I.NeifirstFlag,
        ],
    ),
]


goals_by_id = {goal.id: goal for goal in all_goals}


def get_goal_data(id: int):
    if id in goals_by_id:
        return goals_by_id[id]
    raise Exception(f"invalid goal id: {id}")
