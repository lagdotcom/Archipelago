from typing import NamedTuple, Optional

from BaseClasses import ItemClassification as IC

from .Data import Item as I


class ItemData(NamedTuple):
    id: int
    name: str
    code: Optional[int]
    classification: IC
    meseta: int = 0

    def get_chest_bytes(self):
        if self.meseta > 0:
            return (self.meseta & 0x7FFF).to_bytes(2, "big")
        elif self.code is not None:
            return (0x8000 | self.code).to_bytes(2, "big")
        else:
            raise Exception(f"Item {self.name} cannot be placed in chest!")


key_items = [
    ItemData(452_1_001, I.SmallKey, 0x1, IC.progression),
    ItemData(452_1_002, I.Dynamite, 0x2, IC.progression),
    ItemData(452_1_003, I.KeyTube, 0x3, IC.progression),
    ItemData(452_1_004, I.MarueraGum, 0x4, IC.progression),
    ItemData(452_1_005, I.GreenCard, 0x5, IC.progression),
    ItemData(452_1_006, I.BlueCard, 0x6, IC.progression),
    ItemData(452_1_007, I.YellowCard, 0x7, IC.progression),
    ItemData(452_1_008, I.RedCard, 0x8, IC.progression),
    ItemData(452_1_009, I.Letter, 0x9, IC.progression),
    ItemData(452_1_010, I.Recorder, 0xA, IC.progression),
    ItemData(452_1_011, I.MarueraLeaf, 0xB, IC.progression),
    ItemData(452_1_013, I.Prism, 0xD, IC.progression),
    ItemData(452_1_039, I.NeiMet, 0x27, IC.progression),
    ItemData(452_1_040, I.NeiCrown, 0x28, IC.progression),
    ItemData(452_1_061, I.NeiArmor, 0x3D, IC.progression),
    ItemData(452_1_062, I.NeiCape, 0x3E, IC.progression),
    ItemData(452_1_084, I.NeiShield, 0x54, IC.progression),
    ItemData(452_1_085, I.NeiEmel, 0x55, IC.progression),
    # this isn't actually needed, but good luck beating Dark Force without it
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
    ItemData(452_1_042, I.MogicCap, 0x2A, IC.useful),
    ItemData(452_1_125, I.Visiphone, 0x7D, IC.useful),
]

