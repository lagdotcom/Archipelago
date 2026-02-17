from collections.abc import Mapping
from typing import NamedTuple

from rule_builder.rules import Has, HasAll, Rule, True_

from .Data import area_name as a
from .Data import item_name as i


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, Rule]


has_jet_scooter = Has(i.JetScooterFlag)
can_pass_darum_tunnel = has_jet_scooter | Has(i.Teim)
can_pass_zema_tunnel = has_jet_scooter | HasAll(i.Teim, i.KeyTube)


all_regions = [
    # early game
    RegionData(
        a.Motavia,
        {
            a.Shure: True_(),
            a.Nido: Has(i.Dynamite),
            a.Oputa: can_pass_darum_tunnel,
            a.BioSystemsLab: can_pass_darum_tunnel & Has(i.Dynamite, 2),
            a.Roron: can_pass_zema_tunnel,
            a.Kueri: can_pass_zema_tunnel,
            a.MotavianWater: has_jet_scooter,
            a.Gaira: HasAll(i.RedDamFlag, i.YellowDamFlag, i.BlueDamFlag, i.GreenDamFlag),
            a.Dezolis: Has(i.SpaceshipFlag),
        },
    ),
    RegionData(a.Shure, {a.ShureLockedChests: Has(i.SmallKey)}),
    RegionData(a.ShureLockedChests, {}),
    RegionData(a.Nido, {}),
    RegionData(a.Oputa, {}),
    RegionData(a.BioSystemsLab, {a.BioSystemsLabBasement: Has(i.Dynamite, 3)}),
    RegionData(a.BioSystemsLabBasement, {}),
    RegionData(a.Roron, {}),
    RegionData(a.Kueri, {}),
    # mid game
    RegionData(
        a.MotavianWater,
        {
            a.Uzo: True_(),
            a.Climatrol: Has(i.MarueraGum),
            a.ControlTower: HasAll(i.MusikFlag, i.NeifirstFlag),
            a.RedDam: Has(i.RedCard),
            a.YellowDam: Has(i.YellowCard),
            a.BlueDam: Has(i.BlueCard),
            a.GreenDam: Has(i.GreenCard),
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
            a.DezolisDungeons: Has(i.Prism),
            a.Noah: HasAll(
                i.NeiArmor,
                i.NeiCape,
                i.NeiCrown,
                i.NeiEmel,
                i.NeiMet,
                i.NeiShield,
                i.NeiShot,
                i.NeiSlasher,
                i.NeiSword,  # not needed, but...
            ),
        },
    ),
    RegionData(a.DezolisDungeons, {}),
    RegionData(a.Noah, {}),
]

regions_by_name = {region.name: region for region in all_regions}
