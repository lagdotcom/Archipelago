
from typing import NamedTuple, Optional

from BaseClasses import ItemClassification
from .Names import ItemName as I


class ItemData(NamedTuple):
    id: int
    name: str
    code: Optional[int]
    classification: ItemClassification
    gold_pieces: int = 0


key_items = [
    ItemData(517_9_088, I.RoyalTiara, 0x58, ItemClassification.progression),
    ItemData(517_9_095, I.DwarfKey, 0x5f, ItemClassification.progression),
    ItemData(517_9_096, I.RuneKey, 0x60, ItemClassification.progression),
    ItemData(517_9_097, I.FalseIdol, 0x61, ItemClassification.progression),
    ItemData(517_9_098, I.CellKey, 0x62, ItemClassification.progression),
    ItemData(517_9_099, I.MysticRope, 0x63, ItemClassification.progression),
    ItemData(517_9_112, I.OrbOfTruth, 0x70, ItemClassification.progression),
]


flag_items = [
    ItemData(518_9_300, I.TrialOfStrength, None,
             ItemClassification.progression),
    ItemData(518_9_301, I.TrialOfCourage, None,
             ItemClassification.progression),
    ItemData(518_9_302, I.TrialOfTruth, None, ItemClassification.progression),
    ItemData(518_9_303, I.TrialOfWisdom, None, ItemClassification.progression),

    ItemData(518_9_304, I.Gila, None, ItemClassification.progression),
    ItemData(518_9_305, I.Dai, None, ItemClassification.progression),
    ItemData(518_9_306, I.Jessa, None, ItemClassification.progression),

    ItemData(518_9_307, I.EnterLab3, None, ItemClassification.progression),

    ItemData(518_9_308, I.KaiserKrab, None, ItemClassification.progression),
    ItemData(518_9_309, I.Tortolyde, None, ItemClassification.progression),
    ItemData(518_9_310, I.Doppler, None, ItemClassification.progression),
    ItemData(518_9_311, I.ShellBeast, None, ItemClassification.progression),
    ItemData(518_9_312, I.DarkSol, None, ItemClassification.progression),
]


required_items = key_items + flag_items

unique_useful_items = [
    ItemData(517_9_113, I.VialOfTears, 0x71,
             ItemClassification.progression | ItemClassification.useful),
    ItemData(517_9_114, I.Medallion, 0x72,
             ItemClassification.progression | ItemClassification.useful),
]

