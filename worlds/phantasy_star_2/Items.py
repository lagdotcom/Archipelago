from enum import Enum
from typing import NamedTuple, Optional

from BaseClasses import ItemClassification as IC

from .Constants import jet_scooter_flag, spaceship_flag
from .Data import Item as I
from .Data.Types import EquipSlot as S
from .laglib import IntSpan


class ItemType(Enum):
    GARBAGE = 0
    ITEM = 1
    MONEY = 2
    FLAG = 3
    FLAG_AS_ITEM = 4


class ItemData(NamedTuple):
    id: int
    type: ItemType
    slot: S
    name: str
    code: Optional[int]
    classification: IC
    meseta: int = 0
    ram_flag: Optional[IntSpan] = None
    ram_value: int = 1

    def get_chest_bytes(self):
        if self.name == I.Garbage:
            return (0).to_bytes(2, "big")
        elif self.meseta > 0:
            return (self.meseta & 0x7FFF).to_bytes(2, "big")
        elif self.code is not None:
            return (0x8000 | self.code).to_bytes(2, "big")
        else:
            raise Exception(f"Item {self.name} cannot be placed in chest!")


key_items = [
    ItemData(452_1_001, ItemType.ITEM, S.NONE, I.SmallKey, 0x1, IC.progression),
    ItemData(452_1_002, ItemType.ITEM, S.NONE, I.Dynamite, 0x2, IC.progression),
    ItemData(452_1_003, ItemType.ITEM, S.NONE, I.KeyTube, 0x3, IC.progression),
    ItemData(452_1_004, ItemType.ITEM, S.NONE, I.MarueraGum, 0x4, IC.progression),
    ItemData(452_1_005, ItemType.ITEM, S.NONE, I.GreenCard, 0x5, IC.progression),
    ItemData(452_1_006, ItemType.ITEM, S.NONE, I.BlueCard, 0x6, IC.progression),
    ItemData(452_1_007, ItemType.ITEM, S.NONE, I.YellowCard, 0x7, IC.progression),
    ItemData(452_1_008, ItemType.ITEM, S.NONE, I.RedCard, 0x8, IC.progression),
    ItemData(452_1_009, ItemType.ITEM, S.NONE, I.Letter, 0x9, IC.progression),
    ItemData(452_1_010, ItemType.ITEM, S.NONE, I.Recorder, 0xA, IC.progression),
    ItemData(452_1_011, ItemType.ITEM, S.NONE, I.MarueraLeaf, 0xB, IC.progression),
    ItemData(452_1_013, ItemType.ITEM, S.NONE, I.Prism, 0xD, IC.progression),
    ItemData(452_1_039, ItemType.ITEM, S.HEAD, I.NeiMet, 0x27, IC.progression),
    ItemData(452_1_040, ItemType.ITEM, S.HEAD, I.NeiCrown, 0x28, IC.progression),
    ItemData(452_1_061, ItemType.ITEM, S.BODY, I.NeiArmor, 0x3D, IC.progression),
    ItemData(452_1_062, ItemType.ITEM, S.BODY, I.NeiCape, 0x3E, IC.progression),
    ItemData(452_1_084, ItemType.ITEM, S.HAND, I.NeiShield, 0x54, IC.progression),
    ItemData(452_1_085, ItemType.ITEM, S.HAND, I.NeiEmel, 0x55, IC.progression),
    # this isn't actually needed, but good luck beating Dark Force without it
    ItemData(452_1_108, ItemType.ITEM, S.TWO_HAND, I.NeiSword, 0x6C, IC.progression),
    ItemData(452_1_109, ItemType.ITEM, S.HAND, I.NeiSlasher, 0x6D, IC.progression),
    ItemData(452_1_122, ItemType.ITEM, S.TWO_HAND, I.NeiShot, 0x7A, IC.progression),
    ItemData(452_1_124, ItemType.ITEM, S.NONE, I.Teim, 0x7C, IC.progression),
]

