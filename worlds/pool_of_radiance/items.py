from dataclasses import dataclass
from enum import IntEnum

from BaseClasses import ItemClassification

from .Data import item_name as i


class ItemType(IntEnum):
    Nothing = 0
    Treasure = 1
    Money = 2
    Flag = 3
    FlagAsItem = 4


@dataclass
class ItemData:
    id: int
    type: ItemType
    name: str
    classification: ItemClassification
    treasure_id: int | None = None
    gold_pieces: int = 0
    code: int | None = None


flag_items = [
    ItemData(1_000_000, ItemType.Flag, i.SlumsFightCredit, ItemClassification.progression),
    ItemData(1_000_001, ItemType.Flag, i.SlumsCleared, ItemClassification.progression),
    ItemData(1_000_999, ItemType.Flag, i.TyranthraxusDefeated, ItemClassification.progression),
]

treasure_items = [
    ItemData(1_100_001, ItemType.Treasure, i.Treasure01, ItemClassification.useful, 0x01),
    ItemData(1_100_002, ItemType.Treasure, i.Treasure02, ItemClassification.useful, 0x02),
    ItemData(1_100_003, ItemType.Treasure, i.Treasure03, ItemClassification.useful, 0x03),
    ItemData(1_100_004, ItemType.Treasure, i.Treasure04, ItemClassification.useful, 0x04),
    ItemData(1_100_005, ItemType.Treasure, i.Treasure05, ItemClassification.useful, 0x05),
    ItemData(1_100_006, ItemType.Treasure, i.Treasure06, ItemClassification.useful, 0x06),
    ItemData(1_100_020, ItemType.Treasure, i.Treasure14, ItemClassification.useful, 0x14),
    ItemData(1_100_118, ItemType.Treasure, i.Treasure76, ItemClassification.useful, 0x76),
    ItemData(1_100_119, ItemType.Treasure, i.Treasure77, ItemClassification.useful, 0x77),
]


junk_items = [
    ItemData(1_999_000, ItemType.Nothing, i.Nothing, ItemClassification.filler | ItemClassification.deprioritized),
]

filler_items = junk_items
filler_item_names = [item.name for item in filler_items]

item_name_groups = {
    "Quest Flags": {item.name for item in flag_items},
    "Treasure": {item.name for item in treasure_items},
    "Junk": {item.name for item in junk_items},
}

all_items = treasure_items + filler_items + flag_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}
