
from typing import NamedTuple, Optional

from .Names import ItemName as I, RegionName as R
from .Constants import CHEST_FLAG_START, CHEST_FLAG_END, CHEST_CONTENTS_BY_FLOOR

mask_to_offset = {0x01: 0, 0x02: 1, 0x04: 2,
                  0x08: 3, 0x10: 4, 0x20: 5, 0x40: 6, 0x80: 7}


class Replacement(NamedTuple):
    address: int
    size: int

    def format(self, value: int):
        return value.to_bytes(self.size, 'big')


class LD(NamedTuple):
    id: int
    region_name: str
    item_name: str
    check_address: int
    check_mask: int
    fixed_item: Optional[str] = None
    required_items: Optional[set[str]] = None

    @property
    def name(self):
        return f'{self.region_name} - {self.item_name}'

    @property
    def is_chest(self):
        return self.check_address >= CHEST_FLAG_START and self.check_address < CHEST_FLAG_END

    @property
    def rom_locations(self):
        if self.is_chest:
            floor_no = (self.check_address - CHEST_FLAG_START) // 2
            addr = CHEST_CONTENTS_BY_FLOOR[floor_no] + \
                mask_to_offset[self.check_mask]
            if not self.check_address & 1:
                addr += 8
            return [Replacement(addr, 1)]
        else:
            if self.check_address == 0x1616 and self.check_mask == 0x01:
                return [Replacement(0x5a141, 1)]
            if self.check_address == 0x1618 and self.check_mask == 0x02:
                return [Replacement(0x22a9f, 1), Replacement(0x22ab3, 1)]
            if self.check_address == 0x161a and self.check_mask == 0x02:
                return [Replacement(0x22226, 2), Replacement(0x22234, 2)]
            raise Exception('Cannot get ROM locations for %04x/%02x' %
                            (self.check_address, self.check_mask))


lab1_locations = [
    LD(517_00_00, R.Lab1, 'Herb Chest 1', 0x1620, 0x08),
    LD(517_00_01, R.Lab1, '50g Chest', 0x1620, 0x04),
    LD(517_00_02, R.Lab1, 'Bronze Knife Chest', 0x1620, 0x01),
    LD(517_00_03, R.Lab1, 'Herb Chest 2', 0x1620, 0x02),
    LD(517_00_04, R.Lab1, 'Herb Chest 3', 0x1621, 0x01),
    LD(517_00_05, R.Lab1, '100g Chest', 0x1621, 0x04),
    LD(517_00_06, R.Lab1, 'Defeat Kaiser Krab', 0x163F, 0x02, I.KaiserKrab),
    LD(517_00_07, R.Lab1, "Receive Dwarf's Key from Minister",
       0x1616, 0x01, None, set([I.KaiserKrab])),

    LD(517_01_00, R.Lab1Str, 'Depoison Chest', 0x1621, 0x20),
    LD(517_01_01, R.Lab1Str, 'Herb Chest', 0x1621, 0x40),
    LD(517_01_02, R.Lab1Str, 'Wisdom Seed Chest', 0x1621, 0x80),

    LD(517_03_00, R.Lab1Cou, 'Smelling Salts Chest', 0x1621, 0x02),
    LD(517_03_01, R.Lab1Cou, 'Morning Star Chest', 0x1621, 0x08),

    LD(517_05_00, R.Lab1Tru, '100g Chest', 0x1621, 0x10),
]

