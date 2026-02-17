from typing import NamedTuple

from rule_builder.rules import Has, Rule

from .constants import CHEST_CONTENTS_BY_FLOOR, chest_flags_span
from .laglib import IntSpan
from .laglib import genesis_rom as rom
from .Names import item_name as i
from .Names import region_name as r

mask_to_offset = {0x01: 0, 0x02: 1, 0x04: 2, 0x08: 3, 0x10: 4, 0x20: 5, 0x40: 6, 0x80: 7}


class LD(NamedTuple):
    id: int
    region_name: str
    item_name: str
    vanilla_item: str
    check_address: int
    check_mask: int
    fixed_item: str | None = None
    rule: Rule | None = None

    @property
    def name(self):
        return f"{self.region_name} - {self.item_name}"

    @property
    def is_chest(self):
        return self.check_address >= chest_flags_span.address and self.check_address < chest_flags_span.end_address

    @property
    def rom_locations(self):
        if self.is_chest:
            floor_no = (self.check_address - chest_flags_span.address) // 2
            addr = CHEST_CONTENTS_BY_FLOOR[floor_no] + mask_to_offset[self.check_mask]
            if not self.check_address & 1:
                addr += 8
            return [IntSpan(rom, addr, 1)]
        if self.check_address == 0x1616 and self.check_mask == 0x01:
            return [IntSpan(rom, 0x5A141, 1)]
        if self.check_address == 0x1618 and self.check_mask == 0x02:
            return [IntSpan(rom, 0x22A9F, 1), IntSpan(rom, 0x22AB3, 1)]
        if self.check_address == 0x161A and self.check_mask == 0x02:
            return [IntSpan(rom, 0x22226, 2), IntSpan(rom, 0x22234, 2)]
        raise Exception(f"Cannot get ROM locations for {self.check_address:04x}/{self.check_mask:02x}")


lab1_locations = [
    LD(517_00_00, r.Lab1, "Herb Chest 1", i.Herb, 0x1620, 0x08),
    LD(517_00_01, r.Lab1, "50g Chest", i.gold(50), 0x1620, 0x04),
    LD(517_00_02, r.Lab1, "Bronze Knife Chest", i.BronzeKnife, 0x1620, 0x01),
    LD(517_00_03, r.Lab1, "Herb Chest 2", i.Herb, 0x1620, 0x02),
    LD(517_00_04, r.Lab1, "Herb Chest 3", i.Herb, 0x1621, 0x01),
    LD(517_00_05, r.Lab1, "100g Chest", i.gold(100), 0x1621, 0x04),
    # TODO figure out enemy drops...
    LD(517_00_06, r.Lab1, "Defeat Kaiser Krab", i.RoyalTiara, 0x163F, 0x02, fixed_item=i.RoyalTiara),
    LD(517_00_07, r.Lab1, "Receive Dwarf's Key from Minister", i.DwarfKey, 0x1616, 0x01, rule=Has(i.RoyalTiara)),
    LD(517_01_00, r.Lab1Str, "Depoison Chest", i.Depoison, 0x1621, 0x20),
    LD(517_01_01, r.Lab1Str, "Herb Chest", i.Herb, 0x1621, 0x40),
    LD(517_01_02, r.Lab1Str, "Wisdom Seed Chest", i.WisdomSeed, 0x1621, 0x80),
    LD(517_03_00, r.Lab1Cou, "Smelling Salts Chest", i.SmellingSalts, 0x1621, 0x02),
    LD(517_03_01, r.Lab1Cou, "Morning Star Chest", i.Morningstar, 0x1621, 0x08),
    LD(517_05_00, r.Lab1Tru, "100g Chest", i.gold(100), 0x1621, 0x10),
]