flag_items = [
    ItemData(452_9_000, ItemType.FLAG, S.NONE, I.MusikFlag, None, IC.progression),
    ItemData(
        452_9_001,
        ItemType.FLAG_AS_ITEM,
        S.NONE,
        I.JetScooterFlag,
        0xE1,
        IC.progression,
        0,
        jet_scooter_flag,
        2,
    ),
    ItemData(452_9_002, ItemType.FLAG, S.NONE, I.NeifirstFlag, None, IC.progression),
    ItemData(452_9_003, ItemType.FLAG, S.NONE, I.RedDamFlag, None, IC.progression),
    ItemData(452_9_004, ItemType.FLAG, S.NONE, I.YellowDamFlag, None, IC.progression),
    ItemData(452_9_005, ItemType.FLAG, S.NONE, I.BlueDamFlag, None, IC.progression),
    ItemData(452_9_006, ItemType.FLAG, S.NONE, I.GreenDamFlag, None, IC.progression),
    ItemData(
        452_9_007,
        ItemType.FLAG_AS_ITEM,
        S.NONE,
        I.SpaceshipFlag,
        0xE2,
        IC.progression,
        0,
        spaceship_flag,
    ),
    ItemData(452_9_008, ItemType.FLAG, S.NONE, I.WinTheGameFlag, None, IC.progression),
]


required_items = key_items + flag_items


unique_useful_items = [
    ItemData(452_1_042, ItemType.ITEM, S.HEAD, I.MogicCap, 0x2A, IC.useful),
    ItemData(452_1_125, ItemType.ITEM, S.NONE, I.Visiphone, 0x7D, IC.useful),
]

