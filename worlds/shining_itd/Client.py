import logging
from collections import deque
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .Constants import ALL_FLAG_START, ALL_FLAG_LEN, NAME_SPACE, NAME_SPACE_LEN, ROM_INTERNATIONAL_NAME, ROM_VERSION, INVENTORY_START, INVENTORY_LENGTH, GOLD_START, GOLD_LENGTH, HERO_MAX_HP_START, HERO_MAX_HP_LENGTH
from .Locations import locations_by_id
from .Items import items_by_id

logger = logging.getLogger("Client")


class SITDClient(BizHawkClient):
    game = 'Shining in the Darkness'
    system = 'GEN'
    patch_suffix = '.apsitd'
    rom = 'MD CART'
    ram = '68K RAM'

    items_received: int
    items_queue: deque[int]
    gold_pending: int
    prev_flags = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_received = 0
        self.items_queue = deque()
        self.gold_pending = 0
        self.showing_inventory_full_message = False

    async def validate_rom(self, ctx: 'BizHawkClientContext'):
        try:
            blocks = await bizhawk.read(ctx.bizhawk_ctx, [
                (ROM_INTERNATIONAL_NAME, 32, self.rom),
                (ROM_VERSION, 2, self.rom),
            ])
            rom_name = blocks[0].decode('ascii')
            version = blocks[1].decode('ascii')
        except (UnicodeDecodeError, bizhawk.RequestFailedError, bizhawk.NotConnectedError):
            return False

        if rom_name != 'SHINING IN          THE DARKNESS':
            logger.error("Selected ROM is not Shining in the Darkness")
            return False
        if version != "00":
            logger.error("Selected ROM is not REV00")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # other, own, starting
        ctx.want_slot_data = True
        self.items_queue.clear()
        return True

    async def set_auth(self, ctx: 'BizHawkClientContext'):
        auth_raw = await self.read_rom(ctx, NAME_SPACE, NAME_SPACE_LEN)
        ctx.auth = auth_raw.split(b'\0')[0].decode('utf-8')

    async def game_watcher(self, ctx: 'BizHawkClientContext'):
        if ctx.server is None:
            return
        if ctx.slot is None:
            return

        try:
            await self.location_check(ctx)
            await self.received_items_check(ctx)
            await self.process_item_queue(ctx)
            await self.process_pending_gold(ctx)
        except bizhawk.RequestFailedError:
            pass

    async def location_check(self, ctx: 'BizHawkClientContext'):
        flags_data = await self.read_ram(ctx, ALL_FLAG_START, ALL_FLAG_LEN)
        if not flags_data:
            return

        self.debug_flag_changes(flags_data)

        locations_checked = set[int]()
        for loc_id in ctx.missing_locations:
            data = locations_by_id[loc_id]
            byte = flags_data[data.check_address - ALL_FLAG_START]
            if byte & data.check_mask == data.check_mask:
                locations_checked.add(loc_id)

        found_locations = await ctx.check_locations(locations_checked)
        for loc_id in found_locations:
            ctx.locations_checked.add(loc_id)
            name = ctx.location_names.lookup_in_game(loc_id)
            logger.info(
                f'New Check: {name} ({len(ctx.locations_checked)})/{len(ctx.missing_locations) + len(ctx.checked_locations)}')

    async def received_items_check(self, ctx: 'BizHawkClientContext'):
        new_count = len(ctx.items_received) - self.items_received
        if new_count > 0:
            logger.info(f'Received {new_count} new items')
            for nwi in ctx.items_received[-new_count:]:
                item = items_by_id[nwi.item]
                if item.gold_pieces > 0:
                    self.gold_pending += item.gold_pieces
                else:
                    self.items_queue.append(nwi.item)
                logger.info(f'... got {item.name}')
            self.items_received = len(ctx.items_received)

    async def get_empty_inventory_slot(self, ctx: 'BizHawkClientContext'):
        inventory = await self.read_ram(ctx, INVENTORY_START, INVENTORY_LENGTH)
        for i in range(1, 48, 2):
            existing = inventory[i]
            if existing == 0xff:
                return INVENTORY_START + i, bytes([existing])
        return None, None

    async def show_inventory_full_message(self, ctx: 'BizHawkClientContext'):
        if not self.showing_inventory_full_message:
            self.showing_inventory_full_message = True
            await bizhawk.display_message(ctx.bizhawk_ctx, 'Inventory is full!')

    async def reset_inventory_full_message(self, ctx: 'BizHawkClientContext'):
        self.showing_inventory_full_message = False

    async def not_in_game(self, ctx: 'BizHawkClientContext'):
        hp = int.from_bytes(await self.read_ram(ctx, HERO_MAX_HP_START, HERO_MAX_HP_LENGTH), 'big')
        return hp == 0

    async def process_item_queue(self, ctx: 'BizHawkClientContext'):
        if await self.not_in_game(ctx):
            return

        while len(self.items_queue):
            address, expected = await self.get_empty_inventory_slot(ctx)
            if address is None or expected is None:
                await self.show_inventory_full_message(ctx)
                return
            await self.reset_inventory_full_message(ctx)

            item_id = self.items_queue.pop()
            item = items_by_id[item_id]
            if item.code is None:
                raise Exception(
                    f"Don't know how to reward non-code item: {item.name}")
            await bizhawk.guarded_write(ctx.bizhawk_ctx, [(address, bytes([item.code]), self.ram)], [(address, expected, self.ram)])
            logger.info(f'Sent item {item.name}')

    async def process_pending_gold(self, ctx: 'BizHawkClientContext'):
        amount = self.gold_pending
        if not amount:
            return
        if await self.not_in_game(ctx):
            return

        address = GOLD_START
        old_bytes = await self.read_ram(ctx, GOLD_START, GOLD_LENGTH)
        old_gold = int.from_bytes(old_bytes, 'big')
        new_gold = old_gold + amount
        new_bytes = new_gold.to_bytes(4, 'big')

        logger.info(f'Trying to send {amount} gold ({old_gold} -> {new_gold})')
        await bizhawk.guarded_write(ctx.bizhawk_ctx, [(address, new_bytes, self.ram)], [(address, old_bytes, self.ram)])
        self.gold_pending = 0
        await bizhawk.display_message(ctx.bizhawk_ctx, f'Received {amount} gold')

    async def read_ram(self, ctx: 'BizHawkClientContext', location: int, size: int):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.ram)]))[0]

    async def read_rom(self, ctx: 'BizHawkClientContext', location: int, size: int):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    def debug_flag_changes(self, flags_data: bytes):
        if self.prev_flags:
            for i in range(len(flags_data)):
                ol = self.prev_flags[i]
                nu = flags_data[i]
                if ol != nu:
                    logger.info('Flag %04x: %02x -> %02x (%02x flipped)' %
                                (ALL_FLAG_START+i, ol, nu, ol ^ nu))
        self.prev_flags = flags_data
