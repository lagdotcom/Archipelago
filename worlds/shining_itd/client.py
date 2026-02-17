import logging
from collections import deque
from typing import TYPE_CHECKING, NamedTuple

import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .constants import (
    chest_flags_span,
    game_name,
    goal_space,
    gold_span,
    hero_max_hp_span,
    inventory_span,
    name_space,
    quest_flags_span,
    ram_names,
    received_item_storage,
    rom_international_name,
    rom_version,
)
from .goals import get_goal_data
from .items import items_by_id
from .laglib import IntSpan, MemoryManager
from .laglib import genesis_ram as ram
from .locations import all_locations, locations_by_id

logger = logging.getLogger("Client")


class InventorySlot(NamedTuple):
    char_name: str
    address: int


class Inventory(NamedTuple):
    char_name: str
    start_address: int
    size: int

    def slot(self, index: int):
        return InventorySlot(self.char_name, self.start_address + index)


inventories = [Inventory("Hero", 0x16EA, 16), Inventory("Milo", 0x16FA, 16), Inventory("Pyra", 0x170A, 16)]


class SITDClient(BizHawkClient):
    game = game_name
    system = "GEN"
    patch_suffix = ".apsitd"

    items_queue: deque[int]
    gold_pending: int
    prev_flags = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_queue = deque()
        self.gold_pending = 0
        self.showing_inventory_full_message = False
        self.mem = MemoryManager(ram_names)
        self.mem.spans += [
            quest_flags_span,
            chest_flags_span,
            inventory_span,
            gold_span,
            hero_max_hp_span,
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

        if name != "SHINING IN          THE DARKNESS":
            logger.error("Selected ROM is not Shining in the Darkness")
            return False
        if version != "00":
            logger.error("Selected ROM is not REV00")
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
        return hero_max_hp_span.get(self.mem) > 0

    async def location_check(self, ctx: "BizHawkClientContext"):
        flags_data = self.mem.get_bytes(quest_flags_span)

        locations_checked = set[int]()
        for loc_id in ctx.missing_locations:
            data = locations_by_id[loc_id]
            byte = flags_data[data.check_address - quest_flags_span.address]
            if byte & data.check_mask == data.check_mask:
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
                else:
                    self.items_queue.append(nwi.item)
                logger.debug(f"... got {item.name}")
            await self.mem.write_span(ctx, received_item_storage, items_received)

    def get_empty_inventory_slot(self):
        # TODO don't try to give items to party members we don't have yet
        for inv in inventories:
            for index in range(inv.size):
                slot = inv.slot(index)
                contents = self.mem.get(ram, slot.address)
                if contents == 0xFF:
                    return slot
        return None

    async def show_inventory_full_message(self, ctx: "BizHawkClientContext"):
        if not self.showing_inventory_full_message:
            self.showing_inventory_full_message = True
            await bizhawk.display_message(ctx.bizhawk_ctx, "Inventory is full!")

    async def reset_inventory_full_message(self, ctx: "BizHawkClientContext"):
        self.showing_inventory_full_message = False

    async def process_item_queue(self, ctx: "BizHawkClientContext"):
        if not self.is_playing():
            return

        while len(self.items_queue):
            item_id = self.items_queue.popleft()
            item = items_by_id[item_id]
            if item.code is None:
                logger.warning(f"Don't know how to reward non-code item: {item.name}")
            else:
                slot = self.get_empty_inventory_slot()
                if slot is None:
                    await self.show_inventory_full_message(ctx)
                    return
                await self.reset_inventory_full_message(ctx)

                if await self.mem.write_span(ctx, IntSpan(ram, slot.address, 1), item.code):
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"{slot.char_name} received item: {item.name}")
                    logger.debug(f"Received item {item.name}")
                else:
                    self.items_queue.append(item_id)
                    return  # leave it until next tick

    async def process_pending_gold(self, ctx: "BizHawkClientContext"):
        amount = self.gold_pending
        if not amount or not self.is_playing():
            return

        old_gold = gold_span.get(self.mem)
        new_gold = min(9_999_999, old_gold + amount)

        logger.debug(f"Trying to send {amount} gold ({old_gold} -> {new_gold})")
        if await self.mem.write_span(ctx, gold_span, new_gold):
            self.gold_pending = 0
            await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {amount} gold")

    async def met_goal_check(self, ctx: "BizHawkClientContext"):
        if ctx.finished_game:
            return

        goal_locations = [loc for loc in all_locations if loc.fixed_item in self.goal.completion_item_names]
        for location in goal_locations:
            if location.id not in ctx.checked_locations:
                return
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True