str_locations = [
    LD(517_02_00, R.Str, 'Defeat Chest Beak 1', 0x1633, 0x01),
    LD(517_02_01, R.Str, 'Wisdom Seed Chest 1', 0x1633, 0x02),
    LD(517_02_02, R.Str, 'Defeat Chest Beak 2', 0x1633, 0x20),
    LD(517_02_03, R.Str, 'Wisdom Seed Chest 2', 0x1633, 0x40),
    LD(517_02_04, R.Str, 'Depoison Chest', 0x1633, 0x80),
    LD(517_02_05, R.Str, '100g Chest', 0x1632, 0x08),
    LD(517_02_06, R.Str, 'Smelling Salts Chest', 0x1632, 0x10),
    LD(517_02_07, R.Str, 'Herb Chest', 0x1632, 0x01),
    LD(517_02_08, R.Str, 'Defeat Chest Beak 3', 0x1632, 0x04),
    LD(517_02_09, R.Str, 'Woven Robe Chest', 0x1632, 0x20),
    LD(517_02_10, R.Str, 'Meet Gila', 0x163D, 0x01, I.Gila),
    LD(517_02_11, R.Str, 'Short Sword Chest', 0x1633, 0x10),
    LD(517_02_12, R.Str, 'Wisdom Seed Chest 3', 0x1633, 0x04),
    LD(517_02_13, R.Str, 'Door of Strength', 0x1608, 0x01, I.TrialOfStrength),
    LD(517_02_14, R.Str, 'Healer Fruit Chest', 0x1635, 0x01),

    LD(517_11_00, R.StrRope, 'Mithril Ore Chest', 0x1632, 0x02),

    LD(517_16_00, R.StrCell, 'Forbidden Box Chest', 0x1633, 0x08),
]

cou_locations = [
    LD(517_04_00, R.Cou, 'Wisdom Seed Chest 1', 0x1637, 0x01),
    LD(517_04_01, R.Cou, '50g Chest', 0x1637, 0x02),
    LD(517_04_02, R.Cou, 'Angel Feather Chest', 0x1637, 0x10),
    LD(517_04_03, R.Cou, 'Woven Robe Chest', 0x1637, 0x20),
    LD(517_04_04, R.Cou, 'Defeat Chest Beak', 0x1637, 0x40),
    LD(517_04_05, R.Cou, 'Morning Star Chest', 0x1637, 0x80),
    LD(517_04_06, R.Cou, '100g Chest', 0x1637, 0x04),
    LD(517_04_07, R.Cou, 'Depoison Chest', 0x1636, 0x01),
    LD(517_04_08, R.Cou, 'Smelling Salts Chest', 0x1637, 0x08),
    LD(517_04_09, R.Cou, 'Bronze Shield Chest', 0x1636, 0x04),
    LD(517_04_10, R.Cou, 'Healer Fruit Chest', 0x1636, 0x40),
    LD(517_04_11, R.Cou, 'Wisdom Seed Chest 2', 0x1636, 0x08),
    LD(517_04_12, R.Cou, 'Woven Hood Chest', 0x1636, 0x20),
    LD(517_04_13, R.Cou, 'Door of Courage', 0x1608, 0x02, I.TrialOfCourage),
    LD(517_04_14, R.Cou, 'Defeat Tortolyde', 0x163F, 0x04, I.Tortolyde),

    LD(517_17_00, R.CouCell, 'Demon Staff Chest', 0x1636, 0x02),
]

tru_locations = [
    LD(517_06_00, R.Tru, 'Wisdom Seed Chest', 0x1630, 0x10),
    LD(517_06_01, R.Tru, '50g Chest', 0x1630, 0x04),
    LD(517_06_02, R.Tru, 'Wood Staff Chest', 0x1631, 0x80),
    LD(517_06_03, R.Tru, 'Healer Fruit Chest', 0x1631, 0x10),
    LD(517_06_04, R.Tru, 'Depoison Chest', 0x1630, 0x01),
    LD(517_06_05, R.Tru, 'Defeat Ghost 1', 0x1630, 0x40),
    LD(517_06_06, R.Tru, 'Angel Feather Chest', 0x1630, 0x20),
    LD(517_06_07, R.Tru, 'False Idol Chest', 0x1630, 0x02),
    LD(517_06_08, R.Tru, 'Defeat Ghost 2', 0x1631, 0x20),
    LD(517_06_09, R.Tru, 'Smelling Salts Chest', 0x1630, 0x08),
    LD(517_06_10, R.Tru, 'Chain Mail Chest', 0x1631, 0x01),
    LD(517_06_11, R.Tru, 'Battle Axe Chest', 0x1631, 0x04),
    LD(517_06_12, R.Tru, 'Door of Truth', 0x1608, 0x04, I.TrialOfTruth),

    LD(517_07_00, R.TruIdol, 'Defeat Doppler', 0x163D, 0x10, I.Doppler),
    LD(517_07_01, R.TruIdol, 'Rune Key Chest', 0x1631, 0x08),

    LD(517_18_00, R.TruCell, 'Magic Ring Chest', 0x1631, 0x40),
]

