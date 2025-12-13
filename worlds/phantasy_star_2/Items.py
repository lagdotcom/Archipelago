from enum import Enum
from typing import NamedTuple, Optional

from BaseClasses import ItemClassification as IC

from .Constants import jet_scooter_flag, spaceship_flag
from .Data import Item as I
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
    ItemData(452_1_001, ItemType.ITEM, I.SmallKey, 0x1, IC.progression),
    ItemData(452_1_002, ItemType.ITEM, I.Dynamite, 0x2, IC.progression),
    ItemData(452_1_003, ItemType.ITEM, I.KeyTube, 0x3, IC.progression),
    ItemData(452_1_004, ItemType.ITEM, I.MarueraGum, 0x4, IC.progression),
    ItemData(452_1_005, ItemType.ITEM, I.GreenCard, 0x5, IC.progression),
    ItemData(452_1_006, ItemType.ITEM, I.BlueCard, 0x6, IC.progression),
    ItemData(452_1_007, ItemType.ITEM, I.YellowCard, 0x7, IC.progression),
    ItemData(452_1_008, ItemType.ITEM, I.RedCard, 0x8, IC.progression),
    ItemData(452_1_009, ItemType.ITEM, I.Letter, 0x9, IC.progression),
    ItemData(452_1_010, ItemType.ITEM, I.Recorder, 0xA, IC.progression),
    ItemData(452_1_011, ItemType.ITEM, I.MarueraLeaf, 0xB, IC.progression),
    ItemData(452_1_013, ItemType.ITEM, I.Prism, 0xD, IC.progression),
    ItemData(452_1_039, ItemType.ITEM, I.NeiMet, 0x27, IC.progression),
    ItemData(452_1_040, ItemType.ITEM, I.NeiCrown, 0x28, IC.progression),
    ItemData(452_1_061, ItemType.ITEM, I.NeiArmor, 0x3D, IC.progression),
    ItemData(452_1_062, ItemType.ITEM, I.NeiCape, 0x3E, IC.progression),
    ItemData(452_1_084, ItemType.ITEM, I.NeiShield, 0x54, IC.progression),
    ItemData(452_1_085, ItemType.ITEM, I.NeiEmel, 0x55, IC.progression),
    # this isn't actually needed, but good luck beating Dark Force without it
    ItemData(452_1_108, ItemType.ITEM, I.NeiSword, 0x6C, IC.progression),
    ItemData(452_1_109, ItemType.ITEM, I.NeiSlasher, 0x6D, IC.progression),
    ItemData(452_1_122, ItemType.ITEM, I.NeiShot, 0x7A, IC.progression),
    ItemData(452_1_124, ItemType.ITEM, I.Teim, 0x7C, IC.progression),
]

flag_items = [
    ItemData(452_9_000, ItemType.FLAG, I.MusikFlag, None, IC.progression),
    ItemData(
        452_9_001,
        ItemType.FLAG_AS_ITEM,
        I.JetScooterFlag,
        0xE1,
        IC.progression,
        0,
        jet_scooter_flag,
        2,
    ),
    ItemData(452_9_002, ItemType.FLAG, I.NeifirstFlag, None, IC.progression),
    ItemData(452_9_003, ItemType.FLAG, I.RedDamFlag, None, IC.progression),
    ItemData(452_9_004, ItemType.FLAG, I.YellowDamFlag, None, IC.progression),
    ItemData(452_9_005, ItemType.FLAG, I.BlueDamFlag, None, IC.progression),
    ItemData(452_9_006, ItemType.FLAG, I.GreenDamFlag, None, IC.progression),
    ItemData(
        452_9_007,
        ItemType.FLAG_AS_ITEM,
        I.SpaceshipFlag,
        0xE2,
        IC.progression,
        0,
        spaceship_flag,
    ),
    ItemData(452_9_008, ItemType.FLAG, I.WinTheGameFlag, None, IC.progression),
]


required_items = key_items + flag_items


unique_useful_items = [
    ItemData(452_1_042, ItemType.ITEM, I.MogicCap, 0x2A, IC.useful),
    ItemData(452_1_125, ItemType.ITEM, I.Visiphone, 0x7D, IC.useful),
]