str_locations = [
    LD(517_02_00, r.Str, "Defeat Chest Beak 1", i.ChestBeak, 0x1633, 0x01),
    LD(517_02_01, r.Str, "Wisdom Seed Chest 1", i.WisdomSeed, 0x1633, 0x02),
    LD(517_02_02, r.Str, "Defeat Chest Beak 2", i.ChestBeak, 0x1633, 0x20),
    LD(517_02_03, r.Str, "Wisdom Seed Chest 2", i.WisdomSeed, 0x1633, 0x40),
    LD(517_02_04, r.Str, "Depoison Chest", i.Depoison, 0x1633, 0x80),
    LD(517_02_05, r.Str, "100g Chest", i.gold(100), 0x1632, 0x08),
    LD(517_02_06, r.Str, "Smelling Salts Chest", i.SmellingSalts, 0x1632, 0x10),
    LD(517_02_07, r.Str, "Herb Chest", i.Herb, 0x1632, 0x01),
    LD(517_02_08, r.Str, "Defeat Chest Beak 3", i.ChestBeak, 0x1632, 0x04),
    LD(517_02_09, r.Str, "Woven Robe Chest", i.WovenRobe, 0x1632, 0x20),
    LD(517_02_10, r.Str, "Meet Gila", i.Gila, 0x163D, 0x01, fixed_item=i.Gila),
    LD(517_02_11, r.Str, "Short Sword Chest", i.ShortSword, 0x1633, 0x10),
    LD(517_02_12, r.Str, "Wisdom Seed Chest 3", i.WisdomSeed, 0x1633, 0x04),
    LD(517_02_13, r.Str, "Door of Strength", i.TrialOfStrength, 0x1608, 0x01, fixed_item=i.TrialOfStrength),
    LD(517_02_14, r.Str, "Healer Fruit Chest", i.HealerFruit, 0x1635, 0x01),
    LD(517_11_00, r.StrRope, "Mithril Ore Chest", i.MithrilOre, 0x1632, 0x02),
    LD(517_16_00, r.StrCell, "Forbidden Box Chest", i.ForbiddenBox, 0x1633, 0x08),
]

cou_locations = [
    LD(517_04_00, r.Cou, "Wisdom Seed Chest 1", i.WisdomSeed, 0x1637, 0x01),
    LD(517_04_01, r.Cou, "50g Chest", i.gold(50), 0x1637, 0x02),
    LD(517_04_02, r.Cou, "Angel Feather Chest", i.AngelFeather, 0x1637, 0x10),
    LD(517_04_03, r.Cou, "Woven Robe Chest", i.WovenRobe, 0x1637, 0x20),
    LD(517_04_04, r.Cou, "Defeat Chest Beak", i.ChestBeak, 0x1637, 0x40),
    LD(517_04_05, r.Cou, "Morning Star Chest", i.Morningstar, 0x1637, 0x80),
    LD(517_04_06, r.Cou, "100g Chest", i.gold(100), 0x1637, 0x04),
    LD(517_04_07, r.Cou, "Depoison Chest", i.Depoison, 0x1636, 0x01),
    LD(517_04_08, r.Cou, "Smelling Salts Chest", i.SmellingSalts, 0x1637, 0x08),
    LD(517_04_09, r.Cou, "Bronze Shield Chest", i.BronzeShield, 0x1636, 0x04),
    LD(517_04_10, r.Cou, "Healer Fruit Chest", i.HealerFruit, 0x1636, 0x40),
    LD(517_04_11, r.Cou, "Wisdom Seed Chest 2", i.WisdomSeed, 0x1636, 0x08),
    LD(517_04_12, r.Cou, "Woven Hood Chest", i.WovenHood, 0x1636, 0x20),
    LD(517_04_13, r.Cou, "Door of Courage", i.TrialOfCourage, 0x1608, 0x02, fixed_item=i.TrialOfCourage),
    # TODO figure out enemy drops...
    LD(517_04_14, r.Cou, "Defeat Tortolyde", i.OrbOfTruth, 0x163F, 0x04, fixed_item=i.OrbOfTruth),
    LD(517_17_00, r.CouCell, "Demon Staff Chest", i.DemonStaff, 0x1636, 0x02),
]

