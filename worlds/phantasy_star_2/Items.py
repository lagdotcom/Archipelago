
from typing import NamedTuple, Optional

from BaseClasses import ItemClassification as IC

from .Data import Item as I


class ItemData(NamedTuple):
    id: int
    name: str
    code: Optional[int]
    classification: IC
    meseta: int = 0
    pool_quantity: int = 1


key_items = [
    ItemData(452_1_001, I.SmallKey, 0x1, IC.progression),
    ItemData(452_1_002, I.Dynamite, 0x2, IC.progression, 0, 3),
    ItemData(452_1_003, I.KeyTube, 0x3, IC.progression),
    ItemData(452_1_004, I.MruraGum, 0x4, IC.progression),
    ItemData(452_1_005, I.GreenCard, 0x5, IC.progression),
    ItemData(452_1_006, I.BlueCard, 0x6, IC.progression),
    ItemData(452_1_007, I.YellowCard, 0x7, IC.progression),
    ItemData(452_1_008, I.RedCard, 0x8, IC.progression),
    ItemData(452_1_009, I.Letter, 0x9, IC.progression),
    ItemData(452_1_010, I.Recorder, 0xA, IC.progression),
    ItemData(452_1_011, I.MruraLeaf, 0xB, IC.progression),
    ItemData(452_1_013, I.Prism, 0xD, IC.progression),

    ItemData(452_1_039, I.NeiMet, 0x27, IC.progression),
    ItemData(452_1_040, I.NeiCrown, 0x28, IC.progression),
    ItemData(452_1_061, I.NeiArmor, 0x3D, IC.progression),
    ItemData(452_1_062, I.NeiCape, 0x3E, IC.progression),
    ItemData(452_1_084, I.NeiShield, 0x54, IC.progression),
    ItemData(452_1_085, I.NeiEmel, 0x55, IC.progression),
    # TODO is this actually needed?
    ItemData(452_1_108, I.NeiSword, 0x6C, IC.progression),
    ItemData(452_1_109, I.NeiSlasher, 0x6D, IC.progression),
    ItemData(452_1_122, I.NeiShot, 0x7A, IC.progression),

    ItemData(452_1_124, I.Teim, 0x7C, IC.progression),
]

flag_items = [
    ItemData(452_9_000, I.MusikFlag, None, IC.progression),
    ItemData(452_9_001, I.JetScooterFlag, None, IC.progression),
    ItemData(452_9_002, I.NeifirstFlag, None, IC.progression),
    ItemData(452_9_003, I.RedDamFlag, None, IC.progression),
    ItemData(452_9_004, I.YellowDamFlag, None, IC.progression),
    ItemData(452_9_005, I.BlueDamFlag, None, IC.progression),
    ItemData(452_9_006, I.GreenDamFlag, None, IC.progression),
    ItemData(452_9_007, I.SpaceshipFlag, None, IC.progression),
    ItemData(452_9_008, I.WinTheGameFlag, None, IC.progression),
]


required_items = key_items + flag_items


unique_useful_items = [
    ItemData(452_1_042, 'MogicCap', 0x2A, IC.useful),
    ItemData(452_1_125, 'Visiphone', 0x7D, IC.useful),
]

