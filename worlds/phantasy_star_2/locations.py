from collections.abc import Callable
from enum import Enum
from typing import NamedTuple

from rule_builder.rules import Has, HasAll, Rule

from .constants import (
    TREASURE_CHEST_CONTENT_ARRAY,
    chest_flags,
    game_mode,
)
from .Data import area_name as a
from .Data import item_name as i
from .enums import GameMode
from .items import ItemType
from .laglib import IntSpan, MemoryManager
from .laglib import genesis_ram as ram
from .laglib import genesis_rom as rom


class FlagCheck(NamedTuple):
    span: IntSpan
    predicate: Callable[[int], bool]

    def __repr__(self):
        return repr(self.span) + "?"

    def test(self, mem: MemoryManager):
        value = self.span.get(mem)
        return self.predicate(value)


def equals1(v: int):
    return v == 1


class LocationType(Enum):
    CHEST = 0
    FLAG = 1
    GRANTED_ITEM = 2


class LocationData:
    type: LocationType
    id: int
    region_name: str
    name: str
    vanilla_item: str
    rom_location: IntSpan | None = None
    fixed_item: str | None = None
    checks: list[FlagCheck]
    rule: Rule | None = None
    restricted_types: set[ItemType]
    permanently_missable: bool = False

    def __init__(
        self,
        type: LocationType,
        id: int,
        region_name: str,
        name: str,
        vanilla_item: str,
        restricted_types: set[ItemType],
        permanently_missable: bool = False,
    ):
        self.type = type
        self.id = id
        self.region_name = region_name
        self.name = name
        self.vanilla_item = vanilla_item
        self.restricted_types = restricted_types
        self.permanently_missable = permanently_missable
        self.checks = []

    def at(self, span: IntSpan):
        self.rom_location = span
        return self

    def fix(self, item_name: str):
        self.fixed_item = item_name
        return self

    def flag(self, address: int, predicate: Callable[[int], bool] = equals1):
        self.checks.append(FlagCheck(IntSpan(ram, address, 1), predicate))
        return self

    def set_rule(self, rule: Rule):
        self.rule = rule
        return self


def chest(
    id: int, region_name: str, name: str, chest_index: int, vanilla_item: str, permanently_missable: bool = False
):
    return (
        LocationData(
            LocationType.CHEST,
            id,
            region_name,
            name,
            vanilla_item,
            {ItemType.Garbage, ItemType.Item, ItemType.Money, ItemType.FlagAsItem},
            permanently_missable,
        )
        .at(IntSpan(rom, TREASURE_CHEST_CONTENT_ARRAY + chest_index * 2, 2))
        .flag(chest_flags.address + chest_index)
    )


def flag(
    id: int,
    region_name: str,
    name: str,
    vanilla_item: str,
    ram_location: int,
    predicate: Callable[[int], bool] = equals1,
):
    return LocationData(LocationType.FLAG, id, region_name, name, vanilla_item, {ItemType.Flag}).flag(
        ram_location, predicate
    )


def granted(
    id: int,
    region_name: str,
    name: str,
    vanilla_item: str,
    rom_address: int,
    ram_address: int,
    predicate: Callable[[int], bool] = equals1,
):
    return (
        LocationData(
            LocationType.GRANTED_ITEM,
            id,
            region_name,
            name,
            vanilla_item,
            {ItemType.Item, ItemType.FlagAsItem},
        )
        .at(IntSpan(rom, rom_address, 1))
        .flag(ram_address, predicate)
    )


skure_locations = [
    chest(452_00_01, a.Dezolis, "Skure - 15000 meseta", 0x1, i.meseta(15000)),
    chest(452_00_02, a.Dezolis, "Skure - Mogic Cap", 0x2, i.MogicCap),
    chest(452_00_03, a.Dezolis, "Skure - 18000 meseta", 0x3, i.meseta(18000)),
    chest(452_00_04, a.Dezolis, "Skure - Magic Cap", 0x4, i.MagicCap),
    chest(452_00_05, a.Dezolis, "Skure - 7800 meseta", 0x5, i.meseta(7800)),
    chest(452_00_06, a.Dezolis, "Skure - LaconChest", 0x6, i.LaconChest),
    chest(452_00_07, a.Dezolis, "Skure - 5600 meseta", 0x7, i.meseta(5600)),
    chest(452_00_08, a.Dezolis, "Skure - GardaBoots", 0x8, i.GardaBoots),
    chest(452_00_09, a.Dezolis, "Skure - 8600 meseta", 0x9, i.meseta(8600)),
    chest(452_00_10, a.Dezolis, "Skure - Magic Cap 2", 0xA, i.MagicCap),
    chest(452_00_11, a.Dezolis, "Skure - 12000 meseta", 0xB, i.meseta(12000)),
    chest(452_00_12, a.Dezolis, "Skure - 6400 meseta", 0xC, i.meseta(6400)),
]

