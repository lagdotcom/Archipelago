from typing import NamedTuple

from .constants import CHEST_CONTENTS_BY_FLOOR, CHEST_FLAG_END, CHEST_FLAG_START
from .Names import item_name as i
from .Names import region_name as r

mask_to_offset = {0x01: 0, 0x02: 1, 0x04: 2, 0x08: 3, 0x10: 4, 0x20: 5, 0x40: 6, 0x80: 7}


class Replacement(NamedTuple):
    address: int
    size: int

    def format(self, value: int):
        return value.to_bytes(self.size, "big")


class LD(NamedTuple):
    id: int
    region_name: str
    item_name: str
    check_address: int
    check_mask: int
    fixed_item: str | None = None
    required_items: set[str] | None = None

    @property
    def name(self):
        return f"{self.region_name} - {self.item_name}"

    @property
    def is_chest(self):
        return self.check_address >= CHEST_FLAG_START and self.check_address < CHEST_FLAG_END

    @property
    def rom_locations(self):
        if self.is_chest:
            floor_no = (self.check_address - CHEST_FLAG_START) // 2
            addr = CHEST_CONTENTS_BY_FLOOR[floor_no] + mask_to_offset[self.check_mask]
            if not self.check_address & 1:
                addr += 8
            return [Replacement(addr, 1)]
        if self.check_address == 0x1616 and self.check_mask == 0x01:
            return [Replacement(0x5A141, 1)]
        if self.check_address == 0x1618 and self.check_mask == 0x02:
            return [Replacement(0x22A9F, 1), Replacement(0x22AB3, 1)]
        if self.check_address == 0x161A and self.check_mask == 0x02:
            return [Replacement(0x22226, 2), Replacement(0x22234, 2)]
        raise Exception(f"Cannot get ROM locations for {self.check_address:4x}/{self.check_mask:2x}")


lab1_locations = [
    LD(517_00_00, r.Lab1, "Herb Chest 1", 0x1620, 0x08),
    LD(517_00_01, r.Lab1, "50g Chest", 0x1620, 0x04),
    LD(517_00_02, r.Lab1, "Bronze Knife Chest", 0x1620, 0x01),
    LD(517_00_03, r.Lab1, "Herb Chest 2", 0x1620, 0x02),
    LD(517_00_04, r.Lab1, "Herb Chest 3", 0x1621, 0x01),
    LD(517_00_05, r.Lab1, "100g Chest", 0x1621, 0x04),
    LD(517_00_06, r.Lab1, "Defeat Kaiser Krab", 0x163F, 0x02, i.KaiserKrab),
    LD(517_00_07, r.Lab1, "Receive Dwarf's Key from Minister", 0x1616, 0x01, None, {i.KaiserKrab}),
    LD(517_01_00, r.Lab1Str, "Depoison Chest", 0x1621, 0x20),
    LD(517_01_01, r.Lab1Str, "Herb Chest", 0x1621, 0x40),
    LD(517_01_02, r.Lab1Str, "Wisdom Seed Chest", 0x1621, 0x80),
    LD(517_03_00, r.Lab1Cou, "Smelling Salts Chest", 0x1621, 0x02),
    LD(517_03_01, r.Lab1Cou, "Morning Star Chest", 0x1621, 0x08),
    LD(517_05_00, r.Lab1Tru, "100g Chest", 0x1621, 0x10),
]

