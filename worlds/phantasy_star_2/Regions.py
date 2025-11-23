
from typing import Mapping, NamedTuple

from .Checkers import CheckConstructorFn, Always, And, Has, HasAll, Or
from .Data import Area as A, Item as I


class RegionData(NamedTuple):
    name: str
    exits: Mapping[str, CheckConstructorFn]


def hasDynamite(count: int): return Has(I.Dynamite, count)


hasJetScooter = Has(I.JetScooterFlag)
hasTeim = Has(I.Teim)
canPassDarumTunnel = Or([hasTeim, hasJetScooter])


all_regions = [
    # early game
    RegionData(A.Motavia, {
        A.Shure: Always(),
        A.Nido: hasDynamite(1),
        A.Oputa: canPassDarumTunnel,
        A.BioSystemsLab: And([canPassDarumTunnel, hasDynamite(2)]),
        A.Roron: Or([hasJetScooter, And([canPassDarumTunnel, Has(I.KeyTube)])]),
        A.Kueri: canPassDarumTunnel,
        A.Uzo: hasJetScooter,
        A.Climatrol: HasAll({I.JetScooterFlag, I.MruraGum}),
        A.MotaviaAfterNeifirst: Has(I.NeifirstFlag),
    }),
    RegionData(A.Shure, {
        A.ShureLockedChests: Has(I.SmallKey),
    }),
    RegionData(A.ShureLockedChests, {}),
    RegionData(A.Nido, {}),
    RegionData(A.Oputa, {}),
    RegionData(A.BioSystemsLab, {
        A.BioSystemsLabBasement: hasDynamite(3),
    }),
    RegionData(A.BioSystemsLabBasement, {}),
    RegionData(A.Roron, {}),
    RegionData(A.Kueri, {}),
    RegionData(A.Uzo, {}),
    RegionData(A.Climatrol, {}),

    # mid game
    RegionData(A.MotaviaAfterNeifirst, {
        A.ControlTower: Has(I.MusikFlag),
        A.RedDam: Has(I.RedCard),
        A.YellowDam: Has(I.YellowCard),
        A.BlueDam: Has(I.BlueCard),
        A.GreenDam: Has(I.GreenCard),
        A.Gaira: HasAll({I.RedDamFlag, I.YellowDamFlag, I.BlueDamFlag, I.GreenDamFlag}),
        A.Dezolis: Has(I.SpaceshipFlag),
    }),
    RegionData(A.ControlTower, {}),
    RegionData(A.RedDam, {}),
    RegionData(A.YellowDam, {}),
    RegionData(A.BlueDam, {}),
    RegionData(A.GreenDam, {}),
    RegionData(A.Gaira, {}),

    # late game
    RegionData(A.Dezolis, {
        A.DezolisDungeons: Has(I.Prism),
        A.Noah: HasAll({I.NeiArmor, I.NeiCape, I.NeiCrown, I.NeiEmel, I.NeiMet, I.NeiShield, I.NeiShot, I.NeiSlasher, I.NeiSword}),
    }),
    RegionData(A.DezolisDungeons, {}),
    RegionData(A.Noah, {}),
]

regions_by_name = {region.name: region for region in all_regions}
