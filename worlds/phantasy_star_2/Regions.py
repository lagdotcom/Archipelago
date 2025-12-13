from typing import Mapping, NamedTuple

from .laglib import StateCheck, always, has, has_all, need_all, need_one
from .Data import Area as A, Item as I


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, StateCheck]


def hasDynamite(count: int):
    return has(I.Dynamite, count)


hasJetScooter = has(I.JetScooterFlag)
hasTeim = has(I.Teim)
canPassDarumTunnel = need_one([hasTeim, hasJetScooter])


all_regions = [
    # early game
    RegionData(
        A.Motavia,
        {
            A.Shure: always(),
            A.Nido: hasDynamite(1),
            A.Oputa: canPassDarumTunnel,
            A.BioSystemsLab: need_all([canPassDarumTunnel, hasDynamite(2)]),
            A.Roron: need_one(
                [hasJetScooter, need_all([canPassDarumTunnel, has(I.KeyTube)])]
            ),
            A.Kueri: canPassDarumTunnel,
            A.ControlTower: has_all({I.MusikFlag, I.NeifirstFlag}),
            A.MotavianWater: hasJetScooter,
            A.Gaira: has_all(
                {I.RedDamFlag, I.YellowDamFlag, I.BlueDamFlag, I.GreenDamFlag}
            ),
            A.Dezolis: has(I.SpaceshipFlag),
        },
    ),
    RegionData(A.Shure, {A.ShureLockedChests: has(I.SmallKey)}),
    RegionData(A.ShureLockedChests, {}),
    RegionData(A.Nido, {}),
    RegionData(A.Oputa, {}),
    RegionData(A.BioSystemsLab, {A.BioSystemsLabBasement: hasDynamite(3)}),
    RegionData(A.BioSystemsLabBasement, {}),
    RegionData(A.Roron, {}),
    RegionData(A.Kueri, {}),
    # mid game
    RegionData(
        A.MotavianWater,
        {
            A.Uzo: always(),
            A.Climatrol: has(I.MarueraGum),
            A.RedDam: has(I.RedCard),
            A.YellowDam: has(I.YellowCard),
            A.BlueDam: has(I.BlueCard),
            A.GreenDam: has(I.GreenCard),
        },
    ),
    RegionData(A.ControlTower, {}),
    RegionData(A.Uzo, {}),
    RegionData(A.Climatrol, {}),
    RegionData(A.RedDam, {}),
    RegionData(A.YellowDam, {}),
    RegionData(A.BlueDam, {}),
    RegionData(A.GreenDam, {}),
    RegionData(A.Gaira, {}),
    # late game
    RegionData(
        A.Dezolis,
        {
            A.DezolisDungeons: has(I.Prism),
            A.Noah: has_all(
                {
                    I.NeiArmor,
                    I.NeiCape,
                    I.NeiCrown,
                    I.NeiEmel,
                    I.NeiMet,
                    I.NeiShield,
                    I.NeiShot,
                    I.NeiSlasher,
                    I.NeiSword,  # not needed, but...
                }
            ),
        },
    ),
    RegionData(A.DezolisDungeons, {}),
    RegionData(A.Noah, {}),
]

regions_by_name = {region.name: region for region in all_regions}