str_locations = [
    LD(517_02_00, r.Str, "Defeat Chest Beak 1", 0x1633, 0x01),
    LD(517_02_01, r.Str, "Wisdom Seed Chest 1", 0x1633, 0x02),
    LD(517_02_02, r.Str, "Defeat Chest Beak 2", 0x1633, 0x20),
    LD(517_02_03, r.Str, "Wisdom Seed Chest 2", 0x1633, 0x40),
    LD(517_02_04, r.Str, "Depoison Chest", 0x1633, 0x80),
    LD(517_02_05, r.Str, "100g Chest", 0x1632, 0x08),
    LD(517_02_06, r.Str, "Smelling Salts Chest", 0x1632, 0x10),
    LD(517_02_07, r.Str, "Herb Chest", 0x1632, 0x01),
    LD(517_02_08, r.Str, "Defeat Chest Beak 3", 0x1632, 0x04),
    LD(517_02_09, r.Str, "Woven Robe Chest", 0x1632, 0x20),
    LD(517_02_10, r.Str, "Meet Gila", 0x163D, 0x01, i.Gila),
    LD(517_02_11, r.Str, "Short Sword Chest", 0x1633, 0x10),
    LD(517_02_12, r.Str, "Wisdom Seed Chest 3", 0x1633, 0x04),
    LD(517_02_13, r.Str, "Door of Strength", 0x1608, 0x01, i.TrialOfStrength),
    LD(517_02_14, r.Str, "Healer Fruit Chest", 0x1635, 0x01),
    LD(517_11_00, r.StrRope, "Mithril Ore Chest", 0x1632, 0x02),
    LD(517_16_00, r.StrCell, "Forbidden Box Chest", 0x1633, 0x08),
]

cou_locations = [
    LD(517_04_00, r.Cou, "Wisdom Seed Chest 1", 0x1637, 0x01),
    LD(517_04_01, r.Cou, "50g Chest", 0x1637, 0x02),
    LD(517_04_02, r.Cou, "Angel Feather Chest", 0x1637, 0x10),
    LD(517_04_03, r.Cou, "Woven Robe Chest", 0x1637, 0x20),
    LD(517_04_04, r.Cou, "Defeat Chest Beak", 0x1637, 0x40),
    LD(517_04_05, r.Cou, "Morning Star Chest", 0x1637, 0x80),
    LD(517_04_06, r.Cou, "100g Chest", 0x1637, 0x04),
    LD(517_04_07, r.Cou, "Depoison Chest", 0x1636, 0x01),
    LD(517_04_08, r.Cou, "Smelling Salts Chest", 0x1637, 0x08),
    LD(517_04_09, r.Cou, "Bronze Shield Chest", 0x1636, 0x04),
    LD(517_04_10, r.Cou, "Healer Fruit Chest", 0x1636, 0x40),
    LD(517_04_11, r.Cou, "Wisdom Seed Chest 2", 0x1636, 0x08),
    LD(517_04_12, r.Cou, "Woven Hood Chest", 0x1636, 0x20),
    LD(517_04_13, r.Cou, "Door of Courage", 0x1608, 0x02, i.TrialOfCourage),
    LD(517_04_14, r.Cou, "Defeat Tortolyde", 0x163F, 0x04, i.Tortolyde),
    LD(517_17_00, r.CouCell, "Demon Staff Chest", 0x1636, 0x02),
]

tru_locations = [
    LD(517_06_00, r.Tru, "Wisdom Seed Chest", 0x1630, 0x10),
    LD(517_06_01, r.Tru, "50g Chest", 0x1630, 0x04),
    LD(517_06_02, r.Tru, "Wood Staff Chest", 0x1631, 0x80),
    LD(517_06_03, r.Tru, "Healer Fruit Chest", 0x1631, 0x10),
    LD(517_06_04, r.Tru, "Depoison Chest", 0x1630, 0x01),
    LD(517_06_05, r.Tru, "Defeat Ghost 1", 0x1630, 0x40),
    LD(517_06_06, r.Tru, "Angel Feather Chest", 0x1630, 0x20),
    LD(517_06_07, r.Tru, "False Idol Chest", 0x1630, 0x02),
    LD(517_06_08, r.Tru, "Defeat Ghost 2", 0x1631, 0x20),
    LD(517_06_09, r.Tru, "Smelling Salts Chest", 0x1630, 0x08),
    LD(517_06_10, r.Tru, "Chain Mail Chest", 0x1631, 0x01),
    LD(517_06_11, r.Tru, "Battle Axe Chest", 0x1631, 0x04),
    LD(517_06_12, r.Tru, "Door of Truth", 0x1608, 0x04, i.TrialOfTruth),
    LD(517_07_00, r.TruIdol, "Defeat Doppler", 0x163D, 0x10, i.Doppler),
    LD(517_07_01, r.TruIdol, "Rune Key Chest", 0x1631, 0x08),
    LD(517_18_00, r.TruCell, "Magic Ring Chest", 0x1631, 0x40),
]

