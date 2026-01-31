from enum import Enum
from typing import NamedTuple

from .Data import tech_id as t


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
    Tech(t.FOI, "FOI", 2, Effect.Damage, power=15),
    Tech(t.GIFOI, "GIFOI", 6, Effect.Damage, power=40),
    Tech(t.NAFOI, "NAFOI", 12, Effect.Damage, power=130),
    Tech(t.ZAN, "ZAN", 4, Effect.Damage, target=Target.Group, power=20),
    Tech(t.GIZAN, "GIZAN", 7, Effect.Damage, target=Target.Group, power=30),
    Tech(t.NAZAN, "NAZAN", 11, Effect.Damage, target=Target.Group, power=100),
    Tech(t.GRA, "GRA", 8, Effect.Damage, target=Target.All, power=20),
    Tech(t.GIGRA, "GIGRA", 12, Effect.Damage, target=Target.All, power=40),
    Tech(t.NAGRA, "NAGRA", 20, Effect.Damage, target=Target.All, power=80),
    Tech(t.TSU, "TSU", 6, Effect.Damage, power=30),
    Tech(t.GITHU, "GITHU", 13, Effect.Damage, power=80),
    Tech(t.NATHU, "NATHU", 20, Effect.Damage, power=150),
    Tech(t.SHIFT, "SHIFT", 5, Effect.AttackUp, success_rate=255, power=20),
    Tech(t.FANBI, "FANBI", 2, Effect.Drain, Filter.Bio, success_rate=255, power=10),
    Tech(
        t.EIJIA,
        "EIJIA",
        4,
        Effect.Damage,
        Filter.Mech,
        Target.Group,
        success_rate=255,
        power=23,
    ),
    Tech(t.BROSE, "BROSE", 8, Effect.Kill, Filter.Mech, success_rate=127, power=500),
    Tech(t.CONTE, "CONTE", 6, Effect.Freeze, Filter.Mech, success_rate=255),
    Tech(t.GAJ, "GAJ", 1, Effect.Damage, Filter.Mech, success_rate=255, power=20),
    Tech(t.GIGAJ, "GIGAJ", 5, Effect.Damage, Filter.Mech, power=60),
    Tech(t.NAGAJ, "NAGAJ", 15, Effect.Damage, Filter.Mech, power=150),
    Tech(t.SAG, "SAG", 3, Effect.Damage, Filter.Mech, Target.All, power=20),
    Tech(t.GISAG, "GISAG", 15, Effect.Damage, Filter.Mech, Target.All, power=60),
    Tech(t.NASAG, "NASAG", 27, Effect.Damage, Filter.Mech, Target.All, power=150),
    Tech(t.GEN, "GEN", 1, Effect.Damage, Filter.Bio, power=20),
    Tech(t.SAGEN, "SAGEN", 3, Effect.Damage, Filter.Bio, Target.All, power=20),
    Tech(t.VOL, "VOL", 8, Effect.Kill, Filter.Bio, success_rate=153, power=500),
    Tech(
        t.SAVOL,
        "SAVOL",
        16,
        Effect.Kill,
        Filter.Bio,
        Target.Group,
        success_rate=178,
        power=500,
    ),
    Tech(t.SHIZA, "SHIZA", 6, Effect.Freeze, Filter.Bio, success_rate=255),
    Tech(t.DORAN, "DORAN", 2, Effect.Confuse, Filter.Bio, success_rate=204),
    Tech(t.RIMIT, "RIMIT", 3, Effect.Paralysis, Filter.Bio, success_rate=127),
    Tech(t.SHINB, "SHINB", 4, Effect.Terrify, Filter.Bio, success_rate=255),
    Tech(t.FORSA, "FORSA", 1, Effect.Confuse, Filter.Mech, success_rate=127),
    Tech(t.RIMET, "RIMET", 3, Effect.Paralysis, Filter.Mech, success_rate=102),
    Tech(t.SHU, "SHU", 3, Effect.DefenceUp, success_rate=255),
    Tech(t.SASHU, "SASHU", 8, Effect.DefenceUp, target=Target.All, success_rate=255),
    Tech(t.DEBAN, "DEBAN", 4, Effect.AccuracyDown, target=Target.All, success_rate=255),
    Tech(t.NER, "NER", 2, Effect.AgilityUp, success_rate=255),
    Tech(t.SANER, "SANER", 6, Effect.AgilityUp, target=Target.All, success_rate=255),
    Tech(t.RES, "RES", 3, Effect.Heal, map=True, success_rate=255, power=20),
    Tech(t.GIRES, "GIRES", 7, Effect.Heal, map=True, success_rate=255, power=60),
    Tech(t.NARES, "NARES", 13, Effect.Heal, map=True, success_rate=255, power=500),
    Tech(
        t.SAR,
        "SAR",
        13,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=20,
    ),
    Tech(
        t.GISAR,
        "GISAR",
        29,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=60,
    ),
    Tech(
        t.NASAR,
        "NASAR",
        53,
        Effect.Heal,
        target=Target.All,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(t.SAK, "SAK", 1, Effect.Sacrifice, map=True, success_rate=255, power=500),
    Tech(
        t.NASAK,
        "NASAK",
        1,
        Effect.Sacrifice,
        target=Target.All,
        map=True,
        success_rate=255,
        power=500,
    ),
    Tech(t.ANTI, "ANTI", 2, Effect.Antidote, battle=False, map=True, success_rate=255),
    Tech(t.REVER, "REVER", 30, Effect.Revive, battle=False, map=True, success_rate=255),
    Tech(
        t.RYUKA,
        "RYUKA",
        8,
        Effect.TownTeleport,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(
        t.HINAS,
        "HINAS",
        4,
        Effect.LeaveDungeon,
        battle=False,
        map=True,
        success_rate=255,
    ),
    Tech(t.MUSIK, "MUSIK", 3, Effect.Musik, success_rate=255),
    Tech(t.MEGID, "MEGID", 55, Effect.Megid, success_rate=255),
]

techs_by_id = {tech.id: tech for tech in all_techs}
techs_by_name = {tech.name: tech for tech in all_techs}


tech_strengths: dict[int, int] = {
    # Tier 1
    t.RES: 10_00,
    t.FOI: 10_01,
    t.GAJ: 10_02,
    t.GEN: 10_03,
    t.FANBI: 10_04,
    t.RIMET: 10_05,
    t.RIMIT: 10_06,
    t.SHU: 10_07,
    # Tier 1.5
    t.SAR: 15_00,
    t.ANTI: 15_01,
    t.SAK: 15_02,
    t.TSU: 15_03,
    t.EIJIA: 15_04,
    t.SHINB: 15_05,
    t.HINAS: 15_06,
    # Tier 2
    t.GIRES: 20_00,
    t.GIGAJ: 20_01,
    t.ZAN: 20_02,
    t.SAG: 20_03,
    t.SAGEN: 20_04,
    t.GIFOI: 20_05,
    t.FORSA: 20_06,
    t.DORAN: 20_07,
    t.RYUKA: 20_08,
    t.NER: 20_10,
    t.SASHU: 20_11,
    # Tier 2.5
    t.GISAR: 25_00,
    t.GRA: 25_01,
    t.GITHU: 25_02,
    t.SHIFT: 25_03,
    # Tier 3
    t.GIZAN: 30_00,
    t.NAFOI: 30_01,
    t.NAGAJ: 30_02,
    t.GIGRA: 30_03,
    t.GISAG: 30_04,
    t.CONTE: 30_05,
    t.SHIZA: 30_06,
    # Tier 3.5
    t.NASAK: 35_00,
    t.NATHU: 35_01,
    # Tier 4
    t.REVER: 40_00,
    t.NARES: 40_01,
    t.BROSE: 40_02,
    t.VOL: 40_03,
    t.SANER: 40_05,
    t.DEBAN: 40_06,
    # Tier 4.5
    t.NAZAN: 45_00,
    t.NASAG: 45_01,
    t.NAGRA: 45_02,
    t.SAVOL: 45_03,
    # Tier 5
    t.NASAR: 50_00,
    t.MEGID: 50_01,
}