tru_locations = [
    LD(517_06_00, r.Tru, "Wisdom Seed Chest", i.WisdomSeed, 0x1630, 0x10),
    LD(517_06_01, r.Tru, "50g Chest", i.gold(50), 0x1630, 0x04),
    LD(517_06_02, r.Tru, "Wood Staff Chest", i.WoodStaff, 0x1631, 0x80),
    LD(517_06_03, r.Tru, "Healer Fruit Chest", i.HealerFruit, 0x1631, 0x10),
    LD(517_06_04, r.Tru, "Depoison Chest", i.Depoison, 0x1630, 0x01),
    LD(517_06_05, r.Tru, "Defeat Ghost 1", i.Ghost, 0x1630, 0x40),
    LD(517_06_06, r.Tru, "Angel Feather Chest", i.AngelFeather, 0x1630, 0x20),
    LD(517_06_07, r.Tru, "False Idol Chest", i.FalseIdol, 0x1630, 0x02),
    LD(517_06_08, r.Tru, "Defeat Ghost 2", i.Ghost, 0x1631, 0x20),
    LD(517_06_09, r.Tru, "Smelling Salts Chest", i.SmellingSalts, 0x1630, 0x08),
    LD(517_06_10, r.Tru, "Chain Mail Chest", i.Chainmail, 0x1631, 0x01),
    LD(517_06_11, r.Tru, "Battle Axe Chest", i.BattleAxe, 0x1631, 0x04),
    LD(517_06_12, r.Tru, "Door of Truth", i.TrialOfTruth, 0x1608, 0x04, fixed_item=i.TrialOfTruth),
    LD(517_07_00, r.TruIdol, "Defeat Doppler", i.Doppler, 0x163D, 0x10, fixed_item=i.Doppler),
    LD(517_07_01, r.TruIdol, "Rune Key Chest", i.RuneKey, 0x1631, 0x08),
    LD(517_18_00, r.TruCell, "Magic Ring Chest", i.MagicRing, 0x1631, 0x40),
]

wis_locations = [
    LD(517_08_00, r.Wis, "Map 1 Chest", i.Map1, 0x162B, 0x40),
    LD(517_08_01, r.Wis, "Battle Axe Chest", i.BattleAxe, 0x162B, 0x80),
    LD(517_08_02, r.Wis, "Map 2 Chest", i.Map2, 0x162B, 0x04),
    LD(517_08_03, r.Wis, "Meet Dai", i.Dai, 0x163D, 0x40, fixed_item=i.Dai),
    LD(517_08_04, r.Wis, "Smelling Salts Chest", i.SmellingSalts, 0x162A, 0x04),
    LD(517_08_05, r.Wis, "Flail Chest", i.Flail, 0x162B, 0x20),
    LD(517_08_06, r.Wis, "Defeat Ghost", i.Ghost, 0x162B, 0x01),
    LD(517_08_07, r.Wis, "Dark Block Chest", i.DarkBlock, 0x162B, 0x08),
    LD(517_08_08, r.Wis, "Herb-Water Chest", i.HerbWater, 0x162A, 0x01),
    LD(517_08_09, r.Wis, "Mithril Ore Chest", i.MithrilOre, 0x162B, 0x02),
    LD(517_08_10, r.Wis, "Door of Wisdom", i.TrialOfWisdom, 0x1608, 0x08, fixed_item=i.TrialOfWisdom),
    LD(517_08_11, r.Wis, "Fire Sword Chest", i.FireSword, 0x162D, 0x02),
    LD(517_08_12, r.Wis, "200g Chest", i.gold(200), 0x162D, 0x01),
    LD(517_19_00, r.WisCell, "Defeat Ghost", i.Ghost, 0x162A, 0x02),
]

