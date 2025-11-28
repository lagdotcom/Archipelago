import logging
import os
import settings

from typing import Any, Callable, ClassVar, Iterable, Optional, Sequence, Tuple
from BaseClasses import CollectionState, Item, Location, MultiWorld, Region, Tutorial
from .Constants import game_name
from .Data import Area
from .Goals import get_goal_data
from .Items import (
    all_items,
    filler_item_names,
    item_name_groups,
    items_by_name,
    useful_item_names,
    ItemType,
)
from .Locations import all_locations, locations_by_name, location_name_groups
from .Options import PhSt2Options, DIST_SHUFFLE
from .Regions import all_regions, regions_by_name
from .Rom import REV02_UE_HASH, PhSt2ProcedurePatch, get_base_rom_path, write_tokens
from ..AutoWorld import WebWorld, World
from .Client import PhSt2Client  # type: ignore

logger = logging.getLogger(game_name)


class PhSt2Location(Location):
    game: str = game_name


class PhSt2Item(Item):
    game: str = game_name


def get_item_type(item: Item):
    if isinstance(item, PhSt2Item):
        return items_by_name[item.name].type
    # TODO if possible to fix NPC dialogue, this can be changed to ITEM for greater rando potential
    return ItemType.GARBAGE


class PhSt2Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Phantasy Star II US/EU REV02 rom"""

        copy_to = "Phantasy Star II (UE) (REV02) [!].gen"
        description = "Phantasy Star II REV02 ROM File"
        md5s = [REV02_UE_HASH]

        def browse(
            self: settings.T,
            filetypes: Optional[Sequence[Tuple[str, Sequence[str]]]] = None,
            **kwargs: Any,
        ) -> Optional[settings.T]:
            if not filetypes:
                file_types = [
                    ("GEN", [".gen"]),
                    ("BIN", [".bin"]),
                    ("SMD", [".smd"]),
                    ("68K", [".68k"]),
                ]
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .gen file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = True


class PhSt2Web(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Phantasy Star II randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["lagdotcom"],
        )
    ]


class PhSt2World(World):
    """
    Phantasy Star II is a JRPG where you explore the dark origins of Artificial Intelligence.
    """

    game = game_name
    options_dataclass = PhSt2Options
    options: PhSt2Options  # type: ignore
    settings: ClassVar[PhSt2Settings]  # type: ignore
    web = PhSt2Web()
    required_client_version = (0, 5, 0)

    item_name_to_id = {item.name: item.id for item in all_items}
    item_name_groups = item_name_groups

    location_name_to_id = {data.name: data.id for data in all_locations}
    location_name_groups = location_name_groups

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

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
            # logger.debug('add region: [%s]', info.name)
            region = Region(info.name, player, multiworld)
            multiworld.regions.append(region)

        # make locations
        for info in all_locations:
            if not goal.has_region(info.region_name):
                continue
            region = multiworld.get_region(info.region_name, player)
            # logger.debug('add location [%s] to region [%s]', info.name, region.name)
            loc = PhSt2Location(player, info.name, info.id, region)
            loc.item_rule = self.get_item_rule(info.restricted_types)
            if info.required_items:
                loc.access_rule = self.get_access_rule(info.required_items)
            region.locations.append(loc)

        # make connections
        menu.connect(multiworld.get_region(Area.Motavia, player))

        for info in all_regions:
            if not goal.has_region(info.name):
                continue
            if len(info.exits):
                region = multiworld.get_region(info.name, player)
                for exit_name, make_checker in info.exits.items():
                    if not goal.has_region(exit_name):
                        continue
                    # logger.debug('connect [%s] to [%s]', info.name, exit_name)
                    destination = multiworld.get_region(exit_name, player)
                    region.connect(destination, None, make_checker(player))

    def get_access_rule(
        self, items: Iterable[str]
    ) -> Callable[[CollectionState], bool]:
        capture = tuple(items)
        return lambda state: state.has_all(capture, self.player)

    def get_item_rule(self, types: Iterable[ItemType]) -> Callable[[Item], bool]:
        capture = tuple(types)
        return lambda item: get_item_type(item) in capture

    def set_rules(self):
        goal = get_goal_data(self.options.goal.value)
        self.multiworld.completion_condition[self.player] = (
            goal.get_completion_function(self.player)
        )

    def create_item(self, name: str):
        item = items_by_name[name]
        return PhSt2Item(name, item.classification, item.id, self.player)

    def get_fixed_location_for_item(self, name: str):
        for location_data in all_locations:
            if location_data.fixed_item == name:
                return location_data

    def create_items(self):
        options = self.options
        goal = get_goal_data(options.goal.value)
        required_items: list[str] = []

        # required_item_names = [item.name for item in required_items]
        # place_early_names = set(required_item_names + reward_item_names)

        for name in goal.required_item_names:
            item = self.create_item(name)
            fixed_location = self.get_fixed_location_for_item(name)
            if fixed_location:
                # logger.debug('force [%s] at [%s]', name, fixed_location.name)
                self.get_location(fixed_location.name).place_locked_item(item)
            else:
                required_items.append(item.name)

        if options.item_distribution.value == DIST_SHUFFLE:
            for location in self.get_locations():
                if not location.item:
                    data = locations_by_name[location.name]
                    # logger.debug("shuffle: add [%s] to item pool" % data.vanilla_item)
                    self.multiworld.itempool.append(self.create_item(data.vanilla_item))

        else:
            for required in required_items:
                # logger.debug("required: add [%s] to item pool", required)
                self.multiworld.itempool.append(self.create_item(required))

            remaining = len(list(self.get_locations())) - len(required_items)
            # print(f"remaining location count: {remaining}")

            if options.useful_items.value > 0:
                useful = useful_item_names[:]
                useful_count = min(
                    int(remaining * options.useful_items.value // 100), len(useful)
                )
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

    def generate_output(self, output_directory: str):
        patch = PhSt2ProcedurePatch(
            player=self.player, player_name=self.multiworld.player_name[self.player]
        )
        write_tokens(self, patch, all_locations)

        rom_path = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}",
        )
        patch.write(rom_path)
