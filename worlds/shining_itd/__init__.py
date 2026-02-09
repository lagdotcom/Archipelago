import logging
import os
from collections.abc import Sequence
from typing import Any, ClassVar

import settings
from BaseClasses import Item, Location, MultiWorld, Region, Tutorial
from rule_builder.rules import HasAll

from ..AutoWorld import WebWorld, World
from .client import SITDClient  # type: ignore  # noqa: F401
from .constants import game_name
from .goals import get_goal_data
from .items import all_items, filler_item_names, item_name_groups, items_by_name, useful_item_names
from .locations import all_locations, location_name_groups
from .Names import region_name
from .options import SITDOptions
from .regions import all_regions, regions_by_name
from .rom import SITD_UE_HASH, SITDProcedurePatch, get_base_rom_path, write_tokens

logger = logging.getLogger(game_name)


class SITDLocation(Location):
    game: str = game_name


class SITDItem(Item):
    game: str = game_name


class SITDSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Shining in the Darkness US/EU rom"""

        copy_to = "Shining in the Darkness (UE) [!].gen"
        description = "Shining in the Darkness ROM File"
        md5s: ClassVar[list[str | bytes]] = [SITD_UE_HASH]

        def browse(
            self: settings.T, filetypes: Sequence[tuple[str, Sequence[str]]] | None = None, **kwargs: Any
        ) -> settings.T | None:
            if not filetypes:
                file_types = [
                    ("GEN", [".gen"]),
                    ("BIN", [".bin"]),
                    ("SMD", [".smd"]),
                    ("68K", [".68k"]),
                ]
                return super().browse(file_types, **kwargs)
            return super().browse(filetypes, **kwargs)

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .gen file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = True


class SITDWeb(WebWorld):
    tutorials: ClassVar[list[Tutorial]] = [  # type: ignore
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Shining in the Dark randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["lagdotcom"],
        )
    ]


class SITDWorld(World):
    """
    Shining in the Darkness is a dungeon crawler in a series full of strategy games.
    """

    game = game_name
    options_dataclass = SITDOptions
    options: SITDOptions  # type: ignore
    settings: ClassVar[SITDSettings]  # type: ignore
    web = SITDWeb()
    required_client_version = (0, 5, 0)

    item_name_to_id: ClassVar[dict[str, int]] = {item.name: item.id for item in all_items}
    item_name_groups = item_name_groups

    location_name_to_id: ClassVar[dict[str, int]] = {data.name: data.id for data in all_locations}
    location_name_groups = location_name_groups

    # def __init__(self, multiworld: MultiWorld, player: int):
    #     super().__init__(multiworld, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    # def generate_early(self):
    #     return super().generate_early()

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        options = self.options
        goal = get_goal_data(options.goal.value)

        menu = Region(region_name.Menu, player, multiworld)
        multiworld.regions.append(menu)

        # make regions
        for name in goal.region_names:
            info = regions_by_name[name]
            # logger.debug("add region: [%s]", info.name)
            region = Region(info.name, player, multiworld)
            multiworld.regions.append(region)

        # make locations
        for info in all_locations:
            if not goal.has_region(info.region_name):
                continue
            region = multiworld.get_region(info.region_name, player)
            # logger.debug("add location [%s] to region [%s]", info.name, region.name)
            loc = SITDLocation(player, info.name, info.id, region)
            if info.rule is not None:
                self.set_rule(loc, info.rule)
            region.locations.append(loc)

        # make connections
        menu.connect(multiworld.get_region(region_name.Lab1, player))

        for info in all_regions:
            if not goal.has_region(info.name):
                continue
            if len(info.exits):
                region = multiworld.get_region(info.name, player)
                for exit_name, rule in info.exits.items():
                    if not goal.has_region(exit_name):
                        continue
                    # logger.debug("connect [%s] to [%s]", info.name, exit_name)
                    destination = multiworld.get_region(exit_name, player)
                    entrance = region.connect(destination)
                    self.set_rule(entrance, rule)

    def set_rules(self):
        goal = get_goal_data(self.options.goal.value)
        self.set_completion_rule(HasAll(*goal.completion_item_names))

    def create_item(self, name: str):
        item = items_by_name[name]
        return SITDItem(name, item.classification, item.id, self.player)

    def get_fixed_location_for_item(self, name: str):
        for location_data in all_locations:
            if location_data.fixed_item == name:
                return location_data
        return None

    def create_items(self):
        options = self.options
        goal = get_goal_data(options.goal.value)
        added_items: list[str] = []

        # required_item_names = [item.name for item in required_items]
        # place_early_names = set(required_item_names + reward_item_names)

        for name in goal.required_item_names:
            item = self.create_item(name)
            fixed_location = self.get_fixed_location_for_item(name)
            if fixed_location:
                # logger.debug("force [%s] at [%s]", name, fixed_location.name)
                self.multiworld.get_location(fixed_location.name, self.player).place_locked_item(item)
            else:
                # logger.debug("required: add [%s] to item pool", item.name)
                self.multiworld.itempool.append(item)
            added_items.append(item.name)

        remaining = len(list(self.get_locations())) - len(added_items)
        # logger.debug(f"remaining location count: {remaining}")

        if options.useful_items.value > 0:
            useful = useful_item_names[:]
            useful_count = min(int(remaining * options.useful_items.value // 100), len(useful))
            self.random.shuffle(useful)
            for name in useful[:useful_count]:
                # logger.debug("useful: add [%s] to item pool", name)
                self.multiworld.itempool.append(self.create_item(name))
                remaining -= 1

        for _ in range(remaining):
            name = self.get_filler_item_name()
            # logger.debug("filler: add [%s] to item pool", name)
            self.multiworld.itempool.append(self.create_item(name))

    def get_filler_item_name(self):
        return self.random.choice(filler_item_names)

    # def fill_slot_data(self) -> Mapping[str, Any]:
    #     return self.options.as_dict()

    def generate_output(self, output_directory: str) -> None:
        patch = SITDProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_tokens(self, patch, all_locations)

        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"
        )
        patch.write(rom_path)