lab2_locations = [
    LD(517_09_00, r.Lab2, "Mithril Ore Chest", i.MithrilOre, 0x1623, 0x10),
    LD(517_09_01, r.Lab2, "500g Chest", i.gold(500), 0x1622, 0x01),
    LD(517_09_02, r.Lab2, "Depoison Chest", i.Depoison, 0x1622, 0x04),
    LD(517_09_03, r.Lab2, "Great Axe Chest", i.GreatAxe, 0x1622, 0x02),
    LD(517_09_04, r.Lab2, "Angel Feather Chest", i.AngelFeather, 0x1623, 0x02),
    LD(517_09_05, r.Lab2, "Magic Hood Chest", i.MagicHood, 0x1623, 0x01),
    LD(517_09_06, r.Lab2, "Fire Staff Chest", i.FireStaff, 0x1623, 0x08),
    LD(517_09_07, r.Lab2, "Smelling Salts Chest", i.SmellingSalts, 0x1623, 0x20),
    LD(517_09_08, r.Lab2, "Healer Fruit Chest", i.HealerFruit, 0x1623, 0x04),
    LD(517_09_09, r.Lab2, "Sun Armor Chest", i.SunArmor, 0x1622, 0x08),
    LD(517_09_10, r.Lab2, "Worn Robe Chest", i.WornRobe, 0x1623, 0x80),
    LD(517_09_11, r.Lab2, "300g Chest", i.gold(300), 0x1623, 0x40),
    LD(517_20_00, r.Lab2Cell, "Barrier Ring Chest", i.BarrierRing, 0x1622, 0x10),
]

lab3_locations = [
    LD(517_10_00, r.Lab3, "Entered Labyrinth L3", i.EnterLab3, 0x1605, 0x30, fixed_item=i.EnterLab3),
    LD(517_10_01, r.Lab3, "Defeat Shell Beast", i.ShellBeast, 0x1640, 0x10, fixed_item=i.ShellBeast),
    LD(
        517_10_02, r.Lab3, "Receive Medallion from Xern", i.Medallion, 0x1618, 0x02, fixed_item=i.Medallion
    ),  # TODO what is the requirement for this?
    LD(517_10_03, r.Lab3, "500g Chest", i.gold(500), 0x1625, 0x20),
    LD(517_10_04, r.Lab3, "Mystic Rope Chest", i.MysticRope, 0x1624, 0x01),
    LD(517_10_05, r.Lab3, "Healer Fruit Chest", i.HealerFruit, 0x1624, 0x02),
    LD(517_10_06, r.Lab3, "Herb-Water Chest", i.HerbWater, 0x1625, 0x10),
    LD(517_10_07, r.Lab3, "Ice Staff Chest", i.IceStaff, 0x1625, 0x40),
    LD(517_10_08, r.Lab3, "Light Helm Chest", i.LightHelm, 0x1625, 0x02),
    LD(517_12_00, r.Lab3Rope, "Storm Sword Chest", i.StormSword, 0x1625, 0x08),
    LD(517_12_01, r.Lab3Rope, "Great Flail Chest", i.GreatFlail, 0x1625, 0x08),
    LD(517_13_00, r.Lab3RopeOrCell, "Mithril Ore Chest", i.MithrilOre, 0x1625, 0x80),
    LD(517_21_00, r.Lab3Cell, "Light Shield Chest", i.LightShield, 0x1625, 0x01),
]

