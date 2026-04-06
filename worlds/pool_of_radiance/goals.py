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


GOAL_TYRANTHRAXUS = 0
GOAL_SLUMS = 1

all_goals = [
    # GoalData(GOAL_TYRANTHRAXUS, {}, {}, []),
    GoalData(GOAL_SLUMS, {a.NewPhlan, a.Slums}, {i.SlumsCleared}, []),
]


goals_by_id = {goal.id: goal for goal in all_goals}


def get_goal_data(id: int):
    if id in goals_by_id:
        return goals_by_id[id]
    raise Exception(f"invalid goal id: {id}")
