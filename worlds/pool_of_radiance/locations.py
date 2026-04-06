from collections.abc import Callable
from dataclasses import dataclass
from types import TracebackType
from typing import NamedTuple

from Data import area_name as a
from Data import item_name as i
from rule_builder.rules import Rule

from .constants import rom, sram
from .items import ItemType
from .laglib import IntSpan, MemoryManager


class FlagCheck(NamedTuple):
    span: IntSpan
    predicate: Callable[[int], bool]

    def __repr__(self):
        return repr(self.span) + "?"

    def test(self, mem: MemoryManager):
        value = self.span.get(mem)
        return self.predicate(value)


def flag(address: int, predicate: Callable[[int], bool]):
    return FlagCheck(sram(address, 1), predicate)


def ram_eq(address: int, match: int):
    def check(value: int):
        return value == match

    return flag(address, check)


def ram_and(address: int, match: int):
    def check(value: int):
        return (value & match) > 0

    return flag(address, check)


def check_nz(value: int):
    return value != 0


def ram_nz(address: int):
    return flag(address, check_nz)


@dataclass
class LocationData:
    id: int
    region_name: str
    name: str
    vanilla_item: str
    checks: list[FlagCheck]
    restricted_types: set[ItemType]
    fixed_item: str | None = None
    rom_location: IntSpan | None = None
    rule: Rule | None = None


@dataclass
class Region:
    id: int
    name: str
    locations: list[LocationData]

    def __enter__(self):
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        return False

    def next_id(self):
        id = self.id
        self.id += 1
        return id

    def add(
        self,
        name: str,
        vanilla_item: str,
        checks: list[FlagCheck],
        restricted_types: set[ItemType] | None = None,
        fixed_item: str | None = None,
        rom_location: IntSpan | None = None,
        rule: Rule | None = None,
    ):
        self.locations.append(
            LocationData(
                self.next_id(),
                self.name,
                name,
                vanilla_item,
                checks,
                restricted_types or set(),
                fixed_item,
                rom_location,
                rule,
            )
        )


new_phlan_locations: list[LocationData] = []
with Region(1_000_000, a.NewPhlan, new_phlan_locations) as region:
    region.add("Slums Cleared", i.SlumsCleared, [ram_eq(0x76CD, 0xFE)], fixed_item=i.SlumsCleared)


slums_locations: list[LocationData] = []
with Region(1_001_000, a.Slums, slums_locations) as region:
    region.add("Cleared", i.Nothing, [ram_eq(0x76CD, 0xFF)], fixed_item=i.Nothing)

    for x in range(1, 25 + 1):
        region.add(f"Done {x} fights", i.SlumsFightCredit, [ram_eq(0x7692, x)], fixed_item=i.Nothing)

    region.add("Fought Shop Guards", i.Nothing, [ram_nz(0x766A)], fixed_item=i.Nothing)
    region.add("Killed Gypsy", i.Nothing, [ram_nz(0x7694)], fixed_item=i.Nothing)
    region.add("Floorboard Treasure", i.Nothing, [ram_nz(0x7695)], fixed_item=i.Nothing)
    region.add("Dirty Room Treasure", i.Nothing, [ram_nz(0x76DE)], fixed_item=i.Nothing)
    region.add("Secret Treasure Room", i.Nothing, [ram_nz(0x76E8)], fixed_item=i.Nothing)
    region.add(
        "Gave Ohlo the Potion",
        i.Treasure76,
        [ram_and(0x7693, 0x02)],
        rom_location=rom(36, 0x9A66, 1),
    )
    region.add("Orcs Fight", i.Nothing, [ram_and(0x76D5, 0x01)], fixed_item=i.Nothing)
    region.add("Goblins Fight", i.Nothing, [ram_and(0x76D5, 0x02)], fixed_item=i.Nothing)
    region.add("Kobolds Fight", i.Nothing, [ram_and(0x76D5, 0x04)], fixed_item=i.Nothing)
    region.add("Hobgoblins Fight", i.Nothing, [ram_and(0x76D5, 0x08)], fixed_item=i.Nothing)
    region.add("Big Orc Fight", i.Nothing, [ram_and(0x76D5, 0x10)], fixed_item=i.Nothing)
    region.add("Guards Fight", i.Nothing, [ram_and(0x76D5, 0x20)], fixed_item=i.Nothing)
    region.add("Ogre Fight", i.Nothing, [ram_and(0x76D5, 0x40)], fixed_item=i.Nothing)
    region.add("Leaders Fight", i.Nothing, [ram_and(0x76D5, 0x80)], fixed_item=i.Nothing)
    region.add("Flour Troll Fight", i.Nothing, [ram_nz(0x76EB)], fixed_item=i.Nothing)


all_locations = new_phlan_locations + slums_locations

locations_by_id = {location.id: location for location in all_locations}
locations_by_name = {location.name: location for location in all_locations}

location_name_groups = {
    "New Phlan": {loc.name for loc in new_phlan_locations},
    "Slums": {loc.name for loc in slums_locations},
}
