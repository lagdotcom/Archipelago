from functools import reduce
from random import Random

from .characters import Char, Nei, vanilla_characters
from .techs import tech_strengths, techs_by_name


def get_tech_pools(chars: list[Char]):
    total_normal_tech_pool: list[int] = []
    map_pool: list[int] = []
    battle_pool: list[int] = []
    map_counts: dict[str, int] = {}
    battle_counts: dict[str, int] = {}
    for char in chars:
        battle_count = 0
        map_count = 0
        for name in char.get_tech_learn_set():
            tech = techs_by_name[name]
            total_normal_tech_pool.append(tech.id)
            if tech.battle:
                battle_count += 1
                battle_pool.append(tech.id)
            if tech.map:
                map_count += 1
                map_pool.append(tech.id)
        if battle_count > 16:
            raise Exception(f"{char.name} has too many battle techs")
        if map_count > 16:
            raise Exception(f"{char.name} has too many map techs")
        battle_counts[char.name] = battle_count
        map_counts[char.name] = map_count
    return map_counts, map_pool, battle_counts, battle_pool


def _share(random: Random, pool: list[int], counts: dict[str, int]):
    choices: dict[str, list[int]] = {name: [] for name in counts}

    def remaining(name: str):
        return counts[name] - len(choices[name])

    # assign in frequency order so we don't get stuck
    tech_freq = {id: pool.count(id) for id in set(pool)}
    tech_ids = sorted(pool, key=lambda id: tech_freq[id], reverse=True)
    for id in tech_ids:
        valid = [name for name in choices if id not in choices[name] and remaining(name) > 0]
        name = reduce(lambda x, y: x if remaining(x) >= remaining(y) else y, valid)
        choices[name].append(id)

    return choices


def map_tech_id_to_strength(id: int):
    return tech_strengths[id]


def get_random_tech_choices(random: Random, chars: list[Char], sensible: bool):
    map_counts, map_pool, battle_counts, battle_pool = get_tech_pools(chars)
    map_techs = _share(random, map_pool, map_counts)
    battle_techs = _share(random, battle_pool, battle_counts)
    if sensible:
        for tech_list in map_techs.values():
            tech_list.sort(key=map_tech_id_to_strength)
        for tech_list in battle_techs.values():
            tech_list.sort(key=map_tech_id_to_strength)
    else:
        for tech_list in map_techs.values():
            random.shuffle(tech_list)
        for tech_list in battle_techs.values():
            random.shuffle(tech_list)
    return map_techs, battle_techs


def get_random_char_order(random: Random, except_nei: bool):
    chars = vanilla_characters[:]
    random.shuffle(chars)
    if except_nei:
        if Nei not in chars:
            raise Exception("Nei not in list but has to be second!")
        chars.remove(Nei)
        chars.insert(1, Nei)
    return chars
