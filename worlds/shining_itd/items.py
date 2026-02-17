from typing import NamedTuple

from BaseClasses import ItemClassification

from .Names import item_name as i


class ItemData(NamedTuple):
    id: int
    name: str
    code: int | None
    classification: ItemClassification
    gold_pieces: int = 0


key_items = [
    ItemData(517_9_088, i.RoyalTiara, 0x58, ItemClassification.progression),
    ItemData(517_9_095, i.DwarfKey, 0x5F, ItemClassification.progression),
    ItemData(517_9_096, i.RuneKey, 0x60, ItemClassification.progression),
    ItemData(517_9_097, i.FalseIdol, 0x61, ItemClassification.progression),
    ItemData(517_9_098, i.CellKey, 0x62, ItemClassification.progression),
    ItemData(517_9_099, i.MysticRope, 0x63, ItemClassification.progression),
    ItemData(517_9_112, i.OrbOfTruth, 0x70, ItemClassification.progression),
]


flag_items = [
    ItemData(518_9_300, i.TrialOfStrength, None, ItemClassification.progression),
    ItemData(518_9_301, i.TrialOfCourage, None, ItemClassification.progression),
    ItemData(518_9_302, i.TrialOfTruth, None, ItemClassification.progression),
    ItemData(518_9_303, i.TrialOfWisdom, None, ItemClassification.progression),
    ItemData(518_9_304, i.Gila, None, ItemClassification.progression),
    ItemData(518_9_305, i.Dai, None, ItemClassification.progression),
    ItemData(518_9_306, i.Jessa, None, ItemClassification.progression),
    ItemData(518_9_307, i.EnterLab3, None, ItemClassification.progression),
    ItemData(518_9_308, i.KaiserKrab, None, ItemClassification.progression),
    ItemData(518_9_309, i.Tortolyde, None, ItemClassification.progression),
    ItemData(518_9_310, i.Doppler, None, ItemClassification.progression),
    ItemData(518_9_311, i.ShellBeast, None, ItemClassification.progression),
    ItemData(518_9_312, i.DarkKnight, None, ItemClassification.progression),
    ItemData(518_9_313, i.DarkSol, None, ItemClassification.progression),
]


required_items = key_items + flag_items

unique_useful_items = [
    ItemData(517_9_113, i.VialOfTears, 0x71, ItemClassification.progression | ItemClassification.useful),
    ItemData(517_9_114, i.Medallion, 0x72, ItemClassification.progression | ItemClassification.useful),
]

