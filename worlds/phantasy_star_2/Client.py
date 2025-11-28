import logging
from collections import deque
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .laglib import MemoryManager
from .Constants import (
    GameMode,
    chest_flags,
    game_mode,
    game_name,
    goal_space,
    name_space,
    opening_ending_flag,
    quest_flags,
    ram_names,
    rom_international_name,
    rom_version,
)
from .Goals import GoalData, get_goal_data
from .Locations import all_locations, locations_by_id

logger = logging.getLogger("Client")


class PhSt2Client(BizHawkClient):
    game = game_name
    system = "GEN"
    patch_suffix = ".apphst2"

    items_received: int
    items_queue: deque[int]
    goal: GoalData
    mesetas_pending: int
    prev_flags = None
    prev_chest = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_received = 0
        self.items_queue = deque()
        self.mesetas_pending = 0
        self.showing_inventory_full_message = False
        self.mem = MemoryManager(ram_names)
        self.mem.spans += [
            chest_flags,
            game_mode,
            opening_ending_flag,
            quest_flags,
        ]

    async def validate_rom(self, ctx: "BizHawkClientContext"):
        goal_num = -1
        try:
            [name_raw, version_raw, goal_raw] = await self.mem.request(
                ctx,
                [
                    rom_international_name,
                    rom_version,
                    goal_space,
                ],
            )
            name = rom_international_name.parse(name_raw)
            version = rom_version.parse(version_raw)
            goal_num = goal_space.parse(goal_raw)
        except (
            UnicodeDecodeError,
            bizhawk.RequestFailedError,
            bizhawk.NotConnectedError,
        ):
            return False

        if name != "PHANTASY STAR 2                 ":
            logger.error("Selected ROM is not Phantasy Star II")
            return False
        if version != "02":
            logger.error("Selected ROM is not REV02")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # other, own, starting
        ctx.want_slot_data = True
        self.items_queue.clear()
        self.goal = get_goal_data(goal_num)
        return True

    async def set_auth(self, ctx: "BizHawkClientContext"):
        [auth_raw] = await self.mem.request(ctx, [name_space])
        ctx.auth = name_space.parse(auth_raw)

    async def game_watcher(self, ctx: "BizHawkClientContext"):
        if ctx.server is None:
            return
        if ctx.slot is None:
            return

        try:
            await self.mem.update(ctx)
            await self.location_check(ctx)
            # await self.received_items_check(ctx)
            # await self.process_item_queue(ctx)
            # await self.process_pending_gold(ctx)
            await self.met_goal_check(ctx)
        except bizhawk.RequestFailedError:
            pass

    def not_playing(self):
        oe = opening_ending_flag.get(self.mem)
        mode = game_mode.get(self.mem)
        return not (
            oe == 0
            and GameMode(mode)
            in [GameMode.MAP, GameMode.SCENE, GameMode.BATTLE, GameMode.ENDING]
        )

    async def location_check(self, ctx: "BizHawkClientContext"):
        if self.not_playing():
            return

        locations_checked = set[int]()
        for loc_id in ctx.missing_locations:
            data = locations_by_id[loc_id]

            passes_all = True
            for check in data.checks:
                if not check.test(self.mem):
                    passes_all = False
                    break

            if passes_all:
                locations_checked.add(loc_id)

        found_locations = await ctx.check_locations(locations_checked)
        for loc_id in found_locations:
            ctx.locations_checked.add(loc_id)
            name = ctx.location_names.lookup_in_game(loc_id)
            logger.debug(
                f"New Check: {name} ({len(ctx.locations_checked)})/{len(ctx.missing_locations) + len(ctx.checked_locations)}"
            )

    async def met_goal_check(self, ctx: "BizHawkClientContext"):
        if ctx.finished_game:
            return

        goal_locations = [
            l for l in all_locations if l.fixed_item in self.goal.completion_item_names
        ]
        for location in goal_locations:
            if not location.id in ctx.checked_locations:
                return False
        await ctx.send_msgs(
            [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
        )
        ctx.finished_game = True
