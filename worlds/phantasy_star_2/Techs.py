from enum import Enum
from typing import NamedTuple
from .Data import TechID as T


class Effect(Enum):
    AccuracyDown = 0
    AgilityUp = 1
    Antidote = 2
    AttackUp = 3
    Confuse = 4
    Damage = 5
    DefenceUp = 6
    Drain = 7
    Freeze = 8
    Heal = 9
    Kill = 10
    LeaveDungeon = 11
    Megid = 12
    Musik = 13
    Paralysis = 14
    Revive = 15
    Sacrifice = 16
    Terrify = 17
    TownTeleport = 18


class Target(Enum):
    Single = 0
    Group = 1
    All = 2


class Filter(Enum):
    All = 0
    Bio = 1
    Mech = 2


class Tech(NamedTuple):
    id: int
    name: str
    tp: int
    effect: Effect
    filter: Filter = Filter.All
    target: Target = Target.Single
    battle: bool = True
    map: bool = False
    success_rate: int = 229
    power: int = 0


all_techs = [
    Tech(T.FOI, "FOI", 2, Effect.Damage, power=15),
    Tech(T.GIFOI, "GIFOI", 6, Effect.Damage, power=40),
    Tech(T.NAFOI, "NAFOI", 12, Effect.Damage, power=130),
    Tech(T.ZAN, "ZAN", 4, Effect.Damage, target=Target.Group, power=20),
    Tech(T.GIZAN, "GIZAN", 7, Effect.Damage, target=Target.Group, power=30),
    Tech(T.NAZAN, "NAZAN", 11, Effect.Damage, target=Target.Group, power=100),
    Tech(T.GRA, "GRA", 8, Effect.Damage, target=Target.All, power=20),
    Tech(T.GIGRA, "GIGRA", 12, Effect.Damage, target=Target.All, power=40),
    Tech(T.NAGRA, "NAGRA", 20, Effect.Damage, target=Target.All, power=80),
    Tech(T.TSU, "TSU", 6, Effect.Damage, power=30),
    Tech(T.GITHU, "GITHU", 13, Effect.Damage, power=80),
    Tech(T.NATHU, "NATHU", 20, Effect.Damage, power=150),
    Tech(T.SHIFT, "SHIFT", 5, Effect.AttackUp, success_rate=255, power=20),
    Tech(T.FANBI, "FANBI", 2, Effect.Drain, Filter.Bio, success_rate=255, power=10),
    Tech(
        T.EIJIA,
        "EIJIA",
        4,
        Effect.Damage,
        Filter.Mech,
        Target.Group,
        success_rate=255,
        power=23,
    ),
    Tech(T.BROSE, "BROSE", 8, Effect.Kill, Filter.Mech, success_rate=127, power=500),
    Tech(T.CONTE, "CONTE", 6, Effect.Freeze, Filter.Mech, success_rate=255),
    Tech(T.GAJ, "GAJ", 1, Effect.Damage, Filter.Mech, success_rate=255, power=20),
    Tech(T.GIGAJ, "GIGAJ", 5, Effect.Damage, Filter.Mech, power=60),
    Tech(T.NAGAJ, "NAGAJ", 15, Effect.Damage, Filter.Mech, power=150),
    Tech(T.SAG, "SAG", 3, Effect.Damage, Filter.Mech, Target.All, power=20),
    Tech(T.GISAG, "GISAG", 15, Effect.Damage, Filter.Mech, Target.All, power=60),
    Tech(T.NASAG, "NASAG", 27, Effect.Damage, Filter.Mech, Target.All, power=150),
    Tech(T.GEN, "GEN", 1, Effect.Damage, Filter.Bio, power=20),
    Tech(T.SAGEN, "SAGEN", 3, Effect.Damage, Filter.Bio, Target.All, power=20),
    Tech(T.VOL, "VOL", 8, Effect.Kill, Filter.Bio, success_rate=153, power=500),
    Tech(
        T.SAVOL,
        "SAVOL",
        16,
        Effect.Kill,
        Filter.Bio,
        Target.Group,
        success_rate=178,
        power=500,
    ),
    Tech(T.SHIZA, "SHIZA", 6, Effect.Freeze, Filter.Bio, success_rate=255),
    Tech(T.DORAN, "DORAN", 2, Effect.Confuse, Filter.Bio, success_rate=204),
    Tech(T.RIMIT, "RIMIT", 3, Effect.Paralysis, Filter.Bio, success_rate=127),
    Tech(T.SHINB, "SHINB", 4, Effect.Terrify, Filter.Bio, success_rate=255),
    Tech(T.FORSA, "FORSA", 1, Effect.Confuse, Filter.Mech, success_rate=127),
    Tech(T.RIMET, "RIMET", 3, Effect.Paralysis, Filter.Mech, success_rate=102),
    Tech(T.SHU, "SHU", 3, Effect.DefenceUp, success_rate=255),
    Tech(T.SASHU, "SASHU", 8, Effect.DefenceUp, target=Target.All, success_rate=255),
    Tech(T.DEBAN, "DEBAN", 4, Effect.AccuracyDown, target=Target.All, success_rate=255),
    Tech(T.NER, "NER", 2, Effect.AgilityUp, success_rate=255),
    Tech(T.SANER, "SANER", 6, Effect.AgilityUp, target=Target.All, success_rate=255),
    Tech(T.RES, "RES", 3, Effect.Heal, map=True, success_rate=255, power=20),
    Tech(T.GIRES, "GIRES", 7, Effect.Heal, map=True, success_rate=255, power=60),
    Tech(T.NARES, "NARES", 13, Effect.Heal, map=True, success_rate=255, power=500),
    Tech(
        T.SAR,
        "SAR",
        13,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=20,
    ),
    Tech(
        T.GISAR,
        "GISAR",
        29,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=60,
    ),
    Tech(
        T.NASAR,
        "NASAR",
        53,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(T.SAK, "SAK", 1, Effect.Sacrifice, map=True, success_rate=255, power=500),
    Tech(
        T.NASAK,
        "NASAK",
        1,
        Effect.Sacrifice,
        target=Target.All,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(T.ANTI, "ANTI", 2, Effect.Antidote, battle=False, map=True, success_rate=255),
    Tech(T.REVER, "REVER", 30, Effect.Revive, battle=False, map=True, success_rate=255),
    Tech(
        T.RYUKA,
        "RYUKA",
        8,
        Effect.TownTeleport,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(
        T.HINAS,
        "HINAS",
        4,
        Effect.LeaveDungeon,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(T.MUSIK, "MUSIK", 3, Effect.Musik, success_rate=255),
    Tech(T.MEGID, "MEGID", 55, Effect.Megid, success_rate=255),
]

techs_by_id = {tech.id: tech for tech in all_techs}
techs_by_name = {tech.name: tech for tech in all_techs}


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