equipment_items = [
    ItemData(517_9_000, 'Bronze Knife', 0x00, ItemClassification.useful),
    ItemData(517_9_001, 'Short Sword', 0x01, ItemClassification.useful),
    ItemData(517_9_002, 'Sword', 0x02, ItemClassification.useful),
    ItemData(517_9_003, 'Longsword', 0x03, ItemClassification.useful),
    ItemData(517_9_004, 'Broadsword', 0x04, ItemClassification.useful),
    ItemData(517_9_005, 'Fire Sword', 0x05, ItemClassification.useful),
    ItemData(517_9_006, 'Storm Sword', 0x06, ItemClassification.useful),
    ItemData(517_9_007, 'Light Blade', 0x07, ItemClassification.useful),
    ItemData(517_9_008, 'Dark Blade', 0x08, ItemClassification.useful),
    ItemData(517_9_009, 'Dream Blade', 0x09, ItemClassification.useful),
    ItemData(517_9_010, 'Bronze Saber', 0x0a, ItemClassification.useful),
    ItemData(517_9_011, 'Steel Saber', 0x0b, ItemClassification.useful),
    ItemData(517_9_012, 'Battle Hammer', 0x0c, ItemClassification.useful),
    ItemData(517_9_013, 'Mithril Axe', 0x0d, ItemClassification.useful),
    ItemData(517_9_014, 'Ice Saber', 0x0e, ItemClassification.useful),
    ItemData(517_9_015, 'Dark Scimitar', 0x0f, ItemClassification.useful),
    ItemData(517_9_016, 'Short Axe', 0x10, ItemClassification.useful),
    ItemData(517_9_017, 'Battle Axe', 0x11, ItemClassification.useful),
    ItemData(517_9_018, 'Double Axe', 0x12, ItemClassification.useful),
    ItemData(517_9_019, 'Great Axe', 0x13, ItemClassification.useful),
    ItemData(517_9_020, 'Mithril Sword', 0x14, ItemClassification.useful),
    ItemData(517_9_021, 'Wood Staff', 0x15, ItemClassification.useful),
    ItemData(517_9_022, 'Flail', 0x16, ItemClassification.useful),
    ItemData(517_9_023, 'Morningstar', 0x17, ItemClassification.useful),
    ItemData(517_9_024, 'Fire Staff', 0x18, ItemClassification.useful),
    ItemData(517_9_025, 'Ice Staff', 0x19, ItemClassification.useful),
    ItemData(517_9_026, 'Mercy Staff', 0x1a, ItemClassification.useful),
    ItemData(517_9_027, 'Endurostaff', 0x1b, ItemClassification.useful),
    ItemData(517_9_028, 'Doom Staff', 0x1c, ItemClassification.useful),
    ItemData(517_9_029, 'Mithril Rod', 0x1d, ItemClassification.useful),
    ItemData(517_9_030, 'Wooden Club', 0x1e, ItemClassification.useful),
    ItemData(517_9_031, 'War Hammer', 0x1f, ItemClassification.useful),
    ItemData(517_9_032, 'Bronze Lance', 0x20, ItemClassification.useful),
    ItemData(517_9_033, 'Iron Lance', 0x21, ItemClassification.useful),
    ItemData(517_9_034, 'Steel Lance', 0x22, ItemClassification.useful),
    ItemData(517_9_035, 'Short Spear', 0x23, ItemClassification.useful),
    ItemData(517_9_036, 'Long Spear', 0x24, ItemClassification.useful),
    ItemData(517_9_037, 'Bullwhip', 0x25, ItemClassification.useful),
    ItemData(517_9_038, 'Thorn Whip', 0x26, ItemClassification.useful),
    ItemData(517_9_039, 'Steel Whip', 0x27, ItemClassification.useful),
    ItemData(517_9_040, 'Hex Whip', 0x28, ItemClassification.useful),
    ItemData(517_9_041, 'Great Flail', 0x29, ItemClassification.useful),
    ItemData(517_9_042, 'Super Flail', 0x2a, ItemClassification.useful),
    ItemData(517_9_043, 'Doom Blade', 0x2b, ItemClassification.useful),
    ItemData(517_9_044, 'Wood Shield', 0x2c, ItemClassification.useful),
    ItemData(517_9_045, 'Dark Armor', 0x2d, ItemClassification.useful),
    ItemData(517_9_046, 'Frost Armor', 0x2e, ItemClassification.useful),
    ItemData(517_9_047, 'Thunder Armor', 0x2f, ItemClassification.useful),
    ItemData(517_9_048, 'Sun Armor', 0x30, ItemClassification.useful),
    ItemData(517_9_049, 'Cotton Robe', 0x31, ItemClassification.useful),
    ItemData(517_9_050, 'Woven Robe', 0x32, ItemClassification.useful),
    ItemData(517_9_051, 'Fur Robe', 0x33, ItemClassification.useful),
    ItemData(517_9_052, 'Worn Robe', 0x34, ItemClassification.useful),
    ItemData(517_9_053, 'Straw Robe', 0x35, ItemClassification.useful),
    ItemData(517_9_054, 'Hemp Robe', 0x36, ItemClassification.useful),
    ItemData(517_9_055, 'Leather Robe', 0x37, ItemClassification.useful),
    ItemData(517_9_056, 'Light Robe', 0x38, ItemClassification.useful),
    ItemData(517_9_057, 'Magic Robe', 0x39, ItemClassification.useful),
    ItemData(517_9_058, 'Dark Robe', 0x3a, ItemClassification.useful),
    ItemData(517_9_059, 'Leather Armor', 0x3b, ItemClassification.useful),
    ItemData(517_9_060, 'Chainmail', 0x3c, ItemClassification.useful),
    ItemData(517_9_061, 'Breastplate', 0x3d, ItemClassification.useful),
    ItemData(517_9_062, 'Bronze Armor', 0x3e, ItemClassification.useful),
    ItemData(517_9_063, 'Iron Armor', 0x3f, ItemClassification.useful),
    ItemData(517_9_064, 'Steel Armor', 0x40, ItemClassification.useful),
    ItemData(517_9_065, 'Mithril Armor', 0x41, ItemClassification.useful),
    ItemData(517_9_066, 'Light Armor', 0x42, ItemClassification.useful),
    ItemData(517_9_067, 'Bronze Shield', 0x43, ItemClassification.useful),
    ItemData(517_9_068, 'Iron Shield', 0x44, ItemClassification.useful),
    ItemData(517_9_069, 'Steel Shield', 0x45, ItemClassification.useful),
    ItemData(517_9_070, 'Leather Shield', 0x46, ItemClassification.useful),
    ItemData(517_9_071, 'Light Shield', 0x47, ItemClassification.useful),
    ItemData(517_9_072, 'Dark Shield', 0x48, ItemClassification.useful),
    ItemData(517_9_073, 'Mithril Shield', 0x49, ItemClassification.useful),
    ItemData(517_9_074, 'Elven Hood', 0x4a, ItemClassification.useful),
    ItemData(517_9_075, 'Cloth Hood', 0x4b, ItemClassification.useful),
    ItemData(517_9_076, 'Woven Hood', 0x4c, ItemClassification.useful),
    ItemData(517_9_077, 'Fur Hood', 0x4d, ItemClassification.useful),
    ItemData(517_9_078, 'Magic Hood', 0x4e, ItemClassification.useful),
    ItemData(517_9_079, 'Dark Hood', 0x4f, ItemClassification.useful),
    ItemData(517_9_080, 'Mithril Hood', 0x50, ItemClassification.useful),
    ItemData(517_9_081, 'Leather Helm', 0x51, ItemClassification.useful),
    ItemData(517_9_082, 'Bronze Helm', 0x52, ItemClassification.useful),
    ItemData(517_9_083, 'Iron Helm', 0x53, ItemClassification.useful),
    ItemData(517_9_084, 'Steel Helm', 0x54, ItemClassification.useful),
    ItemData(517_9_085, 'Light Helm', 0x55, ItemClassification.useful),
    ItemData(517_9_086, 'Dark Helm', 0x56, ItemClassification.useful),
    ItemData(517_9_087, 'Mithril Helm', 0x57, ItemClassification.useful),
    ItemData(517_9_089, 'Magic Shield', 0x59, ItemClassification.useful),
    ItemData(517_9_090, 'Magic Mail', 0x5a, ItemClassification.useful),
    ItemData(517_9_108, 'Forbidden Box', 0x6c, ItemClassification.useful),
    ItemData(517_9_118, 'Main Gauche', 0x76, ItemClassification.useful),
    ItemData(517_9_119, 'Madu', 0x77, ItemClassification.useful),
    ItemData(517_9_120, 'Earth Hammer', 0x78, ItemClassification.useful),
    ItemData(517_9_121, 'Shock Box', 0x79, ItemClassification.useful),
    ItemData(517_9_122, 'Ogre Flute', 0x7a, ItemClassification.useful),
    ItemData(517_9_123, 'Black Box', 0x7b, ItemClassification.useful),
    ItemData(517_9_124, 'Gauntlet', 0x7c, ItemClassification.useful),
    ItemData(517_9_125, 'Demon Staff', 0x7e, ItemClassification.useful),
]