equipment_items = [
    ItemData(452_1_023, ItemType.ITEM, I.Headgear, 0x17, IC.useful),
    ItemData(452_1_024, ItemType.ITEM, I.Ribbon, 0x18, IC.useful),
    ItemData(452_1_025, ItemType.ITEM, I.Fibergear, 0x19, IC.useful),
    ItemData(452_1_026, ItemType.ITEM, I.SilRibbon, 0x1A, IC.useful),
    ItemData(452_1_027, ItemType.ITEM, I.SilCrown, 0x1B, IC.useful),
    ItemData(452_1_028, ItemType.ITEM, I.Titanigear, 0x1C, IC.useful),
    ItemData(452_1_029, ItemType.ITEM, I.Titanimet, 0x1D, IC.useful),
    ItemData(452_1_030, ItemType.ITEM, I.JwlCrown, 0x1E, IC.useful),
    ItemData(452_1_031, ItemType.ITEM, I.JwlRibbon, 0x1F, IC.useful),
    ItemData(452_1_032, ItemType.ITEM, I.CresceGear, 0x20, IC.useful),
    ItemData(452_1_033, ItemType.ITEM, I.SnowCrown, 0x21, IC.useful),
    ItemData(452_1_034, ItemType.ITEM, I.WindScarf, 0x22, IC.useful),
    ItemData(452_1_035, ItemType.ITEM, I.ColorScarf, 0x23, IC.useful),
    ItemData(452_1_036, ItemType.ITEM, I.StormGear, 0x24, IC.useful),
    ItemData(452_1_037, ItemType.ITEM, I.Laconigear, 0x25, IC.useful),
    ItemData(452_1_038, ItemType.ITEM, I.LaconiaMet, 0x26, IC.useful),
    ItemData(452_1_043, ItemType.ITEM, I.CarbonSuit, 0x2B, IC.useful),
    ItemData(452_1_044, ItemType.ITEM, I.CarbonVest, 0x2C, IC.useful),
    ItemData(452_1_045, ItemType.ITEM, I.FiberCoat, 0x2D, IC.useful),
    ItemData(452_1_046, ItemType.ITEM, I.FiberCape, 0x2E, IC.useful),
    ItemData(452_1_047, ItemType.ITEM, I.FiberVest, 0x2F, IC.useful),
    ItemData(452_1_048, ItemType.ITEM, I.TtnmArmor, 0x30, IC.useful),
    ItemData(452_1_049, ItemType.ITEM, I.TtnmCape, 0x31, IC.useful),
    ItemData(452_1_050, ItemType.ITEM, I.TtnmChest, 0x32, IC.useful),
    ItemData(452_1_051, ItemType.ITEM, I.CrmcArmor, 0x33, IC.useful),
    ItemData(452_1_052, ItemType.ITEM, I.CrmcCape, 0x34, IC.useful),
    ItemData(452_1_053, ItemType.ITEM, I.CrmcChest, 0x35, IC.useful),
    ItemData(452_1_054, ItemType.ITEM, I.AmberRobe, 0x36, IC.useful),
    ItemData(452_1_055, ItemType.ITEM, I.Crystanish, 0x37, IC.useful),
    ItemData(452_1_056, ItemType.ITEM, I.CrystCape, 0x38, IC.useful),
    ItemData(452_1_057, ItemType.ITEM, I.CrystChest, 0x39, IC.useful),
    ItemData(452_1_058, ItemType.ITEM, I.Laconinish, 0x3A, IC.useful),
    ItemData(452_1_059, ItemType.ITEM, I.LaconCape, 0x3B, IC.useful),
    ItemData(452_1_060, ItemType.ITEM, I.LaconChest, 0x3C, IC.useful),
    ItemData(452_1_063, ItemType.ITEM, I.Shoes, 0x3F, IC.useful),
    ItemData(452_1_064, ItemType.ITEM, I.Sandals, 0x40, IC.useful),
    ItemData(452_1_065, ItemType.ITEM, I.Boots, 0x41, IC.useful),
    ItemData(452_1_066, ItemType.ITEM, I.KnifeBoots, 0x42, IC.useful),
    ItemData(452_1_067, ItemType.ITEM, I.LongBoots, 0x43, IC.useful),
    ItemData(452_1_068, ItemType.ITEM, I.HirzaBoots, 0x44, IC.useful),
    ItemData(452_1_069, ItemType.ITEM, I.ShuneBoots, 0x45, IC.useful),
    ItemData(452_1_070, ItemType.ITEM, I.GardaBoots, 0x46, IC.useful),
    ItemData(452_1_071, ItemType.ITEM, I.CrbnShield, 0x47, IC.useful),
    ItemData(452_1_072, ItemType.ITEM, I.CrbnEmel, 0x48, IC.useful),
    ItemData(452_1_073, ItemType.ITEM, I.FibrShield, 0x49, IC.useful),
    ItemData(452_1_074, ItemType.ITEM, I.FiberEmel, 0x4A, IC.useful),
    ItemData(452_1_075, ItemType.ITEM, I.MirShield, 0x4B, IC.useful),
    ItemData(452_1_076, ItemType.ITEM, I.MirEmel, 0x4C, IC.useful),
    ItemData(452_1_077, ItemType.ITEM, I.CerShield, 0x4D, IC.useful),
    ItemData(452_1_078, ItemType.ITEM, I.CerEmel, 0x4E, IC.useful),
    ItemData(452_1_079, ItemType.ITEM, I.Aegis, 0x4F, IC.useful),
    ItemData(452_1_080, ItemType.ITEM, I.GrSleeves, 0x50, IC.useful),
    ItemData(452_1_081, ItemType.ITEM, I.TruthSlvs, 0x51, IC.useful),
    ItemData(452_1_082, ItemType.ITEM, I.LaconEmel, 0x52, IC.useful),
    ItemData(452_1_083, ItemType.ITEM, I.LacShield, 0x53, IC.useful),
    ItemData(452_1_086, ItemType.ITEM, I.Knife, 0x56, IC.useful),
    ItemData(452_1_087, ItemType.ITEM, I.Dagger, 0x57, IC.useful),
    ItemData(452_1_088, ItemType.ITEM, I.Scalpel, 0x58, IC.useful),
    ItemData(452_1_089, ItemType.ITEM, I.SteelBar, 0x59, IC.useful),
    ItemData(452_1_090, ItemType.ITEM, I.Boomerang, 0x5A, IC.useful),
    ItemData(452_1_091, ItemType.ITEM, I.Slasher, 0x5B, IC.useful),
    ItemData(452_1_092, ItemType.ITEM, I.Sword, 0x5C, IC.useful),
    ItemData(452_1_093, ItemType.ITEM, I.Whip, 0x5D, IC.useful),
    ItemData(452_1_094, ItemType.ITEM, I.CrmcSword, 0x5E, IC.useful),
    ItemData(452_1_095, ItemType.ITEM, I.CeramKnife, 0x5F, IC.useful),
    ItemData(452_1_096, ItemType.ITEM, I.CeramBar, 0x60, IC.useful),
    ItemData(452_1_097, ItemType.ITEM, I.LasrSlshr, 0x61, IC.useful),
    ItemData(452_1_098, ItemType.ITEM, I.LasrSword, 0x62, IC.useful),
    ItemData(452_1_099, ItemType.ITEM, I.LaserBar, 0x63, IC.useful),
    ItemData(452_1_100, ItemType.ITEM, I.LaserKnife, 0x64, IC.useful),
    ItemData(452_1_101, ItemType.ITEM, I.SwdOfAng, 0x65, IC.useful),
    ItemData(452_1_102, ItemType.ITEM, I.FireSlshr, 0x66, IC.useful),
    ItemData(452_1_103, ItemType.ITEM, I.FireStaff, 0x67, IC.useful),
    ItemData(452_1_104, ItemType.ITEM, I.LacnMace, 0x68, IC.useful),
    ItemData(452_1_105, ItemType.ITEM, I.LacDagger, 0x69, IC.useful),
    ItemData(452_1_106, ItemType.ITEM, I.ACSlashr, 0x6A, IC.useful),
    ItemData(452_1_107, ItemType.ITEM, I.LacSword, 0x6B, IC.useful),
    ItemData(452_1_110, ItemType.ITEM, I.Bowgun, 0x6E, IC.useful),
    ItemData(452_1_111, ItemType.ITEM, I.SonicGun, 0x6F, IC.useful),
    ItemData(452_1_112, ItemType.ITEM, I.Shotgun, 0x70, IC.useful),
    ItemData(452_1_113, ItemType.ITEM, I.SilentShot, 0x71, IC.useful),
    ItemData(452_1_114, ItemType.ITEM, I.PoisonShot, 0x72, IC.useful),
    ItemData(452_1_115, ItemType.ITEM, I.AcidShot, 0x73, IC.useful),
    ItemData(452_1_116, ItemType.ITEM, I.Cannon, 0x74, IC.useful),
    ItemData(452_1_117, ItemType.ITEM, I.Vulcan, 0x75, IC.useful),
    ItemData(452_1_118, ItemType.ITEM, I.LaserShot, 0x76, IC.useful),
    ItemData(452_1_119, ItemType.ITEM, I.LsrCannon, 0x77, IC.useful),
    ItemData(452_1_120, ItemType.ITEM, I.PlsCannon, 0x78, IC.useful),
    ItemData(452_1_121, ItemType.ITEM, I.PulseVlcn, 0x79, IC.useful),
]