equipment_items = [
    ItemData(517_9_000, i.BronzeKnife, 0x00, ItemClassification.useful),
    ItemData(517_9_001, i.ShortSword, 0x01, ItemClassification.useful),
    ItemData(517_9_002, i.Sword, 0x02, ItemClassification.useful),
    ItemData(517_9_003, i.Longsword, 0x03, ItemClassification.useful),
    ItemData(517_9_004, i.Broadsword, 0x04, ItemClassification.useful),
    ItemData(517_9_005, i.FireSword, 0x05, ItemClassification.useful),
    ItemData(517_9_006, i.StormSword, 0x06, ItemClassification.useful),
    ItemData(517_9_007, i.LightBlade, 0x07, ItemClassification.useful),
    ItemData(517_9_008, i.DarkBlade, 0x08, ItemClassification.useful),
    ItemData(517_9_009, i.DreamBlade, 0x09, ItemClassification.useful),
    ItemData(517_9_010, i.BronzeSaber, 0x0A, ItemClassification.useful),
    ItemData(517_9_011, i.SteelSaber, 0x0B, ItemClassification.useful),
    ItemData(517_9_012, i.BattleHammer, 0x0C, ItemClassification.useful),
    ItemData(517_9_013, i.MithrilAxe, 0x0D, ItemClassification.useful),
    ItemData(517_9_014, i.IceSaber, 0x0E, ItemClassification.useful),
    ItemData(517_9_015, i.DarkScimitar, 0x0F, ItemClassification.useful),
    ItemData(517_9_016, i.ShortAxe, 0x10, ItemClassification.useful),
    ItemData(517_9_017, i.BattleAxe, 0x11, ItemClassification.useful),
    ItemData(517_9_018, i.DoubleAxe, 0x12, ItemClassification.useful),
    ItemData(517_9_019, i.GreatAxe, 0x13, ItemClassification.useful),
    ItemData(517_9_020, i.MithrilSword, 0x14, ItemClassification.useful),
    ItemData(517_9_021, i.WoodStaff, 0x15, ItemClassification.useful),
    ItemData(517_9_022, i.Flail, 0x16, ItemClassification.useful),
    ItemData(517_9_023, i.Morningstar, 0x17, ItemClassification.useful),
    ItemData(517_9_024, i.FireStaff, 0x18, ItemClassification.useful),
    ItemData(517_9_025, i.IceStaff, 0x19, ItemClassification.useful),
    ItemData(517_9_026, i.MercyStaff, 0x1A, ItemClassification.useful),
    ItemData(517_9_027, i.Endurostaff, 0x1B, ItemClassification.useful),
    ItemData(517_9_028, i.DoomStaff, 0x1C, ItemClassification.useful),
    ItemData(517_9_029, i.MithrilRod, 0x1D, ItemClassification.useful),
    ItemData(517_9_030, i.WoodenClub, 0x1E, ItemClassification.useful),
    ItemData(517_9_031, i.WarHammer, 0x1F, ItemClassification.useful),
    ItemData(517_9_032, i.BronzeLance, 0x20, ItemClassification.useful),
    ItemData(517_9_033, i.IronLance, 0x21, ItemClassification.useful),
    ItemData(517_9_034, i.SteelLance, 0x22, ItemClassification.useful),
    ItemData(517_9_035, i.ShortSpear, 0x23, ItemClassification.useful),
    ItemData(517_9_036, i.LongSpear, 0x24, ItemClassification.useful),
    ItemData(517_9_037, i.Bullwhip, 0x25, ItemClassification.useful),
    ItemData(517_9_038, i.ThornWhip, 0x26, ItemClassification.useful),
    ItemData(517_9_039, i.SteelWhip, 0x27, ItemClassification.useful),
    ItemData(517_9_040, i.HexWhip, 0x28, ItemClassification.useful),
    ItemData(517_9_041, i.GreatFlail, 0x29, ItemClassification.useful),
    ItemData(517_9_042, i.SuperFlail, 0x2A, ItemClassification.useful),
    ItemData(517_9_043, i.DoomBlade, 0x2B, ItemClassification.useful),
    ItemData(517_9_044, i.WoodShield, 0x2C, ItemClassification.useful),
    ItemData(517_9_045, i.DarkArmor, 0x2D, ItemClassification.useful),
    ItemData(517_9_046, i.FrostArmor, 0x2E, ItemClassification.useful),
    ItemData(517_9_047, i.ThunderArmor, 0x2F, ItemClassification.useful),
    ItemData(517_9_048, i.SunArmor, 0x30, ItemClassification.useful),
    ItemData(517_9_049, i.CottonRobe, 0x31, ItemClassification.useful),
    ItemData(517_9_050, i.WovenRobe, 0x32, ItemClassification.useful),
    ItemData(517_9_051, i.FurRobe, 0x33, ItemClassification.useful),
    ItemData(517_9_052, i.WornRobe, 0x34, ItemClassification.useful),
    ItemData(517_9_053, i.StrawRobe, 0x35, ItemClassification.useful),
    ItemData(517_9_054, i.HempRobe, 0x36, ItemClassification.useful),
    ItemData(517_9_055, i.LeatherRobe, 0x37, ItemClassification.useful),
    ItemData(517_9_056, i.LightRobe, 0x38, ItemClassification.useful),
    ItemData(517_9_057, i.MagicRobe, 0x39, ItemClassification.useful),
    ItemData(517_9_058, i.DarkRobe, 0x3A, ItemClassification.useful),
    ItemData(517_9_059, i.LeatherArmor, 0x3B, ItemClassification.useful),
    ItemData(517_9_060, i.Chainmail, 0x3C, ItemClassification.useful),
    ItemData(517_9_061, i.Breastplate, 0x3D, ItemClassification.useful),
    ItemData(517_9_062, i.BronzeArmor, 0x3E, ItemClassification.useful),
    ItemData(517_9_063, i.IronArmor, 0x3F, ItemClassification.useful),
    ItemData(517_9_064, i.SteelArmor, 0x40, ItemClassification.useful),
    ItemData(517_9_065, i.MithrilArmor, 0x41, ItemClassification.useful),
    ItemData(517_9_066, i.LightArmor, 0x42, ItemClassification.useful),
    ItemData(517_9_067, i.BronzeShield, 0x43, ItemClassification.useful),
    ItemData(517_9_068, i.IronShield, 0x44, ItemClassification.useful),
    ItemData(517_9_069, i.SteelShield, 0x45, ItemClassification.useful),
    ItemData(517_9_070, i.LeatherShield, 0x46, ItemClassification.useful),
    ItemData(517_9_071, i.LightShield, 0x47, ItemClassification.useful),
    ItemData(517_9_072, i.DarkShield, 0x48, ItemClassification.useful),
    ItemData(517_9_073, i.MithrilShield, 0x49, ItemClassification.useful),
    ItemData(517_9_074, i.ElvenHood, 0x4A, ItemClassification.useful),
    ItemData(517_9_075, i.ClothHood, 0x4B, ItemClassification.useful),
    ItemData(517_9_076, i.WovenHood, 0x4C, ItemClassification.useful),
    ItemData(517_9_077, i.FurHood, 0x4D, ItemClassification.useful),
    ItemData(517_9_078, i.MagicHood, 0x4E, ItemClassification.useful),
    ItemData(517_9_079, i.DarkHood, 0x4F, ItemClassification.useful),
    ItemData(517_9_080, i.MithrilHood, 0x50, ItemClassification.useful),
    ItemData(517_9_081, i.LeatherHelm, 0x51, ItemClassification.useful),
    ItemData(517_9_082, i.BronzeHelm, 0x52, ItemClassification.useful),
    ItemData(517_9_083, i.IronHelm, 0x53, ItemClassification.useful),
    ItemData(517_9_084, i.SteelHelm, 0x54, ItemClassification.useful),
    ItemData(517_9_085, i.LightHelm, 0x55, ItemClassification.useful),
    ItemData(517_9_086, i.DarkHelm, 0x56, ItemClassification.useful),
    ItemData(517_9_087, i.MithrilHelm, 0x57, ItemClassification.useful),
    ItemData(517_9_089, i.MagicShield, 0x59, ItemClassification.useful),
    ItemData(517_9_090, i.MagicMail, 0x5A, ItemClassification.useful),
    ItemData(517_9_108, i.ForbiddenBox, 0x6C, ItemClassification.useful),
    ItemData(517_9_118, i.MainGauche, 0x76, ItemClassification.useful),
    ItemData(517_9_119, i.Madu, 0x77, ItemClassification.useful),
    ItemData(517_9_120, i.EarthHammer, 0x78, ItemClassification.useful),
    ItemData(517_9_121, i.ShockBox, 0x79, ItemClassification.useful),
    ItemData(517_9_122, i.OgreFlute, 0x7A, ItemClassification.useful),
    ItemData(517_9_123, i.BlackBox, 0x7B, ItemClassification.useful),
    ItemData(517_9_124, i.Gauntlet, 0x7C, ItemClassification.useful),
    ItemData(517_9_126, i.DemonStaff, 0x7E, ItemClassification.useful),
]