crafting_items = [
    ItemData(517_9_101, 'Mithril Ore', 0x65, ItemClassification.useful),
    ItemData(517_9_105, 'Dark Block', 0x69, ItemClassification.useful),
]

useful_items = unique_useful_items + equipment_items + crafting_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(517_9_091, 'Herb', 0x5b, ItemClassification.filler),
    ItemData(517_9_092, 'Depoison', 0x5c, ItemClassification.filler),
    ItemData(517_9_093, 'Angel Feather', 0x5d, ItemClassification.filler),
    ItemData(517_9_094, 'Wisdom Seed', 0x5e, ItemClassification.filler),
    ItemData(517_9_100, 'Tamayoshi', 0x64, ItemClassification.filler),
    ItemData(517_9_102, 'Heal Ring', 0x66, ItemClassification.filler),
    ItemData(517_9_104, 'Barrier Ring', 0x67, ItemClassification.filler),
    ItemData(517_9_105, I.MagicRing, 0x68, ItemClassification.filler),
    ItemData(517_9_107, 'Magic Mirror', 0x6a, ItemClassification.filler),
    ItemData(517_9_108, 'Herb Water', 0x6b, ItemClassification.filler),
    ItemData(517_9_110, 'Holy Water', 0x6d, ItemClassification.filler),
    ItemData(517_9_111, 'Healer Fruit', 0x6e, ItemClassification.filler),
    ItemData(517_9_112, 'Smelling Salts', 0x6f, ItemClassification.filler),
    ItemData(517_9_117, 'Miracle Herb', 0x75, ItemClassification.filler),
]