esper_mansion_locations = [
    chest(452_00_14, a.Dezolis, "Esper Mansion - Prism", 0xE, i.Prism).flag(0xC743, lambda v: v == 3),
    chest(452_00_15, a.Dezolis, "Esper Mansion - NeiSword", 0xF, i.NeiSword)
    .flag(0xC744, lambda v: v == 1)
    .set_rule(
        HasAll(
            i.NeiArmor,
            i.NeiCape,
            i.NeiCrown,
            i.NeiEmel,
            i.NeiMet,
            i.NeiShield,
            i.NeiShot,
            i.NeiSlasher,
        )
    ),
]

shure_locations = [
    chest(452_00_16, a.ShureLockedChests, "Shure Locked - Monomate", 0x10, i.Monomate),
    chest(452_00_17, a.ShureLockedChests, "Shure Locked - 150 meseta", 0x11, i.meseta(150)),
    chest(452_00_18, a.ShureLockedChests, "Shure Locked - Dynamite", 0x12, i.Dynamite),
    chest(452_00_19, a.ShureLockedChests, "Shure Locked - Dynamite 2", 0x13, i.Dynamite),
    chest(452_00_20, a.Shure, "Shure - 40 meseta", 0x14, i.meseta(40)),
    chest(452_00_21, a.Shure, "Shure - Dimate", 0x15, i.Dimate),
    chest(452_00_22, a.Shure, "Shure - Headgear", 0x16, i.Headgear),
    chest(452_00_23, a.Shure, "Shure - 200 meseta", 0x17, i.meseta(200)),
    chest(452_00_24, a.Shure, "Shure - Sil Ribbon", 0x18, i.SilRibbon),
    granted(
        452_01_01,
        a.Shure,
        "Shure - Small Key",
        i.SmallKey,
        0xDBE3,
        0xC721,
        lambda v: v >= 1,
    ),
    granted(452_01_02, a.Shure, "Shure - Letter", i.Letter, 0xDBF3, 0xC721, lambda v: v >= 2),
]

nido_locations = [
    chest(452_00_25, a.Nido, "Nido - 20 meseta", 0x19, i.meseta(20)),
    chest(452_00_26, a.Nido, "Nido - 100 meseta", 0x1A, i.meseta(100)),
    chest(452_00_27, a.Nido, "Nido - Dimate", 0x1B, i.Dimate),
    chest(452_00_28, a.Nido, "Nido - Trimate", 0x1C, i.Trimate),
    chest(452_00_29, a.Nido, "Nido - 60 meseta", 0x1D, i.meseta(60)),
    granted(452_01_03, a.Nido, "Nido - Teim", i.Teim, 0xDC6D, 0xC727).set_rule(Has(i.Letter)),
]

roron_locations = [
    chest(452_00_30, a.Roron, "Roron - Garbage", 0x1E, i.Garbage),
    chest(452_00_31, a.Roron, "Roron - Garbage 2", 0x1F, i.Garbage),
    chest(452_00_32, a.Roron, "Roron - Ceram Bar", 0x20, i.CeramBar),
    chest(452_00_33, a.Roron, "Roron - Garbage 3", 0x21, i.Garbage),
    chest(452_00_34, a.Roron, "Roron - Cannon", 0x22, i.Cannon),
    chest(452_00_35, a.Roron, "Roron - Garbage 4", 0x23, i.Garbage),
    granted(
        452_02_00,
        a.Roron,
        "Roron - Jet Scooter Guy",
        i.JetScooterFlag,
        0xBF857,
        0xC753,
    ),
]