equipment_items = [

    ItemData(452_1_023, 'Headgear', 0x17, IC.useful),
    ItemData(452_1_024, 'Ribbon', 0x18, IC.useful),
    ItemData(452_1_025, 'Fibergear', 0x19, IC.useful),
    ItemData(452_1_026, 'SilRibbon', 0x1A, IC.useful),
    ItemData(452_1_027, 'SilCrown', 0x1B, IC.useful),
    ItemData(452_1_028, 'Titanigear', 0x1C, IC.useful),
    ItemData(452_1_029, 'Titanimet', 0x1D, IC.useful),
    ItemData(452_1_030, 'JwlCrown', 0x1E, IC.useful),
    ItemData(452_1_031, 'JwlRibbon', 0x1F, IC.useful),
    ItemData(452_1_032, 'Crescegear', 0x20, IC.useful),
    ItemData(452_1_033, 'SnowCrown', 0x21, IC.useful),
    ItemData(452_1_034, 'WindScarf', 0x22, IC.useful),
    ItemData(452_1_035, 'ColorScarf', 0x23, IC.useful),
    ItemData(452_1_036, 'StormGear', 0x24, IC.useful),
    ItemData(452_1_037, 'Laconigear', 0x25, IC.useful),
    ItemData(452_1_038, 'Laconimet', 0x26, IC.useful),


    ItemData(452_1_043, 'CarbonSuit', 0x2B, IC.useful),
    ItemData(452_1_044, 'CarbonVest', 0x2C, IC.useful),
    ItemData(452_1_045, 'FiberCoat', 0x2D, IC.useful),
    ItemData(452_1_046, 'FiberCape', 0x2E, IC.useful),
    ItemData(452_1_047, 'FiberVest', 0x2F, IC.useful),
    ItemData(452_1_048, 'TtnmArmor', 0x30, IC.useful),
    ItemData(452_1_049, 'TtnmCape', 0x31, IC.useful),
    ItemData(452_1_050, 'TtnmChest', 0x32, IC.useful),
    ItemData(452_1_051, 'CrmcArmor', 0x33, IC.useful),
    ItemData(452_1_052, 'CrmcCape', 0x34, IC.useful),
    ItemData(452_1_053, 'CrmcChest', 0x35, IC.useful),
    ItemData(452_1_054, 'AmberRobe', 0x36, IC.useful),
    ItemData(452_1_055, 'Crystanish', 0x37, IC.useful),
    ItemData(452_1_056, 'CrystCape', 0x38, IC.useful),
    ItemData(452_1_057, 'CrystChest', 0x39, IC.useful),
    ItemData(452_1_058, 'Laconinish', 0x3A, IC.useful),
    ItemData(452_1_059, 'LaconCape', 0x3B, IC.useful),
    ItemData(452_1_060, 'LaconChest', 0x3C, IC.useful),

    ItemData(452_1_063, 'Shoes', 0x3F, IC.useful),
    ItemData(452_1_064, 'Sandals', 0x40, IC.useful),
    ItemData(452_1_065, 'Boots', 0x41, IC.useful),
    ItemData(452_1_066, 'KnifeBoots', 0x42, IC.useful),
    ItemData(452_1_067, 'LongBoots', 0x43, IC.useful),
    ItemData(452_1_068, 'HirzaBoots', 0x44, IC.useful),
    ItemData(452_1_069, 'ShuneBoots', 0x45, IC.useful),
    ItemData(452_1_070, 'GardaBoots', 0x46, IC.useful),

    ItemData(452_1_071, 'CrbnShield', 0x47, IC.useful),
    ItemData(452_1_072, 'CrbnEmel', 0x48, IC.useful),
    ItemData(452_1_073, 'FibrShield', 0x49, IC.useful),
    ItemData(452_1_074, 'FiberEmel', 0x4A, IC.useful),
    ItemData(452_1_075, 'MirShield', 0x4B, IC.useful),
    ItemData(452_1_076, 'MirEmel', 0x4C, IC.useful),
    ItemData(452_1_077, 'CerShield', 0x4D, IC.useful),
    ItemData(452_1_078, 'CerEmel', 0x4E, IC.useful),
    ItemData(452_1_079, 'Aegis', 0x4F, IC.useful),
    ItemData(452_1_080, 'GrSleeves', 0x50, IC.useful),
    ItemData(452_1_081, 'TruthSlvs', 0x51, IC.useful),
    ItemData(452_1_082, 'LaconEmel', 0x52, IC.useful),
    ItemData(452_1_083, 'LacShield', 0x53, IC.useful),

    ItemData(452_1_086, 'Knife', 0x56, IC.useful),
    ItemData(452_1_087, 'Dagger', 0x57, IC.useful),
    ItemData(452_1_088, 'Scalpel', 0x58, IC.useful),
    ItemData(452_1_089, 'SteelBar', 0x59, IC.useful),
    ItemData(452_1_090, 'Boomerang', 0x5A, IC.useful),
    ItemData(452_1_091, 'Slasher', 0x5B, IC.useful),
    ItemData(452_1_092, 'Sword', 0x5C, IC.useful),
    ItemData(452_1_093, 'Whip', 0x5D, IC.useful),
    ItemData(452_1_094, 'CrmcSword', 0x5E, IC.useful),
    ItemData(452_1_095, 'CeramKnife', 0x5F, IC.useful),
    ItemData(452_1_096, 'CeramBar', 0x60, IC.useful),
    ItemData(452_1_097, 'LasrSlshr', 0x61, IC.useful),
    ItemData(452_1_098, 'LasrSword', 0x62, IC.useful),
    ItemData(452_1_099, 'LaserBar', 0x63, IC.useful),
    ItemData(452_1_100, 'LaserKnife', 0x64, IC.useful),
    ItemData(452_1_101, 'SwdOfAnger', 0x65, IC.useful),
    ItemData(452_1_102, 'FireSlshr', 0x66, IC.useful),
    ItemData(452_1_103, 'FireStaff', 0x67, IC.useful),
    ItemData(452_1_104, 'LacnMace', 0x68, IC.useful),
    ItemData(452_1_105, 'LacDagger', 0x69, IC.useful),
    ItemData(452_1_106, 'AcSlasher', 0x6A, IC.useful),
    ItemData(452_1_107, 'LacSword', 0x6B, IC.useful),
    ItemData(452_1_110, 'Bowgun', 0x6E, IC.useful),
    ItemData(452_1_111, 'SonicGun', 0x6F, IC.useful),
    ItemData(452_1_112, 'Shotgun', 0x70, IC.useful),
    ItemData(452_1_113, 'SilentShot', 0x71, IC.useful),
    ItemData(452_1_114, 'PoisonShot', 0x72, IC.useful),
    ItemData(452_1_115, 'AcidShot', 0x73, IC.useful),
    ItemData(452_1_116, 'Cannon', 0x74, IC.useful),
    ItemData(452_1_117, 'Vulcan', 0x75, IC.useful),
    ItemData(452_1_118, 'LaserShot', 0x76, IC.useful),
    ItemData(452_1_119, 'LsrCannon', 0x77, IC.useful),
    ItemData(452_1_120, 'PlsCannon', 0x78, IC.useful),
    ItemData(452_1_121, 'PulseVlcn', 0x79, IC.useful),
]