wis_locations = [
    LD(517_08_00, r.Wis, "Map 1 Chest", 0x162B, 0x40),
    LD(517_08_01, r.Wis, "Battle Axe Chest", 0x162B, 0x80),
    LD(517_08_02, r.Wis, "Map 2 Chest", 0x162B, 0x04),
    LD(517_08_03, r.Wis, "Meet Dai", 0x163D, 0x40, i.Dai),
    LD(517_08_04, r.Wis, "Smelling Salts Chest", 0x162A, 0x04),
    LD(517_08_05, r.Wis, "Flail Chest", 0x162B, 0x20),
    LD(517_08_06, r.Wis, "Defeat Ghost", 0x162B, 0x01),
    LD(517_08_07, r.Wis, "Dark Block Chest", 0x162B, 0x08),
    LD(517_08_08, r.Wis, "Herb-Water Chest", 0x162A, 0x01),
    LD(517_08_09, r.Wis, "Mithril Ore Chest", 0x162B, 0x02),
    LD(517_08_10, r.Wis, "Door of Wisdom", 0x1608, 0x08, i.TrialOfWisdom),
    LD(517_08_11, r.Wis, "Fire Sword Chest", 0x162D, 0x02),
    LD(517_08_12, r.Wis, "200g Chest", 0x162D, 0x01),
    LD(517_19_00, r.WisCell, "Defeat Ghost", 0x162A, 0x02),
]

lab2_locations = [
    LD(517_09_00, r.Lab2, "Mithril Ore Chest", 0x1623, 0x10),
    LD(517_09_01, r.Lab2, "500g Chest", 0x1622, 0x01),
    LD(517_09_02, r.Lab2, "Depoison Chest", 0x1622, 0x04),
    LD(517_09_03, r.Lab2, "Great Axe Chest", 0x1622, 0x02),
    LD(517_09_04, r.Lab2, "Angel Feather Chest", 0x1623, 0x02),
    LD(517_09_05, r.Lab2, "Magic Hood Chest", 0x1623, 0x01),
    LD(517_09_06, r.Lab2, "Fire Staff Chest", 0x1623, 0x08),
    LD(517_09_07, r.Lab2, "Smelling Salts Chest", 0x1623, 0x20),
    LD(517_09_08, r.Lab2, "Healer Fruit Chest", 0x1623, 0x04),
    LD(517_09_09, r.Lab2, "Sun Armor Chest", 0x1622, 0x08),
    LD(517_09_10, r.Lab2, "Worn Robe Chest", 0x1623, 0x80),
    LD(517_09_11, r.Lab2, "300g Chest", 0x1623, 0x40),
    LD(517_20_00, r.Lab2Cell, "Barrier Ring Chest", 0x1622, 0x10),
]