equipment_items = [
    ItemData(452_1_023, I.Headgear, 0x17, IC.useful),
    ItemData(452_1_024, I.Ribbon, 0x18, IC.useful),
    ItemData(452_1_025, I.Fibergear, 0x19, IC.useful),
    ItemData(452_1_026, I.SilRibbon, 0x1A, IC.useful),
    ItemData(452_1_027, I.SilCrown, 0x1B, IC.useful),
    ItemData(452_1_028, I.Titanigear, 0x1C, IC.useful),
    ItemData(452_1_029, I.Titanimet, 0x1D, IC.useful),
    ItemData(452_1_030, I.JwlCrown, 0x1E, IC.useful),
    ItemData(452_1_031, I.JwlRibbon, 0x1F, IC.useful),
    ItemData(452_1_032, I.CresceGear, 0x20, IC.useful),
    ItemData(452_1_033, I.SnowCrown, 0x21, IC.useful),
    ItemData(452_1_034, I.WindScarf, 0x22, IC.useful),
    ItemData(452_1_035, I.ColorScarf, 0x23, IC.useful),
    ItemData(452_1_036, I.StormGear, 0x24, IC.useful),
    ItemData(452_1_037, I.Laconigear, 0x25, IC.useful),
    ItemData(452_1_038, I.LaconiaMet, 0x26, IC.useful),
    ItemData(452_1_043, I.CarbonSuit, 0x2B, IC.useful),
    ItemData(452_1_044, I.CarbonVest, 0x2C, IC.useful),
    ItemData(452_1_045, I.FiberCoat, 0x2D, IC.useful),
    ItemData(452_1_046, I.FiberCape, 0x2E, IC.useful),
    ItemData(452_1_047, I.FiberVest, 0x2F, IC.useful),
    ItemData(452_1_048, I.TtnmArmor, 0x30, IC.useful),
    ItemData(452_1_049, I.TtnmCape, 0x31, IC.useful),
    ItemData(452_1_050, I.TtnmChest, 0x32, IC.useful),
    ItemData(452_1_051, I.CrmcArmor, 0x33, IC.useful),
    ItemData(452_1_052, I.CrmcCape, 0x34, IC.useful),
    ItemData(452_1_053, I.CrmcChest, 0x35, IC.useful),
    ItemData(452_1_054, I.AmberRobe, 0x36, IC.useful),
    ItemData(452_1_055, I.Crystanish, 0x37, IC.useful),
    ItemData(452_1_056, I.CrystCape, 0x38, IC.useful),
    ItemData(452_1_057, I.CrystChest, 0x39, IC.useful),
    ItemData(452_1_058, I.Laconinish, 0x3A, IC.useful),
    ItemData(452_1_059, I.LaconCape, 0x3B, IC.useful),
    ItemData(452_1_060, I.LaconChest, 0x3C, IC.useful),
    ItemData(452_1_063, I.Shoes, 0x3F, IC.useful),
    ItemData(452_1_064, I.Sandals, 0x40, IC.useful),
    ItemData(452_1_065, I.Boots, 0x41, IC.useful),
    ItemData(452_1_066, I.KnifeBoots, 0x42, IC.useful),
    ItemData(452_1_067, I.LongBoots, 0x43, IC.useful),
    ItemData(452_1_068, I.HirzaBoots, 0x44, IC.useful),
    ItemData(452_1_069, I.ShuneBoots, 0x45, IC.useful),
    ItemData(452_1_070, I.GardaBoots, 0x46, IC.useful),
    ItemData(452_1_071, I.CrbnShield, 0x47, IC.useful),
    ItemData(452_1_072, I.CrbnEmel, 0x48, IC.useful),
    ItemData(452_1_073, I.FibrShield, 0x49, IC.useful),
    ItemData(452_1_074, I.FiberEmel, 0x4A, IC.useful),
    ItemData(452_1_075, I.MirShield, 0x4B, IC.useful),
    ItemData(452_1_076, I.MirEmel, 0x4C, IC.useful),
    ItemData(452_1_077, I.CerShield, 0x4D, IC.useful),
    ItemData(452_1_078, I.CerEmel, 0x4E, IC.useful),
    ItemData(452_1_079, I.Aegis, 0x4F, IC.useful),
    ItemData(452_1_080, I.GrSleeves, 0x50, IC.useful),
    ItemData(452_1_081, I.TruthSlvs, 0x51, IC.useful),
    ItemData(452_1_082, I.LaconEmel, 0x52, IC.useful),
    ItemData(452_1_083, I.LacShield, 0x53, IC.useful),
    ItemData(452_1_086, I.Knife, 0x56, IC.useful),
    ItemData(452_1_087, I.Dagger, 0x57, IC.useful),
    ItemData(452_1_088, I.Scalpel, 0x58, IC.useful),
    ItemData(452_1_089, I.SteelBar, 0x59, IC.useful),
    ItemData(452_1_090, I.Boomerang, 0x5A, IC.useful),
    ItemData(452_1_091, I.Slasher, 0x5B, IC.useful),
    ItemData(452_1_092, I.Sword, 0x5C, IC.useful),
    ItemData(452_1_093, I.Whip, 0x5D, IC.useful),
    ItemData(452_1_094, I.CrmcSword, 0x5E, IC.useful),
    ItemData(452_1_095, I.CeramKnife, 0x5F, IC.useful),
    ItemData(452_1_096, I.CeramBar, 0x60, IC.useful),
    ItemData(452_1_097, I.LasrSlshr, 0x61, IC.useful),
    ItemData(452_1_098, I.LasrSword, 0x62, IC.useful),
    ItemData(452_1_099, I.LaserBar, 0x63, IC.useful),
    ItemData(452_1_100, I.LaserKnife, 0x64, IC.useful),
    ItemData(452_1_101, I.SwdOfAng, 0x65, IC.useful),
    ItemData(452_1_102, I.FireSlshr, 0x66, IC.useful),
    ItemData(452_1_103, I.FireStaff, 0x67, IC.useful),
    ItemData(452_1_104, I.LacnMace, 0x68, IC.useful),
    ItemData(452_1_105, I.LacDagger, 0x69, IC.useful),
    ItemData(452_1_106, I.ACSlashr, 0x6A, IC.useful),
    ItemData(452_1_107, I.LacSword, 0x6B, IC.useful),
    ItemData(452_1_110, I.Bowgun, 0x6E, IC.useful),
    ItemData(452_1_111, I.SonicGun, 0x6F, IC.useful),
    ItemData(452_1_112, I.Shotgun, 0x70, IC.useful),
    ItemData(452_1_113, I.SilentShot, 0x71, IC.useful),
    ItemData(452_1_114, I.PoisonShot, 0x72, IC.useful),
    ItemData(452_1_115, I.AcidShot, 0x73, IC.useful),
    ItemData(452_1_116, I.Cannon, 0x74, IC.useful),
    ItemData(452_1_117, I.Vulcan, 0x75, IC.useful),
    ItemData(452_1_118, I.LaserShot, 0x76, IC.useful),
    ItemData(452_1_119, I.LsrCannon, 0x77, IC.useful),
    ItemData(452_1_120, I.PlsCannon, 0x78, IC.useful),
    ItemData(452_1_121, I.PulseVlcn, 0x79, IC.useful),
]