junk_items = [
    ItemData(517_9_115, 'Map 1', 0x73, ItemClassification.filler |
             ItemClassification.deprioritized),
    ItemData(517_9_116, 'Map 2', 0x74, ItemClassification.filler |
             ItemClassification.deprioritized),
    ItemData(517_9_125, 'Glass Armor', 0x7d,
             ItemClassification.filler | ItemClassification.deprioritized),
]

gold_items = [
    ItemData(517_9_400, '50g', 0x80, ItemClassification.filler |
             ItemClassification.deprioritized, 50),
    ItemData(517_9_401, '100g', 0x81, ItemClassification.filler |
             ItemClassification.deprioritized, 100),
    ItemData(517_9_402, '200g', 0x82, ItemClassification.filler |
             ItemClassification.deprioritized, 200),
    ItemData(517_9_403, '400g', 0x83, ItemClassification.filler |
             ItemClassification.deprioritized, 400),
    ItemData(517_9_404, '800g', 0x84, ItemClassification.filler |
             ItemClassification.deprioritized, 800),
    ItemData(517_9_405, '1000g', 0x85, ItemClassification.filler |
             ItemClassification.deprioritized, 1000),
    ItemData(517_9_406, '2000g', 0x86, ItemClassification.filler |
             ItemClassification.deprioritized, 2000),
]

# TODO
trap_items = [
    ItemData(517_9_500, 'Chest Beak', 0x87, ItemClassification.trap),
    ItemData(517_9_501, 'Ghost', 0x88, ItemClassification.trap),
    ItemData(517_9_502, 'Hand Eater', 0x89, ItemClassification.trap),
]

filler_items = consumable_items + junk_items + gold_items
filler_item_names = [item.name for item in filler_items]

reward_item_names = [
    I.DwarfKey,
    I.Medallion,
    I.MagicRing,
    I.VialOfTears,
]

item_name_groups = {
    'Key Items': {item.name for item in key_items},
    'Unique and Useful': {item.name for item in unique_useful_items},
    'Equipment': {item.name for item in equipment_items},
    'Crafting': {item.name for item in crafting_items},
    'Consumables': {item.name for item in consumable_items},
    'Junk': {item.name for item in junk_items},
    'Quest Flags': {item.name for item in flag_items}
}

all_items = required_items + useful_items + filler_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}