useful_items = unique_useful_items + equipment_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(452_1_014, ItemType.ITEM, I.Telepipe, 0xE, IC.filler),
    ItemData(452_1_015, ItemType.ITEM, I.Escapipe, 0xF, IC.filler),
    ItemData(452_1_016, ItemType.ITEM, I.Hidapipe, 0x10, IC.filler),
    ItemData(452_1_017, ItemType.ITEM, I.Monomate, 0x11, IC.filler),
    ItemData(452_1_018, ItemType.ITEM, I.Dimate, 0x12, IC.filler),
    ItemData(452_1_019, ItemType.ITEM, I.Trimate, 0x13, IC.filler),
    ItemData(452_1_020, ItemType.ITEM, I.Antidote, 0x14, IC.filler),
    ItemData(452_1_021, ItemType.ITEM, I.StarMist, 0x15, IC.filler),
    ItemData(452_1_022, ItemType.ITEM, I.MoonDew, 0x16, IC.filler),
]

junk_items = [
    ItemData(452_1_012, ItemType.ITEM, I.PlsmRing, 0xC, IC.filler),
    ItemData(452_1_041, ItemType.ITEM, I.MagicCap, 0x29, IC.filler),
    ItemData(452_1_123, ItemType.ITEM, I.PrsnClths, 0x7B, IC.filler),
    # ItemData(452_1_126, 'Unknown1', 0x7E, IC.filler),
    # ItemData(452_1_127, 'Unknown2', 0x7F, IC.filler),
    ItemData(452_2_000, ItemType.GARBAGE, I.Garbage, 0, IC.filler),
]