useful_items = unique_useful_items + equipment_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(452_1_014, I.Telepipe, 0xE, IC.filler),
    ItemData(452_1_015, I.Escapipe, 0xF, IC.filler),
    ItemData(452_1_016, I.Hidapipe, 0x10, IC.filler),
    ItemData(452_1_017, I.Monomate, 0x11, IC.filler),
    ItemData(452_1_018, I.Dimate, 0x12, IC.filler),
    ItemData(452_1_019, I.Trimate, 0x13, IC.filler),
    ItemData(452_1_020, I.Antidote, 0x14, IC.filler),
    ItemData(452_1_021, I.StarMist, 0x15, IC.filler),
    ItemData(452_1_022, I.MoonDew, 0x16, IC.filler),
]

junk_items = [
    ItemData(452_1_012, I.PlsmRing, 0xC, IC.filler),
    ItemData(452_1_041, I.MagicCap, 0x29, IC.filler),
    ItemData(452_1_123, I.PrsnClths, 0x7B, IC.filler),
    # ItemData(452_1_126, 'Unknown1', 0x7E, IC.filler),
    # ItemData(452_1_127, 'Unknown2', 0x7F, IC.filler),
    ItemData(452_2_000, I.Garbage, 0, IC.filler),
]

meseta_items = [
    ItemData(452_2_001, I.Meseta(20), None, IC.filler, 20),
    ItemData(452_2_002, I.Meseta(40), None, IC.filler, 40),
    ItemData(452_2_003, I.Meseta(60), None, IC.filler, 60),
    ItemData(452_2_004, I.Meseta(100), None, IC.filler, 100),
    ItemData(452_2_005, I.Meseta(150), None, IC.filler, 150),
    ItemData(452_2_006, I.Meseta(200), None, IC.filler, 200),
    ItemData(452_2_007, I.Meseta(5600), None, IC.filler, 5600),
    ItemData(452_2_008, I.Meseta(6400), None, IC.filler, 6400),
    ItemData(452_2_009, I.Meseta(7800), None, IC.filler, 7800),
    ItemData(452_2_010, I.Meseta(8600), None, IC.filler, 8600),
    ItemData(452_2_011, I.Meseta(12000), None, IC.filler, 12000),
    ItemData(452_2_012, I.Meseta(15000), None, IC.filler, 15000),
    ItemData(452_2_013, I.Meseta(18000), None, IC.filler, 18000),
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