yellow_dam_locations = [
    chest(452_00_36, a.YellowDam, "Yellow Dam - Escapipe", 0x24, i.Escapipe),
    chest(452_00_37, a.YellowDam, "Yellow Dam - Crystanish", 0x25, i.Crystanish),
    chest(452_00_38, a.YellowDam, "Yellow Dam - CrystCape", 0x26, i.CrystCape),
    chest(452_00_39, a.YellowDam, "Yellow Dam - CrystChest", 0x27, i.CrystChest),
    chest(452_00_40, a.YellowDam, "Yellow Dam - Amber Robe", 0x28, i.AmberRobe),
    flag(452_02_01, a.YellowDam, "Yellow Dam - Console", i.YellowDamFlag, 0xC731).fix(i.YellowDamFlag),
]

red_dam_locations = [
    chest(452_00_41, a.RedDam, "Red Dam - Swd of Ang", 0x29, i.SwdOfAng),
    chest(452_00_42, a.RedDam, "Red Dam - Fire Slshr", 0x2A, i.FireSlshr),
    chest(452_00_43, a.RedDam, "Red Dam - Fire Staff", 0x2B, i.FireStaff),
    flag(452_02_02, a.RedDam, "Red Dam - Console", i.RedDamFlag, 0xC733).fix(i.RedDamFlag),
]

blue_dam_locations = [
    chest(452_00_44, a.BlueDam, "Blue Dam - Antidote", 0x2C, i.Antidote),
    chest(452_00_45, a.BlueDam, "Blue Dam - CresceGear", 0x2D, i.CresceGear),
    chest(452_00_46, a.BlueDam, "Blue Dam - Snow Crown", 0x2E, i.SnowCrown),
    chest(452_00_47, a.BlueDam, "Blue Dam - Star Mist", 0x2F, i.StarMist),
    chest(452_00_48, a.BlueDam, "Blue Dam - Wind Scarf", 0x30, i.WindScarf),
    chest(452_00_49, a.BlueDam, "Blue Dam - ColorScarf", 0x31, i.ColorScarf),
    chest(452_00_50, a.BlueDam, "Blue Dam - Trimate", 0x32, i.Trimate),
    chest(452_00_51, a.BlueDam, "Blue Dam - Storm Gear", 0x33, i.StormGear),
    flag(452_02_03, a.BlueDam, "Blue Dam - Console", i.BlueDamFlag, 0xC72F).fix(i.BlueDamFlag),
]

green_dam_locations = [
    chest(452_00_52, a.GreenDam, "Green Dam - Star Mist", 0x34, i.StarMist),
    chest(452_00_53, a.GreenDam, "Green Dam - Aegis", 0x35, i.Aegis),
    chest(452_00_54, a.GreenDam, "Green Dam - Telepipe", 0x36, i.Telepipe),
    chest(452_00_55, a.GreenDam, "Green Dam - Gr Sleeves", 0x37, i.GrSleeves),
    chest(452_00_56, a.GreenDam, "Green Dam - Truth Slvs", 0x38, i.TruthSlvs),
    flag(452_02_04, a.GreenDam, "Green Dam - Console", i.GreenDamFlag, 0xC72D).fix(i.GreenDamFlag),
]

bio_systems_lab_locations = [
    chest(
        452_00_57,
        a.BioSystemsLabBasement,
        "Bio-Systems Lab - Trimate",
        0x39,
        i.Trimate,
    ),
    chest(
        452_00_58,
        a.BioSystemsLabBasement,
        "Bio-Systems Lab - Antidote",
        0x3A,
        i.Antidote,
    ),
    chest(
        452_00_59,
        a.BioSystemsLabBasement,
        "Bio-Systems Lab - PoisonShot",
        0x3B,
        i.PoisonShot,
    ),
    chest(452_00_60, a.BioSystemsLab, "Bio-Systems Lab - Antidote 2", 0x3C, i.Antidote),
    chest(452_00_61, a.BioSystemsLab, "Bio-Systems Lab - Scalpel", 0x3D, i.Scalpel),
    chest(452_00_62, a.BioSystemsLab, "Bio-Systems Lab - Star Mist", 0x3E, i.StarMist),
    chest(452_00_63, a.BioSystemsLab, "Bio-Systems Lab - Dynamite", 0x3F, i.Dynamite),
    granted(
        452_01_04,
        a.BioSystemsLabBasement,
        "Bio-Systems Lab - Recorder",
        i.Recorder,
        0xDBFD,
        0xC722,
    ),
]

