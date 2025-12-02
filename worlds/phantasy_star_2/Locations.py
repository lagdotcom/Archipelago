from typing import NamedTuple, Optional

from .laglib import (
    genesis_ram as RAM,
    genesis_rom as ROM,
    IntSpan,
    MemoryManager,
    Predicate,
)
from .Constants import (
    TREASURE_CHEST_CONTENT_ARRAY,
    chest_flags,
    game_mode,
)
from .Data import Area as A, Item as I
from .Enums import GameMode
from .Items import ItemType


class FlagCheck(NamedTuple):
    span: IntSpan
    predicate: Predicate[int]

    def __repr__(self):
        return repr(self.span) + "?"

    def test(self, mem: MemoryManager):
        value = self.span.get(mem)
        return self.predicate(value)


equals1: Predicate[int] = lambda v: v == 1


class LocationData:
    type: str
    id: int
    region_name: str
    name: str
    vanilla_item: str
    rom_location: Optional[IntSpan] = None
    fixed_item: Optional[str] = None
    checks: list[FlagCheck]
    required_items: Optional[set[str]] = None
    restricted_types: set[ItemType]

    def __init__(
        self,
        type: str,
        id: int,
        region_name: str,
        name: str,
        vanilla_item: str,
        restricted_types: set[ItemType],
    ):
        self.type = type
        self.id = id
        self.region_name = region_name
        self.name = name
        self.vanilla_item = vanilla_item
        self.restricted_types = restricted_types
        self.checks = []

    def at(self, span: IntSpan):
        self.rom_location = span
        return self

    def fix(self, item_name: str):
        self.fixed_item = item_name
        return self

    def flag(self, address: int, predicate: Predicate[int] = equals1):
        self.checks.append(FlagCheck(IntSpan(RAM, address, 1), predicate))
        return self

    def requires(self, required_items: set[str]):
        self.required_items = required_items
        return self


def chest(id: int, region_name: str, name: str, chest_index: int, vanilla_item: str):
    return (
        LocationData(
            "chest",
            id,
            region_name,
            name,
            vanilla_item,
            {ItemType.GARBAGE, ItemType.ITEM, ItemType.MONEY},
        )
        .at(IntSpan(ROM, TREASURE_CHEST_CONTENT_ARRAY + chest_index * 2, 2))
        .flag(chest_flags.address + chest_index)
    )


def flag(
    id: int,
    region_name: str,
    name: str,
    vanilla_item: str,
    ram_location: int,
    predicate: Predicate[int] = equals1,
):
    return LocationData(
        "flag", id, region_name, name, vanilla_item, {ItemType.FLAG}
    ).flag(ram_location, predicate)


def granted(
    id: int,
    region_name: str,
    name: str,
    vanilla_item: str,
    rom_address: int,
    ram_address: int,
    predicate: Predicate[int] = equals1,
):
    return (
        LocationData("granted", id, region_name, name, vanilla_item, {ItemType.ITEM})
        .at(IntSpan(ROM, rom_address, 1))
        .flag(ram_address, predicate)
    )


skure_locations = [
    chest(452_00_01, A.Dezolis, "Skure - 15000 meseta", 0x1, I.Meseta(15000)),
    chest(452_00_02, A.Dezolis, "Skure - MogicCap", 0x2, I.MogicCap),
    chest(452_00_03, A.Dezolis, "Skure - 18000 meseta", 0x3, I.Meseta(18000)),
    chest(452_00_04, A.Dezolis, "Skure - MagicCap", 0x4, I.MagicCap),
    chest(452_00_05, A.Dezolis, "Skure - 7800 meseta", 0x5, I.Meseta(7800)),
    chest(452_00_06, A.Dezolis, "Skure - LaconChest", 0x6, I.LaconChest),
    chest(452_00_07, A.Dezolis, "Skure - 5600 meseta", 0x7, I.Meseta(5600)),
    chest(452_00_08, A.Dezolis, "Skure - GardaBoots", 0x8, I.GardaBoots),
    chest(452_00_09, A.Dezolis, "Skure - 8600 meseta", 0x9, I.Meseta(8600)),
    chest(452_00_10, A.Dezolis, "Skure - MagicCap 2", 0xA, I.MagicCap),
    chest(452_00_11, A.Dezolis, "Skure - 12000 meseta", 0xB, I.Meseta(12000)),
    chest(452_00_12, A.Dezolis, "Skure - 6400 meseta", 0xC, I.Meseta(6400)),
]