equipment_items = [
    ItemData(452_1_023, ItemType.ITEM, S.HEAD, I.Headgear, 0x17, IC.useful),
    ItemData(452_1_024, ItemType.ITEM, S.HEAD, I.Ribbon, 0x18, IC.useful),
    ItemData(452_1_025, ItemType.ITEM, S.HEAD, I.FiberGear, 0x19, IC.useful),
    ItemData(452_1_026, ItemType.ITEM, S.HEAD, I.SilRibbon, 0x1A, IC.useful),
    ItemData(452_1_027, ItemType.ITEM, S.HEAD, I.SilCrown, 0x1B, IC.useful),
    ItemData(452_1_028, ItemType.ITEM, S.HEAD, I.TitaniGear, 0x1C, IC.useful),
    ItemData(452_1_029, ItemType.ITEM, S.HEAD, I.TitaniMet, 0x1D, IC.useful),
    ItemData(452_1_030, ItemType.ITEM, S.HEAD, I.JwlCrown, 0x1E, IC.useful),
    ItemData(452_1_031, ItemType.ITEM, S.HEAD, I.JwlRibbon, 0x1F, IC.useful),
    ItemData(452_1_032, ItemType.ITEM, S.HEAD, I.CresceGear, 0x20, IC.useful),
    ItemData(452_1_033, ItemType.ITEM, S.HEAD, I.SnowCrown, 0x21, IC.useful),
    ItemData(452_1_034, ItemType.ITEM, S.HEAD, I.WindScarf, 0x22, IC.useful),
    ItemData(452_1_035, ItemType.ITEM, S.HEAD, I.ColorScarf, 0x23, IC.useful),
    ItemData(452_1_036, ItemType.ITEM, S.HEAD, I.StormGear, 0x24, IC.useful),
    ItemData(452_1_037, ItemType.ITEM, S.HEAD, I.Laconigear, 0x25, IC.useful),
    ItemData(452_1_038, ItemType.ITEM, S.HEAD, I.LaconiaMet, 0x26, IC.useful),
    ItemData(452_1_043, ItemType.ITEM, S.BODY, I.CarbonSuit, 0x2B, IC.useful),
    ItemData(452_1_044, ItemType.ITEM, S.BODY, I.CarbonVest, 0x2C, IC.useful),
    ItemData(452_1_045, ItemType.ITEM, S.BODY, I.FiberCoat, 0x2D, IC.useful),
    ItemData(452_1_046, ItemType.ITEM, S.BODY, I.FiberCape, 0x2E, IC.useful),
    ItemData(452_1_047, ItemType.ITEM, S.BODY, I.FiberVest, 0x2F, IC.useful),
    ItemData(452_1_048, ItemType.ITEM, S.BODY, I.TtnmArmor, 0x30, IC.useful),
    ItemData(452_1_049, ItemType.ITEM, S.BODY, I.TtnmCape, 0x31, IC.useful),
    ItemData(452_1_050, ItemType.ITEM, S.BODY, I.TtnmChest, 0x32, IC.useful),
    ItemData(452_1_051, ItemType.ITEM, S.BODY, I.CrmcArmor, 0x33, IC.useful),
    ItemData(452_1_052, ItemType.ITEM, S.BODY, I.CrmcCape, 0x34, IC.useful),
    ItemData(452_1_053, ItemType.ITEM, S.BODY, I.CrmcChest, 0x35, IC.useful),
    ItemData(452_1_054, ItemType.ITEM, S.BODY, I.AmberRobe, 0x36, IC.useful),
    ItemData(452_1_055, ItemType.ITEM, S.BODY, I.Crystanish, 0x37, IC.useful),
    ItemData(452_1_056, ItemType.ITEM, S.BODY, I.CrystCape, 0x38, IC.useful),
    ItemData(452_1_057, ItemType.ITEM, S.BODY, I.CrystChest, 0x39, IC.useful),
    ItemData(452_1_058, ItemType.ITEM, S.BODY, I.Laconinish, 0x3A, IC.useful),
    ItemData(452_1_059, ItemType.ITEM, S.BODY, I.LaconCape, 0x3B, IC.useful),
    ItemData(452_1_060, ItemType.ITEM, S.BODY, I.LaconChest, 0x3C, IC.useful),
    ItemData(452_1_063, ItemType.ITEM, S.FEET, I.Shoes, 0x3F, IC.useful),
    ItemData(452_1_064, ItemType.ITEM, S.FEET, I.Sandals, 0x40, IC.useful),
    ItemData(452_1_065, ItemType.ITEM, S.FEET, I.Boots, 0x41, IC.useful),
    ItemData(452_1_066, ItemType.ITEM, S.FEET, I.KnifeBoots, 0x42, IC.useful),
    ItemData(452_1_067, ItemType.ITEM, S.FEET, I.LongBoots, 0x43, IC.useful),
    ItemData(452_1_068, ItemType.ITEM, S.FEET, I.HirzaBoots, 0x44, IC.useful),
    ItemData(452_1_069, ItemType.ITEM, S.FEET, I.ShuneBoots, 0x45, IC.useful),
    ItemData(452_1_070, ItemType.ITEM, S.FEET, I.GardaBoots, 0x46, IC.useful),
    ItemData(452_1_071, ItemType.ITEM, S.HAND, I.CrbnShield, 0x47, IC.useful),
    ItemData(452_1_072, ItemType.ITEM, S.HAND, I.CrbnEmel, 0x48, IC.useful),
    ItemData(452_1_073, ItemType.ITEM, S.HAND, I.FibrShild, 0x49, IC.useful),
    ItemData(452_1_074, ItemType.ITEM, S.HAND, I.FiberEmel, 0x4A, IC.useful),
    ItemData(452_1_075, ItemType.ITEM, S.HAND, I.MirShield, 0x4B, IC.useful),
    ItemData(452_1_076, ItemType.ITEM, S.HAND, I.MirEmel, 0x4C, IC.useful),
    ItemData(452_1_077, ItemType.ITEM, S.HAND, I.CerShield, 0x4D, IC.useful),
    ItemData(452_1_078, ItemType.ITEM, S.HAND, I.CerEmel, 0x4E, IC.useful),
    ItemData(452_1_079, ItemType.ITEM, S.HAND, I.Aegis, 0x4F, IC.useful),
    ItemData(452_1_080, ItemType.ITEM, S.HAND, I.GrSleeves, 0x50, IC.useful),
    ItemData(452_1_081, ItemType.ITEM, S.HAND, I.TruthSlvs, 0x51, IC.useful),
    ItemData(452_1_082, ItemType.ITEM, S.HAND, I.LaconEmel, 0x52, IC.useful),
    ItemData(452_1_083, ItemType.ITEM, S.HAND, I.LacShield, 0x53, IC.useful),
    ItemData(452_1_086, ItemType.ITEM, S.HAND, I.Knife, 0x56, IC.useful),
    ItemData(452_1_087, ItemType.ITEM, S.HAND, I.Dagger, 0x57, IC.useful),
    ItemData(452_1_088, ItemType.ITEM, S.HAND, I.Scalpel, 0x58, IC.useful),
    ItemData(452_1_089, ItemType.ITEM, S.HAND, I.SteelBar, 0x59, IC.useful),
    ItemData(452_1_090, ItemType.ITEM, S.HAND, I.Boomerang, 0x5A, IC.useful),
    ItemData(452_1_091, ItemType.ITEM, S.HAND, I.Slasher, 0x5B, IC.useful),
    ItemData(452_1_092, ItemType.ITEM, S.TWO_HAND, I.Sword, 0x5C, IC.useful),
    ItemData(452_1_093, ItemType.ITEM, S.HAND, I.Whip, 0x5D, IC.useful),
    ItemData(452_1_094, ItemType.ITEM, S.TWO_HAND, I.CeramSwrd, 0x5E, IC.useful),
    ItemData(452_1_095, ItemType.ITEM, S.HAND, I.CeramKnfe, 0x5F, IC.useful),
    ItemData(452_1_096, ItemType.ITEM, S.HAND, I.CeramBar, 0x60, IC.useful),
    ItemData(452_1_097, ItemType.ITEM, S.HAND, I.LasrSlshr, 0x61, IC.useful),
    ItemData(452_1_098, ItemType.ITEM, S.TWO_HAND, I.LasrSword, 0x62, IC.useful),
    ItemData(452_1_099, ItemType.ITEM, S.HAND, I.LaserBar, 0x63, IC.useful),
    ItemData(452_1_100, ItemType.ITEM, S.HAND, I.LaserKnfe, 0x64, IC.useful),
    ItemData(452_1_101, ItemType.ITEM, S.TWO_HAND, I.SwdOfAng, 0x65, IC.useful),
    ItemData(452_1_102, ItemType.ITEM, S.HAND, I.FireSlshr, 0x66, IC.useful),
    ItemData(452_1_103, ItemType.ITEM, S.HAND, I.FireStaff, 0x67, IC.useful),
    ItemData(452_1_104, ItemType.ITEM, S.HAND, I.LacnMace, 0x68, IC.useful),
    ItemData(452_1_105, ItemType.ITEM, S.HAND, I.LacDagger, 0x69, IC.useful),
    ItemData(452_1_106, ItemType.ITEM, S.HAND, I.ACSlashr, 0x6A, IC.useful),
    ItemData(452_1_107, ItemType.ITEM, S.TWO_HAND, I.LacSword, 0x6B, IC.useful),
    ItemData(452_1_110, ItemType.ITEM, S.TWO_HAND, I.BowGun, 0x6E, IC.useful),
    ItemData(452_1_111, ItemType.ITEM, S.HAND, I.SonicGun, 0x6F, IC.useful),
    ItemData(452_1_112, ItemType.ITEM, S.TWO_HAND, I.Shotgun, 0x70, IC.useful),
    ItemData(452_1_113, ItemType.ITEM, S.TWO_HAND, I.SilentShot, 0x71, IC.useful),
    ItemData(452_1_114, ItemType.ITEM, S.HAND, I.PoisonShot, 0x72, IC.useful),
    ItemData(452_1_115, ItemType.ITEM, S.HAND, I.AcidShot, 0x73, IC.useful),
    ItemData(452_1_116, ItemType.ITEM, S.TWO_HAND, I.Cannon, 0x74, IC.useful),
    ItemData(452_1_117, ItemType.ITEM, S.TWO_HAND, I.Vulcan, 0x75, IC.useful),
    ItemData(452_1_118, ItemType.ITEM, S.TWO_HAND, I.LaserShot, 0x76, IC.useful),
    ItemData(452_1_119, ItemType.ITEM, S.TWO_HAND, I.LsrCannon, 0x77, IC.useful),
    ItemData(452_1_120, ItemType.ITEM, S.TWO_HAND, I.PlsCannon, 0x78, IC.useful),
    ItemData(452_1_121, ItemType.ITEM, S.TWO_HAND, I.PulseVlcn, 0x79, IC.useful),
]

