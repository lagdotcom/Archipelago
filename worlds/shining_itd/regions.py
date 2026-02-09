from collections.abc import Mapping
from typing import NamedTuple

from rule_builder.rules import Has, HasAll, Rule, True_

from .Names import item_name, region_name


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, Rule] = {}


all_regions = [
    RegionData(
        region_name.Lab1,
        {
            region_name.Lab1Str: Has(item_name.DwarfKey),
            region_name.Lab1Cou: Has(item_name.TrialOfStrength),
            region_name.Lab1Tru: Has(item_name.OrbOfTruth),
        },
    ),
    RegionData(region_name.Lab1Str, {region_name.Str: True_()}),
    RegionData(
        region_name.Str,
        {
            region_name.StrRope: Has(item_name.MysticRope),
            region_name.StrCell: Has(item_name.CellKey),
        },
    ),
    RegionData(region_name.Lab1Cou, {region_name.Cou: Has(item_name.DwarfKey)}),
    RegionData(region_name.Cou, {region_name.CouCell: Has(item_name.CellKey)}),
    RegionData(
        region_name.Lab1Tru,
        {
            region_name.Tru: Has(item_name.OrbOfTruth),
            region_name.Wis: Has(item_name.RuneKey),
            region_name.Lab2: HasAll(
                item_name.TrialOfStrength, item_name.TrialOfCourage, item_name.TrialOfTruth, item_name.TrialOfWisdom
            ),
        },
    ),
    RegionData(
        region_name.Tru,
        {
            region_name.TruIdol: Has(item_name.FalseIdol),
            region_name.TruCell: Has(item_name.CellKey),
        },
    ),
    RegionData(region_name.TruIdol),
    RegionData(region_name.Wis, {region_name.WisCell: Has(item_name.CellKey)}),
    RegionData(
        region_name.Lab2,
        {
            region_name.Lab3: True_(),
            region_name.Lab2Cell: Has(item_name.CellKey),
        },
    ),
    RegionData(
        region_name.Lab3,
        {
            region_name.Lab3Rope: Has(item_name.MysticRope),
            region_name.Lab3RopeOrCell: Has(item_name.MysticRope) | Has(item_name.CellKey),
            region_name.Lab3Cell: Has(item_name.CellKey),
        },
    ),
    RegionData(region_name.StrRope),
    RegionData(region_name.Lab3Rope, {region_name.Lab4: True_()}),
    RegionData(region_name.Lab3RopeOrCell),
    RegionData(
        region_name.Lab4,
        {
            region_name.Lab4Orb: Has(item_name.OrbOfTruth),
            region_name.Lab4Cell: Has(item_name.CellKey),
            region_name.Lab5: True_(),
        },
    ),
    RegionData(region_name.Lab4Orb),
    RegionData(region_name.StrCell),
    RegionData(region_name.CouCell),
    RegionData(region_name.TruCell),
    RegionData(region_name.WisCell),
    RegionData(region_name.Lab2Cell),
    RegionData(region_name.Lab3Cell),
    RegionData(region_name.Lab4Cell),
    RegionData(region_name.Lab5),
]

regions_by_name = {region.name: region for region in all_regions}