crafting_items = [
    ItemData(517_9_101, i.MithrilOre, 0x65, ItemClassification.useful),
    ItemData(517_9_105, i.DarkBlock, 0x69, ItemClassification.useful),
]

useful_items = unique_useful_items + equipment_items + crafting_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(517_9_091, i.Herb, 0x5B, ItemClassification.filler),
    ItemData(517_9_092, i.Depoison, 0x5C, ItemClassification.filler),
    ItemData(517_9_093, i.AngelFeather, 0x5D, ItemClassification.filler),
    ItemData(517_9_094, i.WisdomSeed, 0x5E, ItemClassification.filler),
    ItemData(517_9_100, i.Tamayoshi, 0x64, ItemClassification.filler),
    ItemData(517_9_102, i.HealRing, 0x66, ItemClassification.filler),
    ItemData(517_9_103, i.BarrierRing, 0x67, ItemClassification.filler),
    ItemData(517_9_104, i.MagicRing, 0x68, ItemClassification.filler),
    ItemData(517_9_106, i.MagicMirror, 0x6A, ItemClassification.filler),
    ItemData(517_9_107, i.HerbWater, 0x6B, ItemClassification.filler),
    ItemData(517_9_109, i.HolyWater, 0x6D, ItemClassification.filler),
    ItemData(517_9_110, i.HealerFruit, 0x6E, ItemClassification.filler),
    ItemData(517_9_111, i.SmellingSalts, 0x6F, ItemClassification.filler),
    ItemData(517_9_117, i.MiracleHerb, 0x75, ItemClassification.filler),
]

