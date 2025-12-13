from enum import Enum
from typing import NamedTuple
from .Data import Tech as T


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
    power: int = 0


all_techs = [
    Tech(T.FOI, "FOI", 2, Effect.DAMAGE, power=15),
    Tech(T.GIFOI, "GIFOI", 6, Effect.DAMAGE, power=40),
    Tech(T.NAFOI, "NAFOI", 12, Effect.DAMAGE, power=130),
    Tech(T.ZAN, "ZAN", 4, Effect.DAMAGE, target=Target.GROUP, power=20),
    Tech(T.GIZAN, "GIZAN", 7, Effect.DAMAGE, target=Target.GROUP, power=30),
    Tech(T.NAZAN, "NAZAN", 11, Effect.DAMAGE, target=Target.GROUP, power=100),
    Tech(T.GRA, "GRA", 8, Effect.DAMAGE, target=Target.ALL, power=20),
    Tech(T.GIGRA, "GIGRA", 12, Effect.DAMAGE, target=Target.ALL, power=40),
    Tech(T.NAGRA, "NAGRA", 20, Effect.DAMAGE, target=Target.ALL, power=80),
    Tech(T.TSU, "TSU", 6, Effect.DAMAGE, power=30),
    Tech(T.GITHU, "GITHU", 13, Effect.DAMAGE, power=80),
    Tech(T.NATHU, "NATHU", 20, Effect.DAMAGE, power=150),
    Tech(T.SHIFT, "SHIFT", 5, Effect.ATTACK_UP, success_rate=255, power=20),
    Tech(T.FANBI, "FANBI", 2, Effect.DRAIN, Only.BIO, success_rate=255, power=10),
    Tech(
        T.EIJIA,
        "EIJIA",
        4,
        Effect.DAMAGE,
        Only.MECH,
        Target.GROUP,
        success_rate=255,
        power=23,
    ),
    Tech(T.BROSE, "BROSE", 8, Effect.KILL, Only.MECH, success_rate=127, power=500),
    Tech(T.CONTE, "CONTE", 6, Effect.FREEZE, Only.MECH, success_rate=255),
    Tech(T.GAJ, "GAJ", 1, Effect.DAMAGE, Only.MECH, success_rate=255, power=20),
    Tech(T.GIGAJ, "GIGAJ", 5, Effect.DAMAGE, Only.MECH, power=60),
    Tech(T.NAGAJ, "NAGAJ", 15, Effect.DAMAGE, Only.MECH, power=150),
    Tech(T.SAG, "SAG", 3, Effect.DAMAGE, Only.MECH, Target.ALL, power=20),
    Tech(T.GISAG, "GISAG", 15, Effect.DAMAGE, Only.MECH, Target.ALL, power=60),
    Tech(T.NASAG, "NASAG", 27, Effect.DAMAGE, Only.MECH, Target.ALL, power=150),
    Tech(T.GEN, "GEN", 1, Effect.DAMAGE, Only.BIO, power=20),
    Tech(T.SAGEN, "SAGEN", 3, Effect.DAMAGE, Only.BIO, Target.ALL, power=20),
    Tech(T.VOL, "VOL", 8, Effect.KILL, Only.BIO, success_rate=153, power=500),
    Tech(
        T.SAVOL,
        "SAVOL",
        16,
        Effect.KILL,
        Only.MECH,
        Target.GROUP,
        success_rate=178,
        power=500,
    ),
    Tech(T.SHIZA, "SHIZA", 6, Effect.FREEZE, Only.BIO, success_rate=255),
    Tech(T.DORAN, "DORAN", 2, Effect.CONFUSE, Only.BIO, success_rate=204),
    Tech(T.RIMIT, "RIMIT", 3, Effect.PARALYSIS, Only.BIO, success_rate=127),
    Tech(T.SHINB, "SHINB", 4, Effect.TERRIFY, Only.BIO, success_rate=255),
    Tech(T.FORSA, "FORSA", 1, Effect.CONFUSE, Only.MECH, success_rate=127),
    Tech(T.RIMET, "RIMET", 3, Effect.PARALYSIS, Only.MECH, success_rate=102),
    Tech(T.SHU, "SHU", 3, Effect.DEFENCE_UP, success_rate=255),
    Tech(T.SASHU, "SASHU", 8, Effect.DEFENCE_UP, target=Target.ALL, success_rate=255),
    Tech(
        T.DEBAN, "DEBAN", 4, Effect.ACCURACY_DOWN, target=Target.ALL, success_rate=255
    ),
    Tech(T.NER, "NER", 2, Effect.AGILITY_UP, success_rate=255),
    Tech(T.SANER, "SANER", 6, Effect.AGILITY_UP, target=Target.ALL, success_rate=255),
    Tech(T.RES, "RES", 3, Effect.HEAL, map=True, success_rate=255, power=20),
    Tech(T.GIRES, "GIRES", 7, Effect.HEAL, map=True, success_rate=255, power=60),
    Tech(T.NARES, "NARES", 13, Effect.HEAL, map=True, success_rate=255, power=500),
    Tech(
        T.SAR,
        "SAR",
        13,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=20,
    ),
    Tech(
        T.GISAR,
        "GISAR",
        29,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=60,
    ),
    Tech(
        T.NASAR,
        "NASAR",
        53,
        Effect.HEAL,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(T.SAK, "SAK", 1, Effect.SACRIFICE, map=True, success_rate=255, power=500),
    Tech(
        T.NASAK,
        "NASAK",
        1,
        Effect.SACRIFICE,
        target=Target.ALL,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(T.ANTI, "ANTI", 2, Effect.ANTIDOTE, battle=False, map=True, success_rate=255),
    Tech(
        T.REVER, "REVER", 30, Effect.REVIVIFY, battle=False, map=True, success_rate=255
    ),
    Tech(
        T.RYUKA,
        "RYUKA",
        8,
        Effect.TOWN_TELEPORT,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(
        T.HINAS,
        "HINAS",
        8,
        Effect.LEAVE_DUNGEON,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(T.MUSIK, "MUSIK", 3, Effect.MUSIK, success_rate=255),
    Tech(T.MEGID, "MEGID", 55, Effect.MEGID, success_rate=255),
]

techs_by_id = {tech.id: tech for tech in all_techs}
techs_by_name = {tech.name: tech for tech in all_techs}


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

total_normal_tech_pool: list[int] = []
total_map_tech_pool: list[int] = []
total_battle_tech_pool: list[int] = []
total_map_techs: dict[str, int] = {}
total_battle_techs: dict[str, int] = {}
for char_name, learn_set in learn_lists.items():
    battle_count = 0
    map_count = 0
    for name in learn_set:
        tech = techs_by_name[name]
        total_normal_tech_pool.append(tech.id)
        if tech.battle:
            battle_count += 1
            total_battle_tech_pool.append(tech.id)
        if tech.map:
            map_count += 1
            total_map_tech_pool.append(tech.id)
    total_battle_techs[char_name] = battle_count
    total_map_techs[char_name] = map_count

tech_strengths: dict[int, int] = {
    # Tier 1
    T.RES: 10_00,
    T.FOI: 10_01,
    T.GAJ: 10_02,
    T.GEN: 10_03,
    T.FANBI: 10_04,
    T.RIMET: 10_05,
    T.RIMIT: 10_06,
    T.SHU: 10_07,
    # Tier 1.5
    T.SAR: 15_00,
    T.ANTI: 15_01,
    T.SAK: 15_02,
    T.TSU: 15_03,
    T.EIJIA: 15_04,
    T.SHINB: 15_05,
    T.HINAS: 15_06,
    # Tier 2
    T.GIRES: 20_00,
    T.GIGAJ: 20_01,
    T.ZAN: 20_02,
    T.SAG: 20_03,
    T.SAGEN: 20_04,
    T.GIFOI: 20_05,
    T.FORSA: 20_06,
    T.DORAN: 20_07,
    T.RYUKA: 20_08,
    T.NER: 20_10,
    T.SASHU: 20_11,
    # Tier 2.5
    T.GISAR: 25_00,
    T.GRA: 25_01,
    T.GITHU: 25_02,
    T.SHIFT: 25_03,
    # Tier 3
    T.GIZAN: 30_00,
    T.NAFOI: 30_01,
    T.NAGAJ: 30_02,
    T.GIGRA: 30_03,
    T.GISAG: 30_04,
    T.CONTE: 30_05,
    T.SHIZA: 30_06,
    # Tier 3.5
    T.NASAK: 35_00,
    T.NATHU: 35_01,
    # Tier 4
    T.REVER: 40_00,
    T.NARES: 40_01,
    T.BROSE: 40_02,
    T.VOL: 40_03,
    T.SANER: 40_05,
    T.DEBAN: 40_06,
    # Tier 4.5
    T.NAZAN: 45_00,
    T.NASAG: 45_01,
    T.NAGRA: 45_02,
    T.SAVOL: 45_03,
    # Tier 5
    T.NASAR: 50_00,
    T.MEGID: 50_01,
}