wis_locations = [
    LD(517_08_00, R.Wis, 'Map 1 Chest', 0x162B, 0x40),
    LD(517_08_01, R.Wis, 'Battle Axe Chest', 0x162B, 0x80),
    LD(517_08_02, R.Wis, 'Map 2 Chest', 0x162B, 0x04),
    LD(517_08_03, R.Wis, 'Meet Dai', 0x163D, 0x40, I.Dai),
    LD(517_08_04, R.Wis, 'Smelling Salts Chest', 0x162A, 0x04),
    LD(517_08_05, R.Wis, 'Flail Chest', 0x162B, 0x20),
    LD(517_08_06, R.Wis, 'Defeat Ghost', 0x162B, 0x01),
    LD(517_08_07, R.Wis, 'Dark Block Chest', 0x162B, 0x08),
    LD(517_08_08, R.Wis, 'Herb-Water Chest', 0x162A, 0x01),
    LD(517_08_09, R.Wis, 'Mithril Ore Chest', 0x162B, 0x02),
    LD(517_08_10, R.Wis, 'Door of Wisdom', 0x1608, 0x08, I.TrialOfWisdom),
    LD(517_08_11, R.Wis, 'Fire Sword Chest', 0x162D, 0x02),
    LD(517_08_12, R.Wis, '200g Chest', 0x162D, 0x01),

    LD(517_19_00, R.WisCell, 'Defeat Ghost', 0x162A, 0x02),
]

lab2_locations = [
    LD(517_09_00, R.Lab2, 'Mithril Ore Chest', 0x1623, 0x10),
    LD(517_09_01, R.Lab2, '500g Chest', 0x1622, 0x01),
    LD(517_09_02, R.Lab2, 'Depoison Chest', 0x1622, 0x04),
    LD(517_09_03, R.Lab2, 'Great Axe Chest', 0x1622, 0x02),
    LD(517_09_04, R.Lab2, 'Angel Feather Chest', 0x1623, 0x02),
    LD(517_09_05, R.Lab2, 'Magic Hood Chest', 0x1623, 0x01),
    LD(517_09_06, R.Lab2, 'Fire Staff Chest', 0x1623, 0x08),
    LD(517_09_07, R.Lab2, 'Smelling Salts Chest', 0x1623, 0x20),
    LD(517_09_08, R.Lab2, 'Healer Fruit Chest', 0x1623, 0x04),
    LD(517_09_09, R.Lab2, 'Sun Armor Chest', 0x1622, 0x08),
    LD(517_09_10, R.Lab2, 'Worn Robe Chest', 0x1623, 0x80),
    LD(517_09_11, R.Lab2, '300g Chest', 0x1623, 0x40),

    LD(517_20_00, R.Lab2Cell, 'Barrier Ring Chest', 0x1622, 0x10),
]

lab3_locations = [
    LD(517_10_00, R.Lab3, 'Entered Labyrinth L3', 0x1605, 0x30, I.EnterLab3),
    LD(517_10_01, R.Lab3, 'Defeat Shell Beast', 0x1640, 0x10, I.ShellBeast),
    LD(517_10_02, R.Lab3, 'Receive Medallion from Xern', 0x1618,
       0x02, I.Medallion),  # TODO what is the requirement for this?
    LD(517_10_03, R.Lab3, '500g Chest', 0x1625, 0x20),
    LD(517_10_04, R.Lab3, 'Mystic Rope Chest', 0x1624, 0x01),
    LD(517_10_05, R.Lab3, 'Healer Fruit Chest', 0x1624, 0x02),
    LD(517_10_06, R.Lab3, 'Herb-Water Chest', 0x1625, 0x10),
    LD(517_10_07, R.Lab3, 'Ice Staff Chest', 0x1625, 0x40),
    LD(517_10_08, R.Lab3, 'Light Helm Chest', 0x1625, 0x02),

    LD(517_12_00, R.Lab3Rope, 'Storm Sword Chest', 0x1625, 0x08),
    LD(517_12_01, R.Lab3Rope, 'Great Flail Chest', 0x1625, 0x08),

    LD(517_13_00, R.Lab3RopeOrCell, 'Mithril Ore Chest', 0x1625, 0x80),

    LD(517_21_00, R.Lab3Cell, 'Light Shield Chest', 0x1625, 0x01),
]

