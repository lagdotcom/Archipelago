from .laglib import IntSpan, StrSpan
from .laglib import genesis_ram as ram
from .laglib import genesis_rom as rom

game_name = "Shining in the Darkness"

# RAM addresses

ram_names = {
    0x1600: "party",
}

# 1600 changes whenever entering battle, so ignore it for now
quest_flags_span = IntSpan(ram, 0x1601, 0x1648)
chest_flags_span = IntSpan(ram, 0x1620, 0x1A)
inventory_span = IntSpan(ram, 0x16EA, 0x30)
gold_span = IntSpan(ram, 0x16A4, 4)
hero_max_hp_span = IntSpan(ram, 0x16B4, 2)

# TODO find a good place for this
received_item_storage = IntSpan(ram, 0xC7FE, 2)

# ROM addresses

"""
possibly useful ROM addresses

~2D30   initial RAM:1600 block?
~69E4   item names, enemy names, npc names
"""

rom_international_name = StrSpan(rom, 0x150, 32)
rom_version = StrSpan(rom, 0x18C, 2)


LAB_L1_CHEST_CONTENTS = 0x84C6
LAB_L2_CHEST_CONTENTS = 0x84D3
LAB_L3_CHEST_CONTENTS = 0x84E1
LAB_L4_CHEST_CONTENTS = 0x84EC
LAB_L5_CHEST_CONTENTS = 0x84FA
WIS_L1_CHEST_CONTENTS = 0x8508
WIS_L2_CHEST_CONTENTS = 0x8508
UNUSED_CHEST_CONTENTS = 0x8517
TRUTH_CHEST_CONTENTS = 0x8518
STRENGTH_L1_CHEST_CONTENTS = 0x8528
SHARED_L2_CHEST_CONTENTS = 0x8537
COURAGE_L1_CHEST_CONTENTS = 0x8539
CHEST_CONTENTS_BY_FLOOR = [
    LAB_L1_CHEST_CONTENTS,
    LAB_L2_CHEST_CONTENTS,
    LAB_L3_CHEST_CONTENTS,
    LAB_L4_CHEST_CONTENTS,
    LAB_L5_CHEST_CONTENTS,
    WIS_L1_CHEST_CONTENTS,
    WIS_L2_CHEST_CONTENTS,
    UNUSED_CHEST_CONTENTS,
    TRUTH_CHEST_CONTENTS,
    STRENGTH_L1_CHEST_CONTENTS,
    SHARED_L2_CHEST_CONTENTS,
    COURAGE_L1_CHEST_CONTENTS,
]

name_space = StrSpan(rom, 0xFFF30, 0xCF, "utf-8")
goal_space = IntSpan(rom, 0xFFFFF, 1)
