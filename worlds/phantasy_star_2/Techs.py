from enum import Enum
from typing import NamedTuple


class Effect(Enum):
    ACCURACY_DOWN = 0
    AGILITY_UP = 1
    ANTIDOTE = 2
    ATTACK_UP = 3
    CONFUSE = 4
    DAMAGE = 5
    DEFENCE_UP = 6
    DRAIN = 7
    FREEZE = 8
    HEAL = 9
    KILL = 10
    LEAVE_DUNGEON = 11
    MEGID = 12
    MUSIK = 13
    PARALYSIS = 14
    REVIVIFY = 15
    SACRIFICE = 16
    TERRIFY = 17
    TOWN_TELEPORT = 18


class Target(Enum):
    SINGLE = 0
    GROUP = 1
    ALL = 2


class Only(Enum):
    NONE = 0
    BIO = 1
    MECH = 2


class Tech(NamedTuple):
    id: int
    name: str
    tp: int
    effect: Effect
    only: Only = Only.NONE
    target: Target = Target.SINGLE
    battle: bool = True
    map: bool = False
    success_rate: int = 229
    power: int = 0  # btw, 255 actually = 500


all_techs = [
    Tech(1, "FOI", 2, Effect.DAMAGE, power=15),
    Tech(2, "GIFOI", 6, Effect.DAMAGE, power=40),
    Tech(3, "NAFOI", 12, Effect.DAMAGE, power=130),
    Tech(4, "ZAN", 4, Effect.DAMAGE, target=Target.GROUP, power=20),
    Tech(5, "GIZAN", 7, Effect.DAMAGE, target=Target.GROUP, power=30),
    Tech(6, "NAZAN", 11, Effect.DAMAGE, target=Target.GROUP, power=100),
    Tech(7, "GRA", 8, Effect.DAMAGE, target=Target.ALL, power=20),
    Tech(8, "GIGRA", 12, Effect.DAMAGE, target=Target.ALL, power=40),
    Tech(9, "NAGRA", 20, Effect.DAMAGE, target=Target.ALL, power=80),
    Tech(10, "TSU", 6, Effect.DAMAGE, power=30),
    Tech(11, "GITHU", 13, Effect.DAMAGE, power=80),
    Tech(12, "NATHU", 20, Effect.DAMAGE, power=150),
    Tech(13, "SHIFT", 5, Effect.ATTACK_UP, success_rate=255, power=20),
    Tech(14, "FANBI", 2, Effect.DRAIN, Only.BIO, success_rate=255, power=10),
    Tech(
        15,
        "EIJIA",
        4,
        Effect.DAMAGE,
        Only.MECH,
        Target.GROUP,
        success_rate=255,
        power=23,
    ),
    Tech(16, "BROSE", 8, Effect.KILL, Only.MECH, success_rate=127, power=255),
    Tech(17, "CONTE", 6, Effect.FREEZE, Only.MECH, success_rate=255),
    Tech(18, "GAJ", 1, Effect.DAMAGE, Only.MECH, success_rate=255, power=20),
    Tech(19, "GIGAJ", 5, Effect.DAMAGE, Only.MECH, power=60),
    Tech(20, "NAGAJ", 15, Effect.DAMAGE, Only.MECH, power=150),
    Tech(21, "SAG", 3, Effect.DAMAGE, Only.MECH, Target.ALL, power=20),
    Tech(22, "GISAG", 15, Effect.DAMAGE, Only.MECH, Target.ALL, power=60),
    Tech(23, "NASAG", 27, Effect.DAMAGE, Only.MECH, Target.ALL, power=150),
    Tech(24, "GEN", 1, Effect.DAMAGE, Only.BIO, power=20),
    Tech(25, "SAGEN", 3, Effect.DAMAGE, Only.BIO, Target.ALL, power=20),
    Tech(26, "VOL", 8, Effect.KILL, Only.BIO, success_rate=153, power=255),
    Tech(
        27,
        "SAVOL",
        16,
        Effect.KILL,
        Only.MECH,
        Target.GROUP,
        success_rate=178,
        power=255,
    ),
    Tech(28, "SHIZA", 6, Effect.FREEZE, Only.BIO, success_rate=255),
    Tech(29, "DORAN", 2, Effect.CONFUSE, Only.BIO, success_rate=204),
    Tech(30, "RIMIT", 3, Effect.PARALYSIS, Only.BIO, success_rate=127),
    Tech(31, "SHINB", 4, Effect.TERRIFY, Only.BIO, success_rate=255),
    Tech(32, "FORSA", 1, Effect.CONFUSE, Only.MECH, success_rate=127),
    Tech(33, "RIMET", 3, Effect.PARALYSIS, Only.MECH, success_rate=102),
    Tech(34, "SHU", 3, Effect.DEFENCE_UP, success_rate=255),
    Tech(35, "SASHU", 8, Effect.DEFENCE_UP, target=Target.ALL, success_rate=255),
    Tech(36, "DEBAN", 4, Effect.ACCURACY_DOWN, target=Target.ALL, success_rate=255),
    Tech(37, "NER", 2, Effect.AGILITY_UP, success_rate=255),
    Tech(38, "SANER", 6, Effect.AGILITY_UP, target=Target.ALL, success_rate=255),
    Tech(39, "RES", 3, Effect.HEAL, map=True, success_rate=255, power=20),
    Tech(40, "GIRES", 7, Effect.HEAL, map=True, success_rate=255, power=60),
    Tech(41, "NARES", 13, Effect.HEAL, map=True, success_rate=255, power=255),
    Tech(
        42,
        "SAR",
        13,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=20,
    ),
    Tech(
        43,
        "GISAR",
        29,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=60,
    ),
    Tech(
        44,
        "NASAR",
        53,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=255,
    ),
    Tech(45, "SAK", 1, Effect.SACRIFICE, map=True, success_rate=255, power=255),
    Tech(
        46,
        "NASAK",
        1,
        Effect.SACRIFICE,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=255,
    ),
    Tech(47, "ANTI", 2, Effect.ANTIDOTE, battle=False, map=True, success_rate=255),
    Tech(48, "REVER", 30, Effect.REVIVIFY, battle=False, map=True, success_rate=255),
    Tech(
        49, "RYUKA", 8, Effect.TOWN_TELEPORT, battle=False, map=True, success_rate=255
    ),
    Tech(
        50, "HINAS", 8, Effect.LEAVE_DUNGEON, battle=False, map=True, success_rate=255
    ),
    Tech(51, "MUSIK", 3, Effect.MUSIK, success_rate=255),
    Tech(52, "MEGID", 55, Effect.MEGID, success_rate=255),
]