useful_items = unique_useful_items + equipment_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(452_1_014, ItemType.ITEM, S.NONE, I.Telepipe, 0xE, IC.filler),
    ItemData(452_1_015, ItemType.ITEM, S.NONE, I.Escapipe, 0xF, IC.filler),
    ItemData(452_1_016, ItemType.ITEM, S.NONE, I.Hidapipe, 0x10, IC.filler),
    ItemData(452_1_017, ItemType.ITEM, S.NONE, I.Monomate, 0x11, IC.filler),
    ItemData(452_1_018, ItemType.ITEM, S.NONE, I.Dimate, 0x12, IC.filler),
    ItemData(452_1_019, ItemType.ITEM, S.NONE, I.Trimate, 0x13, IC.filler),
    ItemData(452_1_020, ItemType.ITEM, S.NONE, I.Antidote, 0x14, IC.filler),
    ItemData(452_1_021, ItemType.ITEM, S.NONE, I.StarMist, 0x15, IC.filler),
    ItemData(452_1_022, ItemType.ITEM, S.NONE, I.MoonDew, 0x16, IC.filler),
]

junk_items = [
    ItemData(452_1_012, ItemType.ITEM, S.NONE, I.PlasmaRing, 0xC, IC.filler),
    ItemData(452_1_041, ItemType.ITEM, S.HEAD, I.MagicCap, 0x29, IC.filler),
    ItemData(452_1_123, ItemType.ITEM, S.BODY, I.PrsnClths, 0x7B, IC.filler),
    ItemData(452_2_000, ItemType.GARBAGE, S.NONE, I.Garbage, None, IC.filler),
]

