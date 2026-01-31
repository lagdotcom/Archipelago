from collections.abc import Mapping
from typing import NamedTuple

from .Names import item_name, region_name


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, list[list[str]]]


all_regions = [
    RegionData(
        region_name.Lab1,
        {
            region_name.Lab1Str: [[item_name.DwarfKey]],
            region_name.Lab1Cou: [[item_name.TrialOfStrength]],
            region_name.Lab1Tru: [[item_name.OrbOfTruth]],
        },
    ),
    RegionData(region_name.Lab1Str, {region_name.Str: []}),
    RegionData(
        region_name.Str,
        {
            region_name.StrRope: [[item_name.MysticRope]],
            region_name.StrCell: [[item_name.CellKey]],
        },
    ),
    RegionData(region_name.Lab1Cou, {region_name.Cou: [[item_name.DwarfKey]]}),
    RegionData(region_name.Cou, {region_name.CouCell: [[item_name.CellKey]]}),
    RegionData(
        region_name.Lab1Tru,
        {
            region_name.Tru: [[item_name.OrbOfTruth]],
            region_name.Wis: [[item_name.RuneKey]],
            region_name.Lab2: [
                [item_name.TrialOfStrength, item_name.TrialOfCourage, item_name.TrialOfTruth, item_name.TrialOfWisdom]
            ],
        },
    ),
    RegionData(
        region_name.Tru,
        {
            region_name.TruIdol: [[item_name.FalseIdol]],
            region_name.TruCell: [[item_name.CellKey]],
        },
    ),
    RegionData(region_name.TruIdol, {}),
    RegionData(region_name.Wis, {region_name.WisCell: [[item_name.CellKey]]}),
    RegionData(
        region_name.Lab2,
        {
            region_name.Lab3: [],
            region_name.Lab2Cell: [[item_name.CellKey]],
        },
    ),
    RegionData(
        region_name.Lab3,
        {
            region_name.Lab3Rope: [[item_name.MysticRope]],
            region_name.Lab3RopeOrCell: [[item_name.MysticRope], [item_name.CellKey]],
            region_name.Lab3Cell: [[item_name.CellKey]],
        },
    ),
    RegionData(region_name.StrRope, {}),
    RegionData(region_name.Lab3Rope, {region_name.Lab4: []}),
    RegionData(region_name.Lab3RopeOrCell, {}),
    RegionData(
        region_name.Lab4,
        {
            region_name.Lab4Orb: [[item_name.OrbOfTruth]],
            region_name.Lab4Cell: [[item_name.CellKey]],
            region_name.Lab5: [],
        },
    ),
    RegionData(region_name.Lab4Orb, {}),
    RegionData(region_name.StrCell, {}),
    RegionData(region_name.CouCell, {}),
    RegionData(region_name.TruCell, {}),
    RegionData(region_name.WisCell, {}),
    RegionData(region_name.Lab2Cell, {}),
    RegionData(region_name.Lab3Cell, {}),
    RegionData(region_name.Lab4Cell, {}),
    RegionData(region_name.Lab5, {}),
]

regions_by_name = {region.name: region for region in all_regions}