junk_items = [
    ItemData(517_9_115, i.Map1, 0x73, ItemClassification.filler | ItemClassification.deprioritized),
    ItemData(517_9_116, i.Map2, 0x74, ItemClassification.filler | ItemClassification.deprioritized),
    ItemData(517_9_125, i.GlassArmor, 0x7D, ItemClassification.filler | ItemClassification.deprioritized),
]

gold_items = [
    ItemData(517_9_400, i.gold(50), 0x80, ItemClassification.filler | ItemClassification.deprioritized, 50),
    ItemData(517_9_401, i.gold(100), 0x81, ItemClassification.filler | ItemClassification.deprioritized, 100),
    ItemData(517_9_402, i.gold(200), 0x82, ItemClassification.filler | ItemClassification.deprioritized, 200),
    ItemData(517_9_403, i.gold(300), 0x83, ItemClassification.filler | ItemClassification.deprioritized, 300),
    ItemData(517_9_404, i.gold(500), 0x83, ItemClassification.filler | ItemClassification.deprioritized, 500),
    ItemData(517_9_405, i.gold(1000), 0x85, ItemClassification.filler | ItemClassification.deprioritized, 1000),
    ItemData(517_9_406, i.gold(2000), 0x86, ItemClassification.filler | ItemClassification.deprioritized, 2000),
]

mimic_items = [
    ItemData(517_9_500, i.ChestBeak, 0x87, ItemClassification.trap),
    ItemData(517_9_501, i.Ghost, 0x88, ItemClassification.trap),
    ItemData(517_9_502, i.HandEater, 0x89, ItemClassification.trap),
]

mimic_item_names = [item.name for item in mimic_items]

filler_items = consumable_items + junk_items + gold_items
filler_item_names = [item.name for item in filler_items]

reward_item_names = [
    i.DwarfKey,
    i.Medallion,
    i.MagicRing,
    i.VialOfTears,
]

item_name_groups = {
    "Key Items": {item.name for item in key_items},
    "Unique and Useful": {item.name for item in unique_useful_items},
    "Equipment": {item.name for item in equipment_items},
    "Crafting": {item.name for item in crafting_items},
    "Consumables": {item.name for item in consumable_items},
    "Junk": {item.name for item in junk_items},
    "Quest Flags": {item.name for item in flag_items},
}

all_items = required_items + useful_items + filler_items + mimic_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}
