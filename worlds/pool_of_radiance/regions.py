from collections.abc import Mapping
from typing import NamedTuple

from rule_builder.rules import Rule, True_

from .Data import area_name as a


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, Rule]


all_regions = [
    RegionData(
        a.NewPhlan,
        {
            a.Slums: True_(),
            a.Wilderness: True_(),
            a.SokalKeep: True_(),
            a.Arena: True_(),  # TODO intro_done?
            a.CityHall: True_(),
            a.MendorLibrary: True_(),
        },
    ),
    RegionData(a.Slums, {a.Sewers: True_()}),
    RegionData(
        a.Sewers,
        {
            a.PodolPlaza: True_(),
            a.MendorLibrary: True_(),
            a.Buccaneer: True_(),  # TODO verify
        },
    ),
    RegionData(a.PodolPlaza, {a.Cadorna: True_(), a.Stojanow: True_(), a.Wilderness: True_()}),
    RegionData(a.Cadorna, {a.MendorLibrary: True_(), a.Wilderness: True_()}),
    RegionData(
        a.Wilderness,
        {
            a.Valhingen: True_(),
            a.KovelMansion: True_(),
            a.WealthyArea: True_(),
            a.Yarash: True_(),
            a.NomadCamp: True_(),  # TODO only while commission open
            a.DragonCave: True_(),
            a.ZhentilKeep: True_(),
            a.Buccaneer: True_(),  # TODO only while bivant heir...?
            a.RuinedCastle: True_(),
            a.KoboldCaves: True_(),
        },
    ),
    RegionData(a.KovelMansion, {a.WealthyArea: True_()}),
    RegionData(a.Stojanow, {a.ValjevoSW: True_()}),
    RegionData(a.ValjevoSW, {a.ValjevoNW: True_()}),
    RegionData(
        a.ValjevoNW,
        {
            a.ValjevoNE: True_(),
            a.ValjevoSE: True_(),  # TODO need Bane sword or fight?
        },
    ),
    RegionData(a.ValjevoSE, {a.ValjevoTower: True_()}),
    RegionData(a.ValjevoNE, {}),
    RegionData(a.ValjevoTower, {}),
    RegionData(a.MendorLibrary, {}),
    RegionData(a.Buccaneer, {}),
    RegionData(a.WealthyArea, {}),
    RegionData(a.SokalKeep, {}),
    RegionData(a.Arena, {}),
    RegionData(a.CityHall, {}),
    RegionData(a.Valhingen, {}),
    RegionData(a.Yarash, {}),
    RegionData(a.NomadCamp, {}),
    RegionData(a.DragonCave, {}),
    RegionData(a.ZhentilKeep, {}),
    RegionData(a.RuinedCastle, {}),
    RegionData(a.KoboldCaves, {}),
]

regions_by_name = {region.name: region for region in all_regions}
