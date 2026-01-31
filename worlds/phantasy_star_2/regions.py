from collections.abc import Mapping
from typing import NamedTuple

from .Data import area_name as a
from .Data import item_name as i
from .laglib import StateCheck, always, has, has_all, need_all, need_one


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, StateCheck]


def has_dynamite(count: int):
    return has(i.Dynamite, count)


has_jet_scooter = has(i.JetScooterFlag)
has_teim = has(i.Teim)
can_pass_darum_tunnel = need_one([has_teim, has_jet_scooter])
can_pass_zema_tunnel = need_one([has_jet_scooter, need_all([has_teim, has(i.KeyTube)])])


all_regions = [
    # early game
    RegionData(
        a.Motavia,
        {
            a.Shure: always(),
            a.Nido: has_dynamite(1),
            a.Oputa: can_pass_darum_tunnel,
            a.BioSystemsLab: need_all([can_pass_darum_tunnel, has_dynamite(2)]),
            a.Roron: can_pass_zema_tunnel,
            a.Kueri: can_pass_zema_tunnel,
            a.MotavianWater: has_jet_scooter,
            a.Gaira: has_all({i.RedDamFlag, i.YellowDamFlag, i.BlueDamFlag, i.GreenDamFlag}),
            a.Dezolis: has(i.SpaceshipFlag),
        },
    ),
    RegionData(a.Shure, {a.ShureLockedChests: has(i.SmallKey)}),
    RegionData(a.ShureLockedChests, {}),
    RegionData(a.Nido, {}),
    RegionData(a.Oputa, {}),
    RegionData(a.BioSystemsLab, {a.BioSystemsLabBasement: has_dynamite(3)}),
    RegionData(a.BioSystemsLabBasement, {}),
    RegionData(a.Roron, {}),
    RegionData(a.Kueri, {}),
    # mid game
    RegionData(
        a.MotavianWater,
        {
            a.Uzo: always(),
            a.Climatrol: has(i.MarueraGum),
            a.ControlTower: has_all({i.MusikFlag, i.NeifirstFlag}),
            a.RedDam: has(i.RedCard),
            a.YellowDam: has(i.YellowCard),
            a.BlueDam: has(i.BlueCard),
            a.GreenDam: has(i.GreenCard),
        },
    ),
    RegionData(a.ControlTower, {}),
    RegionData(a.Uzo, {}),
    RegionData(a.Climatrol, {}),
    RegionData(a.RedDam, {}),
    RegionData(a.YellowDam, {}),
    RegionData(a.BlueDam, {}),
    RegionData(a.GreenDam, {}),
    RegionData(a.Gaira, {}),
    # late game
    RegionData(
        a.Dezolis,
        {
            a.DezolisDungeons: has(i.Prism),
            a.Noah: has_all(
                {
                    i.NeiArmor,
                    i.NeiCape,
                    i.NeiCrown,
                    i.NeiEmel,
                    i.NeiMet,
                    i.NeiShield,
                    i.NeiShot,
                    i.NeiSlasher,
                    i.NeiSword,  # not needed, but...
                }
            ),
        },
    ),
    RegionData(a.DezolisDungeons, {}),
    RegionData(a.Noah, {}),
]

regions_by_name = {region.name: region for region in all_regions}