techs_by_name = {tech.name: tech for tech in all_techs}

character_names = ["Rolf", "Nei", "Rudolf", "Amy", "Hugh", "Anna", "Kain", "Shir"]


learn_lists: dict[str, dict[str, int]] = {
    "Rolf": {
        "FOI": 1,
        "RYUKA": 4,
        "GIFOI": 5,
        "TSU": 5,
        "HINAS": 7,
        "ZAN": 7,
        "RES": 8,
        "GRA": 10,
        "GITHU": 11,
        "NAFOI": 14,
        "GIRES": 16,
        "GIZAN": 16,
        "NATHU": 20,
        "NAZAN": 24,
        "GIGRA": 27,
        "REVER": 30,
        "MEGID": 35,
        "NAGRA": 40,
    },
    "Nei": {
        "RES": 1,
        "ANTI": 16,
        "SAK": 20,
        "NASAK": 24,
    },
    "Rudolf": {},
    "Amy": {
        "RES": 1,
        "SHU": 2,
        "SAR": 9,
        "DEBAN": 4,
        "ANTI": 5,
        "FOI": 5,
        "GIRES": 6,
        "SAK": 10,
        "NASAK": 12,
        "NARES": 15,
        "SASHU": 15,
        "SANER": 25,
        "GISAR": 27,
        "REVER": 27,
        "NASAR": 30,
        "GRA": 40,
        "GIGRA": 50,
    },
    "Hugh": {
        "RIMIT": 2,
        "DORAN": 3,
        "GEN": 3,
        "SAGEN": 5,
        "SHINB": 5,
        "SHIZA": 6,
        "FOI": 9,
        "GIFOI": 12,
        "VOL": 15,
        "ZAN": 18,
        "SAVOL": 24,
        "GRA": 27,
        "GIRES": 30,
        "GIGRA": 33,
        "GIZAN": 36,
    },
    "Anna": {
        "FOI": 1,
        "NER": 5,
        "SHIFT": 8,
        "FANBI": 16,
        "ZAN": 32,
    },
    "Kain": {
        "FOI": 1,
        "FORSA": 1,
        "EIJIA": 4,
        "GAJ": 7,
        "RIMET": 7,
        "CONTE": 9,
        "GIGAJ": 10,
        "ZAN": 10,
        "SAG": 13,
        "GRA": 14,
        "NAGAJ": 17,
        "GISAG": 21,
        "BROSE": 26,
        "NASAG": 28,
        "GIZAN": 31,
    },
    "Shir": {
        "FOI": 1,
        "RYUKA": 6,
        "HINAS": 9,
        "RES": 12,
        "GIFOI": 15,
        "ZAN": 18,
        "GRA": 24,
        "GIZAN": 27,
        "GIRES": 30,
        "NAZAN": 33,
        "GIGRA": 36,
        "NAGRA": 45,
    },
}

total_normal_tech_pool: list[str] = []
total_map_techs: dict[str, int] = {}
total_battle_techs: dict[str, int] = {}
for char_name, learn_set in learn_lists.items():
    battle_count = 0
    map_count = 0
    for name in learn_set:
        total_normal_tech_pool.append(name)
        tech = techs_by_name[name]
        if tech.battle:
            battle_count += 1
        if tech.map:
            map_count += 1
    total_battle_techs[char_name] = battle_count
    total_map_techs[char_name] = map_count
