from functools import reduce
from random import Random

from .Techs import (
    tech_strengths,
    total_battle_tech_pool,
    total_battle_techs,
    total_map_tech_pool,
    total_map_techs,
)


def _share(random: Random, pool: list[int], counts: dict[str, int]):
    choices: dict[str, list[int]] = {name: [] for name in counts}

    def remaining(name: str):
        return counts[name] - len(choices[name])

    random.shuffle(pool)
    for id in pool:
        valid = [name for name in choices if id not in choices[name]]
        name = reduce(lambda x, y: x if remaining(x) >= remaining(y) else y, valid)
        choices[name].append(id)

    return choices


def map_tech_id_to_strength(id: int):
    return tech_strengths[id]


def get_random_tech_choices(random: Random, sensible: bool):
    map_techs = _share(random, total_map_tech_pool, total_map_techs)
    battle_techs = _share(random, total_battle_tech_pool, total_battle_techs)
    if sensible:
        for tech_list in map_techs.values():
            tech_list.sort(key=map_tech_id_to_strength)
        for tech_list in battle_techs.values():
            tech_list.sort(key=map_tech_id_to_strength)
    return map_techs, battle_techs
