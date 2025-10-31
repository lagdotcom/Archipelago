
from typing import Mapping, NamedTuple
from .Names import ItemName, RegionName


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, list[list[str]]]


all_regions = [
    RegionData(RegionName.Lab1, {
        RegionName.Lab1Str: [[ItemName.DwarfKey]],
        RegionName.Lab1Cou: [[ItemName.TrialOfStrength]],
        RegionName.Lab1Tru: [[ItemName.OrbOfTruth]],
    }),
    RegionData(RegionName.Lab1Str, {RegionName.Str: []}),
    RegionData(RegionName.Str, {
        RegionName.StrRope: [[ItemName.MysticRope]],
        RegionName.StrCell: [[ItemName.CellKey]],
    }),
    RegionData(RegionName.Lab1Cou, {
               RegionName.Cou: [[ItemName.DwarfKey]]}),
    RegionData(RegionName.Cou, {RegionName.CouCell: [[ItemName.CellKey]]}),
    RegionData(RegionName.Lab1Tru, {
        RegionName.Tru: [[ItemName.OrbOfTruth]],
        RegionName.Wis: [[ItemName.RuneKey]],
        RegionName.Lab2: [[ItemName.TrialOfStrength, ItemName.TrialOfCourage, ItemName.TrialOfTruth, ItemName.TrialOfWisdom]],
    }),
    RegionData(RegionName.Tru, {
        RegionName.TruIdol: [[ItemName.FalseIdol]],
        RegionName.TruCell: [[ItemName.CellKey]],
    }),
    RegionData(RegionName.TruIdol, {}),
    RegionData(RegionName.Wis, {RegionName.WisCell: [[ItemName.CellKey]]}),
    RegionData(RegionName.Lab2, {
        RegionName.Lab3: [],
        RegionName.Lab2Cell: [[ItemName.CellKey]],
    }),
    RegionData(RegionName.Lab3, {
        RegionName.Lab3Rope: [[ItemName.MysticRope]],
        RegionName.Lab3RopeOrCell: [[ItemName.MysticRope], [ItemName.CellKey]],
        RegionName.Lab3Cell: [[ItemName.CellKey]],
    }),
    RegionData(RegionName.StrRope, {}),
    RegionData(RegionName.Lab3Rope, {RegionName.Lab4: []}),
    RegionData(RegionName.Lab3RopeOrCell, {}),
    RegionData(RegionName.Lab4, {
        RegionName.Lab4Orb: [[ItemName.OrbOfTruth]],
        RegionName.Lab4Cell: [[ItemName.CellKey]],
        RegionName.Lab5: [],
    }),
    RegionData(RegionName.Lab4Orb, {}),
    RegionData(RegionName.StrCell, {}),
    RegionData(RegionName.CouCell, {}),
    RegionData(RegionName.TruCell, {}),
    RegionData(RegionName.WisCell, {}),
    RegionData(RegionName.Lab2Cell, {}),
    RegionData(RegionName.Lab3Cell, {}),
    RegionData(RegionName.Lab4Cell, {}),
    RegionData(RegionName.Lab5, {}),
]