esper_mansion_locations = [
    chest(452_00_14, A.Dezolis, "Esper Mansion - Prism", 0xE, I.Prism).flag(
        0xC743, lambda v: v == 3
    ),
    chest(452_00_15, A.Dezolis, "Esper Mansion - NeiSword", 0xF, I.NeiSword)
    .flag(0xC744, lambda v: v == 1)
    .requires(
        {
            I.NeiArmor,
            I.NeiCape,
            I.NeiCrown,
            I.NeiEmel,
            I.NeiMet,
            I.NeiShield,
            I.NeiShot,
            I.NeiSlasher,
        }
    ),
]

shure_locations = [
    chest(452_00_16, A.ShureLockedChests, "Shure Locked - Monomate", 0x10, I.Monomate),
    chest(
        452_00_17, A.ShureLockedChests, "Shure Locked - 150 meseta", 0x11, I.Meseta(150)
    ),
    chest(452_00_18, A.ShureLockedChests, "Shure Locked - Dynamite", 0x12, I.Dynamite),
    chest(
        452_00_19, A.ShureLockedChests, "Shure Locked - Dynamite 2", 0x13, I.Dynamite
    ),
    chest(452_00_20, A.Shure, "Shure - 40 meseta", 0x14, I.Meseta(40)),
    chest(452_00_21, A.Shure, "Shure - Dimate", 0x15, I.Dimate),
    chest(452_00_22, A.Shure, "Shure - Headgear", 0x16, I.Headgear),
    chest(452_00_23, A.Shure, "Shure - 200 meseta", 0x17, I.Meseta(200)),
    chest(452_00_24, A.Shure, "Shure - SilRibbon", 0x18, I.SilRibbon),
    granted(
        452_01_01,
        A.Shure,
        "Shure - Small Key",
        I.SmallKey,
        0xDBE3,
        0xC721,
        lambda v: v >= 1,
    ),
    granted(
        452_01_02, A.Shure, "Shure - Letter", I.Letter, 0xDBF3, 0xC721, lambda v: v >= 2
    ),
]

nido_locations = [
    chest(452_00_25, A.Nido, "Nido - 20 meseta", 0x19, I.Meseta(20)),
    chest(452_00_26, A.Nido, "Nido - 100 meseta", 0x1A, I.Meseta(100)),
    chest(452_00_27, A.Nido, "Nido - Dimate", 0x1B, I.Dimate),
    chest(452_00_28, A.Nido, "Nido - Trimate", 0x1C, I.Trimate),
    chest(452_00_29, A.Nido, "Nido - 60 meseta", 0x1D, I.Meseta(60)),
    granted(452_01_03, A.Nido, "Nido - Teim", I.Teim, 0xDC6D, 0xC727).requires(
        {I.Letter}
    ),
]

roron_locations = [
    chest(452_00_30, A.Roron, "Roron - Garbage", 0x1E, I.Garbage),
    chest(452_00_31, A.Roron, "Roron - Garbage 2", 0x1F, I.Garbage),
    chest(452_00_32, A.Roron, "Roron - CeramBar", 0x20, I.CeramBar),
    chest(452_00_33, A.Roron, "Roron - Garbage 3", 0x21, I.Garbage),
    chest(452_00_34, A.Roron, "Roron - Cannon", 0x22, I.Cannon),
    chest(452_00_35, A.Roron, "Roron - Garbage 4", 0x23, I.Garbage),
    flag(452_02_00, A.Roron, "Roron - Jet Scooter Guy", I.JetScooterFlag, 0xC716).fix(
        I.JetScooterFlag
    ),
]

yellow_dam_locations = [
    chest(452_00_36, A.YellowDam, "Yellow Dam - Escapipe", 0x24, I.Escapipe),
    chest(452_00_37, A.YellowDam, "Yellow Dam - Crystanish", 0x25, I.Crystanish),
    chest(452_00_38, A.YellowDam, "Yellow Dam - CrystCape", 0x26, I.CrystCape),
    chest(452_00_39, A.YellowDam, "Yellow Dam - CrystChest", 0x27, I.CrystChest),
    chest(452_00_40, A.YellowDam, "Yellow Dam - AmberRobe", 0x28, I.AmberRobe),
    flag(452_02_01, A.YellowDam, "Yellow Dam - Console", I.YellowDamFlag, 0xC731).fix(
        I.YellowDamFlag
    ),
]

red_dam_locations = [
    chest(452_00_41, A.RedDam, "Red Dam - SwdOfAnger", 0x29, I.SwdOfAng),
    chest(452_00_42, A.RedDam, "Red Dam - FireSlshr", 0x2A, I.FireSlshr),
    chest(452_00_43, A.RedDam, "Red Dam - FireStaff", 0x2B, I.FireStaff),
    flag(452_02_02, A.RedDam, "Red Dam - Console", I.RedDamFlag, 0xC733).fix(
        I.RedDamFlag
    ),
]

