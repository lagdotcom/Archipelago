import logging
from collections import deque
from typing import TYPE_CHECKING, NamedTuple

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .laglib import MemoryManager, genesis_ram as RAM
from .Constants import (
    GameMode,
    chest_flags,
    current_money,
    game_mode,
    game_name,
    goal_space,
    name_space,
    opening_ending_flag,
    party_composition,
    party_inventories,
    party_size,
    quest_flags,
    ram_names,
    received_item_storage,
    rom_international_name,
    rom_version,
)
from .Goals import GoalData, get_goal_data
from .Items import items_by_id
from .Locations import all_locations, locations_by_id

logger = logging.getLogger("Client")


class InventorySlot(NamedTuple):
    count_address: int
    used: int

    def guard_list(self):
        return [
            (self.count_address, bytes([self.used]), RAM),
            (self.count_address + self.used + 1, bytes([0]), RAM),
        ]

    def write_list(self, item_id: int):
        return [
            (self.count_address, bytes([self.used + 1]), RAM),
            (self.count_address + self.used + 1, bytes([item_id]), RAM),
        ]


class PhSt2Client(BizHawkClient):
    game = game_name
    system = "GEN"
    patch_suffix = ".apphst2"

    items_queue: deque[int]
    goal: GoalData
    mesetas_pending: int
    prev_flags = None
    prev_chest = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_queue = deque()
        self.mesetas_pending = 0
        self.showing_inventory_full_message = False
        self.mem = MemoryManager(ram_names)
        self.mem.spans += (
            [
                chest_flags,
                current_money,
                game_mode,
                opening_ending_flag,
                party_size,
                quest_flags,
                received_item_storage,
            ]
            + party_composition
            + party_inventories
        )

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
            await self.received_items_check(ctx)
            await self.process_item_queue(ctx)
            await self.process_pending_mesetas(ctx)
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

    def get_empty_inventory_slot(self):
        count = party_size.get(self.mem) + 1
        for comp_span in party_composition[:count]:
            char_id = comp_span.get(self.mem)
            inv_span = party_inventories[char_id]
            inventory = self.mem.get_bytes(inv_span)
            used_slots = inventory[0]
            if used_slots < 16:
                return InventorySlot(inv_span.address, used_slots)

    async def show_inventory_full_message(self, ctx: "BizHawkClientContext"):
        if not self.showing_inventory_full_message:
            self.showing_inventory_full_message = True
            await bizhawk.display_message(ctx.bizhawk_ctx, "Inventory is full!")

    async def reset_inventory_full_message(self, ctx: "BizHawkClientContext"):
        self.showing_inventory_full_message = False

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        if self.not_playing():
            return

        items_sent = received_item_storage.get(self.mem)
        items_received = len(ctx.items_received)
        new_count = items_received - items_sent
        if new_count > 0:
            logger.debug(f"Received {new_count} new items")
            for nwi in ctx.items_received[-new_count:]:
                item = items_by_id[nwi.item]
                if item.meseta > 0:
                    self.mesetas_pending += item.meseta
                else:
                    self.items_queue.append(nwi.item)
                logger.debug(f"... got {item.name}")
            await self.mem.write_span(ctx, received_item_storage, items_received)

    async def process_item_queue(self, ctx: "BizHawkClientContext"):
        if self.not_playing():
            return

        while len(self.items_queue):
            slot = self.get_empty_inventory_slot()
            if slot is None:
                await self.show_inventory_full_message(ctx)
                return
            await self.reset_inventory_full_message(ctx)

            item_id = self.items_queue.popleft()
            item = items_by_id[item_id]
            if item.code is None:
                logger.warning(f"Don't know how to reward non-code item: {item.name}")
            else:
                if await self.mem.write_list(
                    ctx, slot.write_list(item.code), slot.guard_list()
                ):
                    logger.debug(f"Received item {item.name}")
                else:
                    self.items_queue.append(item_id)
                    return  # leave it until next tick

    async def process_pending_mesetas(self, ctx: "BizHawkClientContext"):
        amount = self.mesetas_pending
        if not amount or self.not_playing():
            return

        old_mesetas = current_money.get(self.mem)
        new_mesetas = min(999999, old_mesetas + amount)

        logger.debug(f"Trying to send {amount} MST ({old_mesetas} -> {new_mesetas})")
        if await self.mem.write_span(ctx, current_money, new_mesetas):
            self.mesetas_pending = 0
            await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {amount} MST")

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