lab3_locations = [
    LD(517_10_00, r.Lab3, "Entered Labyrinth L3", 0x1605, 0x30, i.EnterLab3),
    LD(517_10_01, r.Lab3, "Defeat Shell Beast", 0x1640, 0x10, i.ShellBeast),
    LD(
        517_10_02, r.Lab3, "Receive Medallion from Xern", 0x1618, 0x02, i.Medallion
    ),  # TODO what is the requirement for this?
    LD(517_10_03, r.Lab3, "500g Chest", 0x1625, 0x20),
    LD(517_10_04, r.Lab3, "Mystic Rope Chest", 0x1624, 0x01),
    LD(517_10_05, r.Lab3, "Healer Fruit Chest", 0x1624, 0x02),
    LD(517_10_06, r.Lab3, "Herb-Water Chest", 0x1625, 0x10),
    LD(517_10_07, r.Lab3, "Ice Staff Chest", 0x1625, 0x40),
    LD(517_10_08, r.Lab3, "Light Helm Chest", 0x1625, 0x02),
    LD(517_12_00, r.Lab3Rope, "Storm Sword Chest", 0x1625, 0x08),
    LD(517_12_01, r.Lab3Rope, "Great Flail Chest", 0x1625, 0x08),
    LD(517_13_00, r.Lab3RopeOrCell, "Mithril Ore Chest", 0x1625, 0x80),
    LD(517_21_00, r.Lab3Cell, "Light Shield Chest", 0x1625, 0x01),
]

lab4_locations = [
    LD(517_14_00, r.Lab4, "Endurostaff Chest", 0x1626, 0x08),
    LD(517_14_01, r.Lab4, "Elven Hood Chest", 0x1627, 0x02),
    LD(517_14_02, r.Lab4, "Holy Water Chest", 0x1626, 0x04),
    LD(517_14_03, r.Lab4, "Healer Fruit Chest", 0x1626, 0x10),
    LD(517_14_04, r.Lab4, "Herb-Water Chest", 0x1626, 0x02),
    LD(517_14_05, r.Lab4, "Steel Whip Chest", 0x1627, 0x40),
    LD(517_14_06, r.Lab4, "Heal Ring Chest", 0x1627, 0x08),
    LD(517_14_07, r.Lab4, "Defeat Hand Eater 1", 0x1627, 0x20),
    LD(517_14_08, r.Lab4, "Defeat Hand Eater 2", 0x1627, 0x80),
    LD(517_14_09, r.Lab4, "Frost Armor Chest", 0x1626, 0x01),
    LD(517_14_10, r.Lab4, "Defeat Dark Knight", 0x163D, 0x04),
    LD(517_14_11, r.Lab4, "Cell Key Chest", 0x1627, 0x10),
    LD(517_14_12, r.Lab4, "Miracle Herb Chest", 0x1627, 0x04),
    LD(517_15_00, r.Lab4Orb, "Light Blade Chest", 0x1627, 0x01),
    LD(517_22_00, r.Lab4Cell, "Meet Jessa", 0x163F, 0x01, i.Jessa),
    LD(517_22_01, r.Lab4Cell, "Receive Magic Ring from King", 0x161A, 0x02, None, {i.Jessa}),
]

lab5_locations = [
    LD(517_23_00, r.Lab5, "Mithril Ore Chest", 0x1629, 0x01),
    LD(517_23_01, r.Lab5, "1000g Chest", 0x1628, 0x08),
    LD(517_23_02, r.Lab5, "Magic Robe Chest", 0x1628, 0x02),
    LD(517_23_03, r.Lab5, "Defeat Hand Eater 1", 0x1628, 0x04),
    LD(517_23_04, r.Lab5, "Magic Ring Chest", 0x1628, 0x10),
    LD(517_23_05, r.Lab5, "Defeat Hand Eater 2", 0x1629, 0x08),
    LD(517_23_06, r.Lab5, "Defeat Hand Eater 3", 0x1629, 0x40),
    LD(517_23_07, r.Lab5, "Dark Scimitar Chest", 0x1629, 0x80),
    LD(517_23_08, r.Lab5, "Dark Block Chest", 0x1628, 0x01),
    LD(517_23_09, r.Lab5, "2000g Chest", 0x1629, 0x10),
    LD(517_23_10, r.Lab5, "200g Chest", 0x1629, 0x04),
    LD(517_23_11, r.Lab5, "Light Armor Chest", 0x1629, 0x02),
    LD(517_23_12, r.Lab5, "Miracle Herb Chest", 0x1629, 0x20),
    LD(517_23_13, r.Lab5, "Defeat Dark Sol", 0x1607, 0x80, i.DarkSol),
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