climatrol_locations = [
    chest(452_00_64, a.Climatrol, "Climatrol - Jwl Ribbon", 0x40, i.JwlRibbon, permanently_missable=True),
    chest(452_00_65, a.Climatrol, "Climatrol - FiberVest", 0x41, i.FiberVest, permanently_missable=True),
    chest(452_00_66, a.Climatrol, "Climatrol - KnifeBoots", 0x42, i.KnifeBoots, permanently_missable=True),
    chest(452_00_67, a.Climatrol, "Climatrol - Sil Ribbon", 0x43, i.SilRibbon, permanently_missable=True),
    chest(452_00_68, a.Climatrol, "Climatrol - Sandals", 0x44, i.Sandals, permanently_missable=True),
    chest(452_00_69, a.Climatrol, "Climatrol - Laser Bar", 0x45, i.LaserBar, permanently_missable=True),
    chest(452_00_70, a.Climatrol, "Climatrol - Ceram Bar", 0x46, i.CeramBar, permanently_missable=True),
    flag(452_02_05, a.Climatrol, "Climatrol - Neifirst", i.NeifirstFlag, 0xC735).fix(i.NeifirstFlag),
    # beating Neifirst immediately sets c710=3 and c737=1
    # after the 'Nei is really dead' scene, sets c710=4 and c711=3
    # the later scenes set all kinds of c710/1 values as it progresses
]

naval_locations = [
    chest(452_00_71, a.DezolisDungeons, "Naval - NeiShield", 0x47, i.NeiShield),
    chest(452_00_72, a.DezolisDungeons, "Naval - NeiEmel", 0x48, i.NeiEmel),
    chest(452_00_73, a.DezolisDungeons, "Naval - Truth Slvs", 0x49, i.TruthSlvs),
    chest(452_00_74, a.DezolisDungeons, "Naval - Trimate", 0x4A, i.Trimate),
    chest(452_00_75, a.DezolisDungeons, "Naval - Mir Emel", 0x4B, i.MirEmel),
    chest(452_00_76, a.DezolisDungeons, "Naval - Lacon Emel", 0x4C, i.LaconEmel),
    chest(452_00_77, a.DezolisDungeons, "Naval - GrSleeves", 0x4D, i.GrSleeves),
]

menobe_locations = [
    chest(452_00_78, a.DezolisDungeons, "Menobe - NeiCrown", 0x4E, i.NeiCrown),
    chest(452_00_79, a.DezolisDungeons, "Menobe - Storm Gear", 0x4F, i.StormGear),
    chest(452_00_80, a.DezolisDungeons, "Menobe - NeiMet", 0x50, i.NeiMet),
    chest(452_00_81, a.DezolisDungeons, "Menobe - ColorScarf", 0x51, i.ColorScarf),
]

ikuto_locations = [
    chest(452_00_82, a.DezolisDungeons, "Ikuto - NeiSlasher", 0x52, i.NeiSlasher),
    chest(452_00_83, a.DezolisDungeons, "Ikuto - NeiShot", 0x53, i.NeiShot),
    chest(452_00_84, a.DezolisDungeons, "Ikuto - FireStaff", 0x54, i.FireStaff),
    chest(452_00_85, a.DezolisDungeons, "Ikuto - Lacn Mace", 0x55, i.LacnMace),
    chest(452_00_86, a.DezolisDungeons, "Ikuto - Pls Cannon", 0x56, i.PlsCannon),
    chest(452_00_87, a.DezolisDungeons, "Ikuto - Lac Dagger", 0x57, i.LacDagger),
]

guaron_locations = [
    chest(452_00_88, a.DezolisDungeons, "Guaron - Amber Robe", 0x58, i.AmberRobe),
    chest(452_00_89, a.DezolisDungeons, "Guaron - Laconinish", 0x59, i.Laconinish),
    chest(452_00_90, a.DezolisDungeons, "Guaron - CrystChest", 0x5A, i.CrystChest),
    chest(452_00_91, a.DezolisDungeons, "Guaron - NeiCape", 0x5B, i.NeiCape),
    chest(452_00_92, a.DezolisDungeons, "Guaron - CrystCape", 0x5C, i.CrystCape),
    chest(452_00_93, a.DezolisDungeons, "Guaron - NeiArmor", 0x5D, i.NeiArmor),
]

