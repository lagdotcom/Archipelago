from collections.abc import Mapping
from typing import NamedTuple

from rule_builder.rules import Rule, True_

from .Data import area_name as a


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, Rule]


all_regions = [
    RegionData(a.NewPhlan, {a.Slums: True_()}),
    RegionData(a.Slums, {}),
]

regions_by_name = {region.name: region for region in all_regions}
