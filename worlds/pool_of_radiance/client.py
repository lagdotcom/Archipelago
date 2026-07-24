import logging
from collections import deque
from typing import TYPE_CHECKING, NamedTuple

import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .constants import (
    current_money,
    game_mode,
    game_name,
    goal_space,
    name_space,
    patch_file_ending,
    progress_flags,
    ram_names,
    received_item_storage,
    rom_name,
)
from .enums import GameMode
from .goals import GoalData, get_goal_data
from .items import items_by_id
from .laglib import IntSpan, MemoryManager
from .laglib import nes_ram as ram
from .locations import all_locations, locations_by_id

logger = logging.getLogger("Client")


class InventorySlot(NamedTuple):
    char_name: str
    address: int


class PendingItem(NamedTuple):
    name: str
    code: int


class PRClient(BizHawkClient):
    game = game_name
    system = "NES"
    patch_suffix = patch_file_ending

    items_queue: deque[PendingItem]
    goal: GoalData
    gold_pending: int
    prev_flags = None
    prev_chest = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_queue = deque()
        self.gold_pending = 0
        self.showing_inventory_full_message = False
        self.mem = MemoryManager(ram_names)
        self.mem.spans += [
            game_mode,
            progress_flags,
        ]
        # self.mem.translate(0xF600, GameMode)
        # self.mem.translate(0xC641, MapID)
        # self.mem.translate(0xCD00, ScriptID)
        # self.mem.translate(0xDE55, WinID)
        # self.mem.translate(0xF753, SceneID)

    async def validate_rom(self, ctx: "BizHawkClientContext"):
        goal_num = -1
        try:
            [name_raw, goal_raw] = await self.mem.request(
                ctx,
                [
                    rom_name,
                    goal_space,
                ],
            )
            name = rom_name.parse(name_raw)
            goal_num = goal_space.parse(goal_raw)
        except (
            UnicodeDecodeError,
            bizhawk.RequestFailedError,
            bizhawk.NotConnectedError,
        ):
            return False

        if name != "Pool of Radiance":
            logger.error("Selected ROM is not Pool of Radiance")
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
            await self.received_items_check(ctx)
            await self.process_item_queue(ctx)
            await self.process_pending_gold(ctx)
            await self.met_goal_check(ctx)
        except bizhawk.RequestFailedError:
            pass

    def is_playing(self):
        mode = game_mode.get(self.mem)
        return GameMode(mode) in {
            GameMode.Explore,
            GameMode.Combat,
            GameMode.BattleBegins,
            GameMode.Spoils,
        }

    def can_receive_item(self):
        mode = game_mode.get(self.mem)
        return mode == GameMode.Explore

    async def location_check(self, ctx: "BizHawkClientContext"):
        if not self.is_playing():
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
                "New Check: %s (%d)/%d",
                name,
                len(ctx.locations_checked),
                len(ctx.missing_locations) + len(ctx.checked_locations),
            )

    def get_empty_inventory_slot(self) -> InventorySlot | None:
        # TODO find inventory slot
        return None

    async def show_inventory_full_message(self, ctx: "BizHawkClientContext"):
        if not self.showing_inventory_full_message:
            self.showing_inventory_full_message = True
            await bizhawk.display_message(ctx.bizhawk_ctx, "Inventory is full!")

    def reset_inventory_full_message(self):
        self.showing_inventory_full_message = False

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        if not self.is_playing():
            return

        items_sent = received_item_storage.get(self.mem)
        items_received = len(ctx.items_received)
        new_count = items_received - items_sent
        if new_count > 0:
            logger.debug(f"Received {new_count} new items")
            for nwi in ctx.items_received[-new_count:]:
                item = items_by_id[nwi.item]
                if item.gold_pieces > 0:
                    self.gold_pending += item.gold_pieces
                elif item.code is not None:
                    self.items_queue.append(PendingItem(item.name, item.code))
                else:
                    logger.warning("received non-code item: %s", item.name)
                logger.debug(f"... got {item.name}")
            await self.mem.write_span(ctx, received_item_storage, items_received)

    async def process_item_queue(self, ctx: "BizHawkClientContext"):
        if not self.can_receive_item():
            return

        slot = self.get_empty_inventory_slot()
        while len(self.items_queue) and slot is not None:
            item = self.items_queue.popleft()
            if await self.mem.write_span(ctx, IntSpan(ram, slot.address, 1), item.code):
                await bizhawk.display_message(ctx.bizhawk_ctx, f"{slot.char_name} received item: {item.name}")
                logger.debug(f"Received item {item.name}")
                slot = self.get_empty_inventory_slot()
            else:
                self.items_queue.append(item)
                return  # leave it until next tick

        if len(self.items_queue):
            await self.show_inventory_full_message(ctx)
        else:
            self.reset_inventory_full_message()

    async def process_pending_gold(self, ctx: "BizHawkClientContext"):
        amount = self.gold_pending
        if not amount or not self.can_receive_item():
            return

        old_gold = current_money.get(self.mem)
        new_gold = min(999999, old_gold + amount)

        logger.debug("Trying to send %dgp (%d -> %d)", amount, old_gold, new_gold)
        if await self.mem.write_span(ctx, current_money, new_gold):
            self.gold_pending = 0
            await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {amount}gp")

    async def met_goal_check(self, ctx: "BizHawkClientContext"):
        if ctx.finished_game:
            return

        goal_locations = [loc for loc in all_locations if loc.fixed_item in self.goal.completion_item_names]
        for location in goal_locations:
            if location.id not in ctx.checked_locations:
                return
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True
