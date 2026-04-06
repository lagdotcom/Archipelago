import logging
import os
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, ClassVar

import settings
from BaseClasses import CollectionState, Item, Location, Region, Tutorial

from ..AutoWorld import WebWorld, World
from .client import PRClient  # type: ignore  # noqa: F401
from .constants import game_name
from .Data import area_name
from .goals import get_goal_data
from .items import ItemType, all_items, filler_item_names, item_name_groups, items_by_name
from .laglib import nes_file_types, use_re_gen_passthrough
from .locations import all_locations, location_name_groups, locations_by_name
from .options import DIST_SHUFFLE, PROptions, option_groups, options_presets
from .regions import all_regions, regions_by_name
from .rom import U_HASH, PRProcedurePatch, write_tokens

logger = logging.getLogger(game_name)


class PRLocation(Location):
    game: str = game_name


class PRItem(Item):
    game: str = game_name


def get_item_type(item: Item):
    if isinstance(item, PRItem):
        return items_by_name[item.name].type
    # TODO
    return ItemType.Garbage


class PRSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Pool of Radiance US rom"""

        copy_to = "Pool of Radiance (U).nes"
        description = "Pool of Radiance US ROM File"
        md5s: ClassVar[list[str | bytes]] = [U_HASH]

        def browse(
            self: settings.T,
            filetypes: Sequence[tuple[str, Sequence[str]]] | None = None,
            **kwargs: Any,
        ) -> settings.T | None:
            return super().browse(filetypes or nes_file_types, **kwargs)

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .gen file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = True


class PRWeb(WebWorld):
    game = game_name
    option_groups = option_groups
    options_presets = options_presets

    tutorials: ClassVar[list[Tutorial]] = [  # type: ignore
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Pool of Radiance randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["lagdotcom"],
        )
    ]


class PRWorld(World):
    """
    Pool of Radiance is an Advanced Dungeons & Dragons sandbox adventure.
    """

    game = game_name
    options_dataclass = PROptions
    options: PROptions  # type: ignore
    settings: ClassVar[PRSettings]  # type: ignore
    web = PRWeb()
    required_client_version = (0, 5, 0)
    ut_can_gen_without_yaml = True

    item_name_to_id: ClassVar[dict[str, int]] = {item.name: item.id for item in all_items}
    item_name_groups = item_name_groups

    location_name_to_id: ClassVar[dict[str, int]] = {data.name: data.id for data in all_locations}
    location_name_groups = location_name_groups

    location_count: int = 0

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        options = self.options
        goal = get_goal_data(options.goal.value)

        menu = Region("Menu", player, multiworld)
        multiworld.regions.append(menu)

        # make regions
        for region_name in goal.region_names:
            info = regions_by_name[region_name]
            logger.debug("add region: [%s]", info.name)
            region = Region(info.name, player, multiworld)
            multiworld.regions.append(region)

        # make locations
        for info in all_locations:
            if not goal.has_region(info.region_name):
                continue
            region = multiworld.get_region(info.region_name, player)
            logger.debug("add location [%s] to region [%s]", info.name, region.name)
            loc = PRLocation(player, info.name, info.id, region)
            loc.item_rule = self.get_item_rule(info.restricted_types)
            if info.rule is not None:
                self.set_rule(loc, info.rule)
            region.locations.append(loc)
            self.location_count += 1

        logger.debug("create_regions: %d locations", self.location_count)

        # make connections
        menu.connect(multiworld.get_region(area_name.NewPhlan, player))

        for info in all_regions:
            if not goal.has_region(info.name):
                continue
            if len(info.exits):
                region = multiworld.get_region(info.name, player)
                for exit_name, rule in info.exits.items():
                    if not goal.has_region(exit_name):
                        continue
                    logger.debug("connect [%s] to [%s]", info.name, exit_name)
                    destination = multiworld.get_region(exit_name, player)
                    entrance = region.connect(destination)
                    self.set_rule(entrance, rule)

    def get_access_rule(self, items: Iterable[str]) -> Callable[[CollectionState], bool]:
        capture = tuple(items)
        return lambda state: state.has_all(capture, self.player)

    def get_item_rule(self, types: Iterable[ItemType]) -> Callable[[Item], bool]:
        capture = tuple(types)
        return lambda item: get_item_type(item) in capture

    def set_rules(self):
        goal = get_goal_data(self.options.goal.value)
        self.multiworld.completion_condition[self.player] = goal.get_completion_function(self.player)

    def create_item(self, name: str):
        item = items_by_name[name]
        return PRItem(name, item.classification, item.id, self.player)

    def get_items_to_place(self):
        options = self.options
        required: list[str] = []
        optional: list[str] = []

        if options.item_distribution.value == DIST_SHUFFLE:
            for location in self.get_locations():
                data = locations_by_name[location.name]
                required.append(data.vanilla_item)
            logger.debug("shuffle: added %d items", len(required))
        else:
            raise Exception("DIST_RANDO not implemented yet")
            # goal = get_goal_data(options.goal.value)
            # required = list(goal.required_item_names)

            # spaces = self.location_count - len(required)
            # useful_count = spaces * options.useful_items.value // 100
            # filler_count = spaces - useful_count
            # logger.debug("rando: %d useful, %d filler", useful_count, filler_count)
            # optional += sample_repeating(self.random, useful_item_names, useful_count)
            # optional += sample_repeating(self.random, filler_item_names, filler_count)

        return required, optional

    def create_items(self):
        required, optional = self.get_items_to_place()

        for location in self.get_locations():
            data = locations_by_name[location.name]
            if data.fixed_item:
                item = self.create_item(data.fixed_item)
                if item.name in required:
                    required.remove(item.name)
                    resolution = "removed from required"
                elif item.name in optional:
                    optional.remove(item.name)
                    resolution = "removed from optional"
                else:
                    _ = optional.pop()
                    resolution = f"removed {_} from optional"
                logger.debug("fixed: [%s] at [%s]; %s", item.name, location.name, resolution)
                location.place_locked_item(item)

        for name in required + optional:
            logger.debug("pool: added %s", name)
            self.multiworld.itempool.append(self.create_item(name))

    def get_filler_item_name(self):
        return self.random.choice(filler_item_names)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "options": self.options.as_dict("goal"),
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    def generate_early(self):
        use_re_gen_passthrough(self)

    def generate_output(self, output_directory: str):
        patch = PRProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])

        write_tokens(self, patch, all_locations)

        rom_path = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}",
        )
        patch.write(rom_path)