blue_dam_locations = [
    chest(452_00_44, A.BlueDam, "Blue Dam - Antidote", 0x2C, I.Antidote),
    chest(452_00_45, A.BlueDam, "Blue Dam - CresceGear", 0x2D, I.CresceGear),
    chest(452_00_46, A.BlueDam, "Blue Dam - SnowCrown", 0x2E, I.SnowCrown),
    chest(452_00_47, A.BlueDam, "Blue Dam - StarMist", 0x2F, I.StarMist),
    chest(452_00_48, A.BlueDam, "Blue Dam - WindScarf", 0x30, I.WindScarf),
    chest(452_00_49, A.BlueDam, "Blue Dam - ColorScarf", 0x31, I.ColorScarf),
    chest(452_00_50, A.BlueDam, "Blue Dam - Trimate", 0x32, I.Trimate),
    chest(452_00_51, A.BlueDam, "Blue Dam - StormGear", 0x33, I.StormGear),
    flag(452_02_03, A.BlueDam, "Blue Dam - Console", I.BlueDamFlag, 0xC72F).fix(
        I.BlueDamFlag
    ),
]

green_dam_locations = [
    chest(452_00_52, A.GreenDam, "Green Dam - StarMist", 0x34, I.StarMist),
    chest(452_00_53, A.GreenDam, "Green Dam - Aegis", 0x35, I.Aegis),
    chest(452_00_54, A.GreenDam, "Green Dam - Telepipe", 0x36, I.Telepipe),
    chest(452_00_55, A.GreenDam, "Green Dam - GrSleeves", 0x37, I.GrSleeves),
    chest(452_00_56, A.GreenDam, "Green Dam - TruthSlvs", 0x38, I.TruthSlvs),
    flag(452_02_04, A.GreenDam, "Green Dam - Console", I.GreenDamFlag, 0xC72D).fix(
        I.GreenDamFlag
    ),
]

bio_systems_lab_locations = [
    chest(452_00_57, A.BioSystemsLab, "Bio-Systems Lab - Trimate", 0x39, I.Trimate),
    chest(452_00_58, A.BioSystemsLab, "Bio-Systems Lab - Antidote", 0x3A, I.Antidote),
    chest(
        452_00_59, A.BioSystemsLab, "Bio-Systems Lab - PoisonShot", 0x3B, I.PoisonShot
    ),
    chest(452_00_60, A.BioSystemsLab, "Bio-Systems Lab - Antidote 2", 0x3C, I.Antidote),
    chest(452_00_61, A.BioSystemsLab, "Bio-Systems Lab - Scalpel", 0x3D, I.Scalpel),
    chest(452_00_62, A.BioSystemsLab, "Bio-Systems Lab - StarMist", 0x3E, I.StarMist),
    chest(452_00_63, A.BioSystemsLab, "Bio-Systems Lab - Dynamite", 0x3F, I.Dynamite),
    granted(
        452_01_04,
        A.BioSystemsLabBasement,
        "Bio-Systems Lab - Recorder",
        I.Recorder,
        0xDBFD,
        0xC722,
    ),
]

climatrol_locations = [
    chest(452_00_64, A.Climatrol, "Climatrol - JwlRibbon", 0x40, I.JwlRibbon),
    chest(452_00_65, A.Climatrol, "Climatrol - FiberVest", 0x41, I.FiberVest),
    chest(452_00_66, A.Climatrol, "Climatrol - KnifeBoots", 0x42, I.KnifeBoots),
    chest(452_00_67, A.Climatrol, "Climatrol - SilRibbon", 0x43, I.SilRibbon),
    chest(452_00_68, A.Climatrol, "Climatrol - Sandals", 0x44, I.Sandals),
    chest(452_00_69, A.Climatrol, "Climatrol - LaserBar", 0x45, I.LaserBar),
    chest(452_00_70, A.Climatrol, "Climatrol - CeramBar", 0x46, I.CeramBar),
    flag(452_02_05, A.Climatrol, "Climatrol - Neifirst", I.NeifirstFlag, 0xC735).fix(
        I.NeifirstFlag
    ),
    # beating Neifirst immediately sets c710=3 and c737=1
    # after the 'Nei is really dead' scene, sets c710=4 and c711=3
    # the later scenes set all kinds of c710/1 values as it progresses
]

