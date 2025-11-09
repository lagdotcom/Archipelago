import logging
import os
import settings

from typing import Any, Callable, ClassVar, Optional, Sequence, Tuple
from BaseClasses import CollectionState, Item, Location, MultiWorld, Region, Tutorial
from .Goals import get_goal_data
from .Items import all_items, items_by_name, item_name_groups, useful_item_names, filler_item_names
from .Locations import all_locations, chest_locations, location_name_groups
from .Names import RegionName
from .Options import SITDOptions
from .Regions import all_regions, regions_by_name
from .Rom import SITD_UE_HASH, SITDProcedurePatch, get_base_rom_path, write_tokens
from ..AutoWorld import WebWorld, World
from .Client import SITDClient  # type: ignore

logger = logging.getLogger("Shining in the Darkness")


class SITDLocation(Location):
    game: str = "Shining in the Darkness"


class SITDItem(Item):
    game: str = "Shining in the Darkness"


class SITDSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Shining in the Darkness US/EU rom"""
        copy_to = "Shining in the Darkness (UE) [!].gen"
        description = "Shining in the Darkness ROM File"
        md5s = [SITD_UE_HASH]

        def browse(self: settings.T,
                   filetypes: Optional[Sequence[Tuple[str,
                                                      Sequence[str]]]] = None,
                   **kwargs: Any) -> Optional[settings.T]:
            if not filetypes:
                file_types = [("GEN", [".gen"]), ("BIN", [".bin"]),
                              ("SMD", [".smd"]), ("68K", [".68k"]),]
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


class SITDWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Shining in the Dark randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["lagdotcom"]
    )]


class SITDWorld(World):
    """
    Shining in the Darkness is a dungeon crawler in a series full of strategy games.
    """
    game = "Shining in the Darkness"
    options_dataclass = SITDOptions
    options: SITDOptions  # type: ignore
    settings: ClassVar[SITDSettings]  # type: ignore
    web = SITDWeb()
    required_client_version = (0, 5, 0)

    item_name_to_id = {item.name: item.id for item in all_items}
    item_name_groups = item_name_groups

    location_name_to_id = {data.name: data.id for data in all_locations}
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

        menu = Region(RegionName.Menu, player, multiworld)
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
            loc = SITDLocation(player, info.name, info.id, region)
            region.locations.append(loc)

        # make connections
        menu.connect(multiworld.get_region(RegionName.Lab1, player))

        for info in all_regions:
            if not goal.has_region(info.name):
                continue
            if len(info.exits):
                region = multiworld.get_region(info.name, player)
                for (exit_name, item_lists) in info.exits.items():
                    if not goal.has_region(exit_name):
                        continue
                    # logger.debug('connect [%s] to [%s]', info.name, exit_name)
                    destination = multiworld.get_region(exit_name, player)
                    region.connect(destination, None,
                                   self.make_exit_rule(item_lists))

    def make_exit_rule(self, item_lists: list[list[str]]) -> Optional[Callable[[CollectionState], bool]]:
        if len(item_lists) == 0:
            return None
        return lambda state: self.check_exit_rule(state, item_lists)

    def check_exit_rule(self, state: CollectionState, item_lists: list[list[str]]):
        for items in item_lists:
            if state.has_all(items, self.player):
                return True
        return False

    def set_rules(self):
        goal = get_goal_data(self.options.goal.value)
        self.multiworld.completion_condition[self.player] = goal.get_completion_function(
            self.player)

    def create_item(self, name: str):
        item = items_by_name[name]
        return SITDItem(name, item.classification, item.id, self.player)

    def get_fixed_location_for_item(self, name: str):
        for location_data in all_locations:
            if location_data.fixed_item == name:
                return location_data

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
                # logger.debug('force [%s] at [%s]', name, fixed_location.name)
                self.multiworld.get_location(
                    fixed_location.name, self.player).place_locked_item(item)
            else:
                # logger.debug('required: add [%s] to item pool', item.name)
                self.multiworld.itempool.append(item)
            added_items.append(item.name)

        remaining = len(list(self.get_locations())) - len(added_items)
        # print(f'remaining location count: {remaining}')

        if options.useful_items.value > 0:
            useful = useful_item_names[:]
            useful_count = min(
                int(remaining * 100 // options.useful_items.value), len(useful))
            self.random.shuffle(useful)
            for name in useful[:useful_count]:
                # logger.debug('useful: add [%s] to item pool', name)
                self.multiworld.itempool.append(self.create_item(name))
                remaining -= 1

        for _ in range(remaining):
            name = self.get_filler_item_name()
            # logger.debug('filler: add [%s] to item pool', name)
            self.multiworld.itempool.append(self.create_item(name))

    def get_filler_item_name(self):
        return self.random.choice(filler_item_names)

    # def fill_slot_data(self) -> Mapping[str, Any]:
    #     return self.options.as_dict()

    def generate_output(self, output_directory: str) -> None:
        patch = SITDProcedurePatch(player=self.player,
                                   player_name=self.multiworld.player_name[self.player])
        write_tokens(self, patch, chest_locations)

        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
        patch.write(rom_path)