meseta_items = [
    ItemData(452_2_001, ItemType.MONEY, I.Meseta(20), None, IC.filler, 20),
    ItemData(452_2_002, ItemType.MONEY, I.Meseta(40), None, IC.filler, 40),
    ItemData(452_2_003, ItemType.MONEY, I.Meseta(60), None, IC.filler, 60),
    ItemData(452_2_004, ItemType.MONEY, I.Meseta(100), None, IC.filler, 100),
    ItemData(452_2_005, ItemType.MONEY, I.Meseta(150), None, IC.filler, 150),
    ItemData(452_2_006, ItemType.MONEY, I.Meseta(200), None, IC.filler, 200),
    ItemData(452_2_007, ItemType.MONEY, I.Meseta(5600), None, IC.filler, 5600),
    ItemData(452_2_008, ItemType.MONEY, I.Meseta(6400), None, IC.filler, 6400),
    ItemData(452_2_009, ItemType.MONEY, I.Meseta(7800), None, IC.filler, 7800),
    ItemData(452_2_010, ItemType.MONEY, I.Meseta(8600), None, IC.filler, 8600),
    ItemData(452_2_011, ItemType.MONEY, I.Meseta(12000), None, IC.filler, 12000),
    ItemData(452_2_012, ItemType.MONEY, I.Meseta(15000), None, IC.filler, 15000),
    ItemData(452_2_013, ItemType.MONEY, I.Meseta(18000), None, IC.filler, 18000),
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