useful_items = unique_useful_items + equipment_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(452_1_014, 'Telepipe', 0xE, IC.filler),
    ItemData(452_1_015, 'Escapipe', 0xF, IC.filler),
    ItemData(452_1_016, 'Hidapipe', 0x10, IC.filler),

    ItemData(452_1_017, 'Monomate', 0x11, IC.filler),
    ItemData(452_1_018, 'Dimate', 0x12, IC.filler),
    ItemData(452_1_019, 'Trimate', 0x13, IC.filler),
    ItemData(452_1_020, 'Antidote', 0x14, IC.filler),
    ItemData(452_1_021, 'StarMist', 0x15, IC.filler),
    ItemData(452_1_022, 'MoonDew', 0x16, IC.filler),
]

junk_items = [
    ItemData(452_1_012, 'PlsmRing', 0xC, IC.filler),
    ItemData(452_1_041, 'MagicCap', 0x29, IC.filler),
    ItemData(452_1_123, 'PrsnClths', 0x7B, IC.filler),
    # ItemData(452_1_126, 'Unknown1', 0x7E, IC.filler),
    # ItemData(452_1_127, 'Unknown2', 0x7F, IC.filler),

    ItemData(452_2_000, 'Garbage', 0, IC.filler),
]

meseta_items = [
    ItemData(452_2_001, '20 Meseta', None, IC.filler, 20),
    ItemData(452_2_002, '40 Meseta', None, IC.filler, 40),
    ItemData(452_2_003, '60 Meseta', None, IC.filler, 60),
    ItemData(452_2_004, '100 Meseta', None, IC.filler, 100),
    ItemData(452_2_005, '150 Meseta', None, IC.filler, 150),
    ItemData(452_2_006, '200 Meseta', None, IC.filler, 200),
    ItemData(452_2_007, '5600 Meseta', None, IC.filler, 5600),
    ItemData(452_2_008, '6400 Meseta', None, IC.filler, 6400),
    ItemData(452_2_009, '7800 Meseta', None, IC.filler, 7800),
    ItemData(452_2_010, '8600 Meseta', None, IC.filler, 8600),
    ItemData(452_2_011, '12000 Meseta', None, IC.filler, 12000),
    ItemData(452_2_012, '15000 Meseta', None, IC.filler, 15000),
    ItemData(452_2_013, '18000 Meseta', None, IC.filler, 18000),
]

filler_items = consumable_items + junk_items + meseta_items
filler_item_names = [item.name for item in filler_items]

item_name_groups = {
    'Key Items': {item.name for item in key_items},
    'Unique and Useful': {item.name for item in unique_useful_items},
    'Equipment': {item.name for item in equipment_items},
    'Consumables': {item.name for item in consumable_items},
    'Junk': {item.name for item in junk_items},
    'Quest Flags': {item.name for item in flag_items}
}

all_items = required_items + useful_items + filler_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}