naval_locations = [
    chest(452_00_71, A.DezolisDungeons, "Naval - NeiShield", 0x47, I.NeiShield),
    chest(452_00_72, A.DezolisDungeons, "Naval - NeiEmel", 0x48, I.NeiEmel),
    chest(452_00_73, A.DezolisDungeons, "Naval - TruthSlvs", 0x49, I.TruthSlvs),
    chest(452_00_74, A.DezolisDungeons, "Naval - Trimate", 0x4A, I.Trimate),
    chest(452_00_75, A.DezolisDungeons, "Naval - MirEmel", 0x4B, I.MirEmel),
    chest(452_00_76, A.DezolisDungeons, "Naval - LaconEmel", 0x4C, I.LaconEmel),
    chest(452_00_77, A.DezolisDungeons, "Naval - GrSleeves", 0x4D, I.GrSleeves),
]

menobe_locations = [
    chest(452_00_78, A.DezolisDungeons, "Menobe - NeiCrown", 0x4E, I.NeiCrown),
    chest(452_00_79, A.DezolisDungeons, "Menobe - StormGear", 0x4F, I.StormGear),
    chest(452_00_80, A.DezolisDungeons, "Menobe - NeiMet", 0x50, I.NeiMet),
    chest(452_00_81, A.DezolisDungeons, "Menobe - ColorScarf", 0x51, I.ColorScarf),
]

ikuto_locations = [
    chest(452_00_82, A.DezolisDungeons, "Ikuto - NeiSlasher", 0x52, I.NeiSlasher),
    chest(452_00_83, A.DezolisDungeons, "Ikuto - NeiShot", 0x53, I.NeiShot),
    chest(452_00_84, A.DezolisDungeons, "Ikuto - FireStaff", 0x54, I.FireStaff),
    chest(452_00_85, A.DezolisDungeons, "Ikuto - LacnMace", 0x55, I.LacnMace),
    chest(452_00_86, A.DezolisDungeons, "Ikuto - PlsCannon", 0x56, I.PlsCannon),
    chest(452_00_87, A.DezolisDungeons, "Ikuto - LacDagger", 0x57, I.LacDagger),
]

guaron_locations = [
    chest(452_00_88, A.DezolisDungeons, "Guaron - AmberRobe", 0x58, I.AmberRobe),
    chest(452_00_89, A.DezolisDungeons, "Guaron - Laconinish", 0x59, I.Laconinish),
    chest(452_00_90, A.DezolisDungeons, "Guaron - CrystChest", 0x5A, I.CrystChest),
    chest(452_00_91, A.DezolisDungeons, "Guaron - NeiCape", 0x5B, I.NeiCape),
    chest(452_00_92, A.DezolisDungeons, "Guaron - CrystCape", 0x5C, I.CrystCape),
    chest(452_00_93, A.DezolisDungeons, "Guaron - NeiArmor", 0x5D, I.NeiArmor),
]

uzo_locations = [
    granted(452_01_05, A.Uzo, "Uzo - Maruera Tree", I.MarueraLeaf, 0xDBAD, 0xC720),
]

paseo_locations = [
    granted(
        452_01_06,
        A.Motavia,
        "Paseo - Give Recorder to Governor",
        I.KeyTube,
        0xC4D1,
        0xC750,
    ).requires({I.Recorder})
]


oputa_locations = [
    flag(452_02_06, A.Oputa, "Oputa - Ustvestia", I.MusikFlag, 0xC751).fix(I.MusikFlag)
]

control_tower_locations = [
    # TODO all four card locations are handled by one function; split somehow?
    flag(
        452_01_07, A.ControlTower, "Control Tower - Green Card", I.GreenCard, 0xC723
    ).fix(I.GreenCard),
    flag(
        452_01_08, A.ControlTower, "Control Tower - Blue Card", I.BlueCard, 0xC724
    ).fix(I.BlueCard),
    flag(
        452_01_09, A.ControlTower, "Control Tower - Yellow Card", I.YellowCard, 0xC725
    ).fix(I.YellowCard),
    flag(452_01_10, A.ControlTower, "Control Tower - Red Card", I.RedCard, 0xC726).fix(
        I.RedCard
    ),
]

kueri_locations = [
    granted(
        452_01_11,
        A.Kueri,
        "Kueri - Give Maruera Leaf to Researcher",
        I.MarueraGum,
        0xC94F,
        0xC752,
    ).requires({I.MarueraLeaf}),
]

gaira_locations = [
    flag(452_02_07, A.Gaira, "Gaira - Console", I.SpaceshipFlag, 0xC73F).fix(
        I.SpaceshipFlag
    ),
]

noah_locations = [
    flag(
        452_02_08,
        A.Noah,
        "Noah - Mother Brain",
        I.WinTheGameFlag,
        game_mode.address,
        lambda v: GameMode(v) == GameMode.ENDING,
    ).fix(I.WinTheGameFlag),
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