uzo_locations = [
    granted(452_01_05, a.Uzo, "Uzo - Maruera Tree", i.MarueraLeaf, 0xDBAD, 0xC720),
]

paseo_locations = [
    granted(
        452_01_06,
        a.Motavia,
        "Paseo - Give Recorder to Governor",
        i.KeyTube,
        0xC4D1,
        0xC750,
    ).set_rule(Has(i.Recorder))
]


oputa_locations = [flag(452_02_06, a.Oputa, "Oputa - Ustvestia", i.MusikFlag, 0xC751).fix(i.MusikFlag)]

control_tower_locations = [
    granted(
        452_01_07,
        a.ControlTower,
        "Control Tower - Green Console",
        i.GreenCard,
        0xBF872,
        0xC723,
    ),
    granted(
        452_01_08,
        a.ControlTower,
        "Control Tower - Blue Console",
        i.BlueCard,
        0xBF873,
        0xC724,
    ),
    granted(
        452_01_09,
        a.ControlTower,
        "Control Tower - Yellow Console",
        i.YellowCard,
        0xBF874,
        0xC725,
    ),
    granted(
        452_01_10,
        a.ControlTower,
        "Control Tower - Red Console",
        i.RedCard,
        0xBF875,
        0xC726,
    ),
]

kueri_locations = [
    granted(
        452_01_11,
        a.Kueri,
        "Kueri - Give Maruera Leaf to Researcher",
        i.MarueraGum,
        0xC94F,
        0xC752,
    ).set_rule(Has(i.MarueraLeaf)),
]

gaira_locations = [granted(452_02_07, a.Gaira, "Gaira - Console", i.SpaceshipFlag, 0xBF89D, 0xC754)]

noah_locations = [
    flag(
        452_02_08,
        a.Noah,
        "Noah - Mother Brain",
        i.WinTheGameFlag,
        game_mode.address,
        lambda v: GameMode(v) == GameMode.ENDING,
    ).fix(i.WinTheGameFlag),
]

all_locations = (
    skure_locations
    + esper_mansion_locations
    + shure_locations
    + nido_locations
    + roron_locations
    + yellow_dam_locations
    + red_dam_locations
    + blue_dam_locations
    + green_dam_locations
    + bio_systems_lab_locations
    + climatrol_locations
    + naval_locations
    + menobe_locations
    + ikuto_locations
    + guaron_locations
    + uzo_locations
    + paseo_locations
    + oputa_locations
    + control_tower_locations
    + kueri_locations
    + gaira_locations
    + noah_locations
)

locations_by_id = {location.id: location for location in all_locations}
locations_by_name = {location.name: location for location in all_locations}

location_name_groups = {
    "Shure": {loc.name for loc in shure_locations},
    "Tower of Nido": {loc.name for loc in nido_locations},
    "Skure": {loc.name for loc in skure_locations},
    "Roron": {loc.name for loc in roron_locations},
    "Bio-Systems Lab": {loc.name for loc in bio_systems_lab_locations},
    "Yellow Dam": {loc.name for loc in yellow_dam_locations},
    "Red Dam": {loc.name for loc in red_dam_locations},
    "Blue Dam": {loc.name for loc in blue_dam_locations},
    "Green Dam": {loc.name for loc in green_dam_locations},
    "Climatrol": {loc.name for loc in climatrol_locations},
    "Esper Mansion": {loc.name for loc in esper_mansion_locations},
    "Naval": {loc.name for loc in naval_locations},
    "Menobe": {loc.name for loc in menobe_locations},
    "Ikuto": {loc.name for loc in ikuto_locations},
    "Guaron": {loc.name for loc in guaron_locations},
    "Other": {
        loc.name
        for loc in uzo_locations
        + paseo_locations
        + oputa_locations
        + control_tower_locations
        + kueri_locations
        + gaira_locations
        + noah_locations
    },
}
