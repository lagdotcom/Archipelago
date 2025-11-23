import logging
from collections import deque
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .Constants import NAME_SPACE, NAME_SPACE_LEN, ROM_INTERNATIONAL_NAME, ROM_VERSION, GOAL_SPACE
from .Goals import get_goal_data
from .Locations import all_locations

logger = logging.getLogger('Client')


class PhSt2Client(BizHawkClient):
    game = 'Phantasy Star II'
    system = 'GEN'
    patch_suffix = '.apphst2'
    rom = 'MD CART'
    ram = '68K RAM'

    items_received: int
    items_queue: deque[int]
    mesetas_pending: int
    prev_flags = None
    showing_inventory_full_message: bool

    def __init__(self):
        super().__init__()
        self.items_received = 0
        self.items_queue = deque()
        self.mesetas_pending = 0
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

        if rom_name != 'PHANTASY STAR 2                 ':
            logger.error('Selected ROM is not Phantasy Star II')
            return False
        if version != '02':
            logger.error('Selected ROM is not REV02')
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # other, own, starting
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
            # await self.location_check(ctx)
            # await self.received_items_check(ctx)
            # await self.process_item_queue(ctx)
            # await self.process_pending_gold(ctx)
            await self.met_goal_check(ctx)
        except bizhawk.RequestFailedError:
            pass

    async def met_goal_check(self, ctx: 'BizHawkClientContext'):
        if ctx.finished_game:
            return
        goal_id = (await self.read_rom(ctx, GOAL_SPACE, 1))[0]
        goal = get_goal_data(goal_id)
        goal_locations = [
            l for l in all_locations if l.fixed_item in goal.completion_item_names]
        for location in goal_locations:
            if not location.id in ctx.checked_locations:
                return False
        await ctx.send_msgs([{'cmd': 'StatusUpdate', 'status': ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True

    async def read_ram(self, ctx: 'BizHawkClientContext', location: int, size: int):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.ram)]))[0]

    async def read_rom(self, ctx: 'BizHawkClientContext', location: int, size: int):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]