lab4_locations = [
    LD(517_14_00, R.Lab4, 'Endurostaff Chest', 0x1626, 0x08),
    LD(517_14_01, R.Lab4, 'Elven Hood Chest', 0x1627, 0x02),
    LD(517_14_02, R.Lab4, 'Holy Water Chest', 0x1626, 0x04),
    LD(517_14_03, R.Lab4, 'Healer Fruit Chest', 0x1626, 0x10),
    LD(517_14_04, R.Lab4, 'Herb-Water Chest', 0x1626, 0x02),
    LD(517_14_05, R.Lab4, 'Steel Whip Chest', 0x1627, 0x40),
    LD(517_14_06, R.Lab4, 'Heal Ring Chest', 0x1627, 0x08),
    LD(517_14_07, R.Lab4, 'Defeat Hand Eater 1', 0x1627, 0x20),
    LD(517_14_08, R.Lab4, 'Defeat Hand Eater 2', 0x1627, 0x80),
    LD(517_14_09, R.Lab4, 'Frost Armor Chest', 0x1626, 0x01),
    LD(517_14_10, R.Lab4, 'Defeat Dark Knight', 0x163D, 0x04),
    LD(517_14_11, R.Lab4, 'Cell Key Chest', 0x1627, 0x10),
    LD(517_14_12, R.Lab4, 'Miracle Herb Chest', 0x1627, 0x04),

    LD(517_15_00, R.Lab4Orb, 'Light Blade Chest', 0x1627, 0x01),

    LD(517_22_00, R.Lab4Cell, 'Meet Jessa', 0x163F, 0x01, I.Jessa),
    LD(517_22_01, R.Lab4Cell, 'Receive Magic Ring from King',
       0x161A, 0x02, None, set([I.Jessa])),
]

lab5_locations = [
    LD(517_23_00, R.Lab5, 'Mithril Ore Chest', 0x1629, 0x01),
    LD(517_23_01, R.Lab5, '1000g Chest', 0x1628, 0x08),
    LD(517_23_02, R.Lab5, 'Magic Robe Chest', 0x1628, 0x02),
    LD(517_23_03, R.Lab5, 'Defeat Hand Eater 1', 0x1628, 0x04),
    LD(517_23_04, R.Lab5, 'Magic Ring Chest', 0x1628, 0x10),
    LD(517_23_05, R.Lab5, 'Defeat Hand Eater 2', 0x1629, 0x08),
    LD(517_23_06, R.Lab5, 'Defeat Hand Eater 3', 0x1629, 0x40),
    LD(517_23_07, R.Lab5, 'Dark Scimitar Chest', 0x1629, 0x80),
    LD(517_23_08, R.Lab5, 'Dark Block Chest', 0x1628, 0x01),
    LD(517_23_09, R.Lab5, '2000g Chest', 0x1629, 0x10),
    LD(517_23_10, R.Lab5, '200g Chest', 0x1629, 0x04),
    LD(517_23_11, R.Lab5, 'Light Armor Chest', 0x1629, 0x02),
    LD(517_23_12, R.Lab5, 'Miracle Herb Chest', 0x1629, 0x20),
    LD(517_23_13, R.Lab5, 'Defeat Dark Sol', 0x1607, 0x80, I.DarkSol),
]

all_locations = lab1_locations + str_locations + cou_locations + tru_locations + \
    wis_locations + lab2_locations + lab3_locations + lab4_locations + lab5_locations
chest_locations = [location for location in all_locations if location.is_chest]

locations_by_id = {location.id: location for location in all_locations}
locations_by_name = {location.name: location for location in all_locations}

location_name_groups = {
    'Labyrinth L1': {loc.name for loc in lab1_locations},
    'Labyrinth L2': {loc.name for loc in lab2_locations},
    'Labyrinth L3': {loc.name for loc in lab3_locations},
    'Labyrinth L4': {loc.name for loc in lab4_locations},
    'Labyrinth L5': {loc.name for loc in lab5_locations},
    'Cave of Strength': {loc.name for loc in str_locations},
    'Cave of Courage': {loc.name for loc in cou_locations},
    'Cave of Truth': {loc.name for loc in tru_locations},
    'Cave of Wisdom': {loc.name for loc in wis_locations},
}