meseta_items = [
    ItemData(452_2_001, ItemType.MONEY, S.NONE, I.Meseta(20), None, IC.filler, 20),
    ItemData(452_2_002, ItemType.MONEY, S.NONE, I.Meseta(40), None, IC.filler, 40),
    ItemData(452_2_003, ItemType.MONEY, S.NONE, I.Meseta(60), None, IC.filler, 60),
    ItemData(452_2_004, ItemType.MONEY, S.NONE, I.Meseta(100), None, IC.filler, 100),
    ItemData(452_2_005, ItemType.MONEY, S.NONE, I.Meseta(150), None, IC.filler, 150),
    ItemData(452_2_006, ItemType.MONEY, S.NONE, I.Meseta(200), None, IC.filler, 200),
    ItemData(452_2_007, ItemType.MONEY, S.NONE, I.Meseta(5600), None, IC.filler, 5600),
    ItemData(452_2_008, ItemType.MONEY, S.NONE, I.Meseta(6400), None, IC.filler, 6400),
    ItemData(452_2_009, ItemType.MONEY, S.NONE, I.Meseta(7800), None, IC.filler, 7800),
    ItemData(452_2_010, ItemType.MONEY, S.NONE, I.Meseta(8600), None, IC.filler, 8600),
    ItemData(
        452_2_011,
        ItemType.MONEY,
        S.NONE,
        I.Meseta(12000),
        None,
        IC.filler,
        12000,
    ),
    ItemData(
        452_2_012,
        ItemType.MONEY,
        S.NONE,
        I.Meseta(15000),
        None,
        IC.filler,
        15000,
    ),
    ItemData(
        452_2_013,
        ItemType.MONEY,
        S.NONE,
        I.Meseta(18000),
        None,
        IC.filler,
        18000,
    ),
]

filler_items = consumable_items + junk_items + meseta_items
filler_item_names = [item.name for item in filler_items]

item_name_groups = {
    "Key Items": {item.name for item in key_items},
    "Unique and Useful": {item.name for item in unique_useful_items},
    "Equipment": {item.name for item in equipment_items},
    "Consumables": {item.name for item in consumable_items},
    "Junk": {item.name for item in junk_items},
    "Quest Flags": {item.name for item in flag_items},
}

all_items = required_items + useful_items + filler_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}