lab4_locations = [
    LD(517_14_00, r.Lab4, "Endurostaff Chest", i.Endurostaff, 0x1626, 0x08),
    LD(517_14_01, r.Lab4, "Elven Hood Chest", i.ElvenHood, 0x1627, 0x02),
    LD(517_14_02, r.Lab4, "Holy Water Chest", i.HolyWater, 0x1626, 0x04),
    LD(517_14_03, r.Lab4, "Healer Fruit Chest", i.HealerFruit, 0x1626, 0x10),
    LD(517_14_04, r.Lab4, "Herb-Water Chest", i.HerbWater, 0x1626, 0x02),
    LD(517_14_05, r.Lab4, "Steel Whip Chest", i.SteelWhip, 0x1627, 0x40),
    LD(517_14_06, r.Lab4, "Heal Ring Chest", i.HealRing, 0x1627, 0x08),
    LD(517_14_07, r.Lab4, "Defeat Hand Eater 1", i.HandEater, 0x1627, 0x20),
    LD(517_14_08, r.Lab4, "Defeat Hand Eater 2", i.HandEater, 0x1627, 0x80),
    LD(517_14_09, r.Lab4, "Frost Armor Chest", i.FrostArmor, 0x1626, 0x01),
    LD(517_14_10, r.Lab4, "Defeat Dark Knight", i.DarkKnight, 0x163D, 0x04, fixed_item=i.DarkKnight),
    LD(517_14_11, r.Lab4, "Cell Key Chest", i.CellKey, 0x1627, 0x10),
    LD(517_14_12, r.Lab4, "Miracle Herb Chest", i.MiracleHerb, 0x1627, 0x04),
    LD(517_15_00, r.Lab4Orb, "Light Blade Chest", i.LightBlade, 0x1627, 0x01),
    LD(517_22_00, r.Lab4Cell, "Meet Jessa", i.Jessa, 0x163F, 0x01, i.Jessa),
    LD(517_22_01, r.Lab4Cell, "Receive Magic Ring from King", i.MagicRing, 0x161A, 0x02, rule=Has(i.Jessa)),
]

lab5_locations = [
    LD(517_23_00, r.Lab5, "Mithril Ore Chest", i.MithrilOre, 0x1629, 0x01),
    LD(517_23_01, r.Lab5, "1000g Chest", i.gold(1000), 0x1628, 0x08),
    LD(517_23_02, r.Lab5, "Magic Robe Chest", i.MagicRobe, 0x1628, 0x02),
    LD(517_23_03, r.Lab5, "Defeat Hand Eater 1", i.HandEater, 0x1628, 0x04),
    LD(517_23_04, r.Lab5, "Magic Ring Chest", i.MagicRing, 0x1628, 0x10),
    LD(517_23_05, r.Lab5, "Defeat Hand Eater 2", i.HandEater, 0x1629, 0x08),
    LD(517_23_06, r.Lab5, "Defeat Hand Eater 3", i.HandEater, 0x1629, 0x40),
    LD(517_23_07, r.Lab5, "Dark Scimitar Chest", i.DarkScimitar, 0x1629, 0x80),
    LD(517_23_08, r.Lab5, "Dark Block Chest", i.DarkBlock, 0x1628, 0x01),
    LD(517_23_09, r.Lab5, "2000g Chest", i.gold(2000), 0x1629, 0x10),
    LD(517_23_10, r.Lab5, "200g Chest", i.gold(200), 0x1629, 0x04),
    LD(517_23_11, r.Lab5, "Light Armor Chest", i.LightArmor, 0x1629, 0x02),
    LD(517_23_12, r.Lab5, "Miracle Herb Chest", i.MiracleHerb, 0x1629, 0x20),
    LD(517_23_13, r.Lab5, "Defeat Dark Sol", i.DarkSol, 0x1607, 0x80, fixed_item=i.DarkSol),
]

all_locations = (
    lab1_locations
    + str_locations
    + cou_locations
    + tru_locations
    + wis_locations
    + lab2_locations
    + lab3_locations
    + lab4_locations
    + lab5_locations
)
chest_locations = [location for location in all_locations if location.is_chest]

locations_by_id = {location.id: location for location in all_locations}
locations_by_name = {location.name: location for location in all_locations}

location_name_groups = {
    "Labyrinth L1": {loc.name for loc in lab1_locations},
    "Labyrinth L2": {loc.name for loc in lab2_locations},
    "Labyrinth L3": {loc.name for loc in lab3_locations},
    "Labyrinth L4": {loc.name for loc in lab4_locations},
    "Labyrinth L5": {loc.name for loc in lab5_locations},
    "Cave of Strength": {loc.name for loc in str_locations},
    "Cave of Courage": {loc.name for loc in cou_locations},
    "Cave of Truth": {loc.name for loc in tru_locations},
    "Cave of Wisdom": {loc.name for loc in wis_locations},
}
