import logging
from collections import deque
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .Constants import game_name, NAME_SPACE, NAME_SPACE_LEN, ROM_INTERNATIONAL_NAME, ROM_VERSION, GOAL_SPACE, CHEST_FLAG_START, CHEST_FLAG_LEN, QUEST_FLAG_START, QUEST_FLAG_LEN, GAME_MODE, OPENING_ENDING_FLAG
from .Goals import get_goal_data
from .Locations import all_locations, locations_by_id

logger = logging.getLogger('Client')


class PhSt2Client(BizHawkClient):
    game = game_name
    system = 'GEN'
    patch_suffix = '.apphst2'
    rom = 'MD CART'
    ram = '68K RAM'

    items_received: int
    items_queue: deque[int]
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
            await self.location_check(ctx)
            # await self.received_items_check(ctx)
            # await self.process_item_queue(ctx)
            # await self.process_pending_gold(ctx)
            await self.met_goal_check(ctx)
        except bizhawk.RequestFailedError:
            pass

    async def not_in_game(self, ctx: 'BizHawkClientContext'):
        [oe, mode] = await bizhawk.read(ctx.bizhawk_ctx, [
            (OPENING_ENDING_FLAG, 1, self.ram),
            (GAME_MODE, 1, self.ram),
        ])
        # MAP, SCENE, BATTLE
        return not (oe[0] == 0 and mode[0] in [12, 16, 20])

    async def location_check(self, ctx: 'BizHawkClientContext'):
        if await self.not_in_game(ctx):
            return

        [flags_data, chest_data] = await bizhawk.read(ctx.bizhawk_ctx, [
            (QUEST_FLAG_START, QUEST_FLAG_LEN, self.ram),
            (CHEST_FLAG_START, CHEST_FLAG_LEN, self.ram),
        ])

        if not flags_data or not chest_data:
            return

        self.debug_flag_changes(flags_data, chest_data)

        locations_checked = set[int]()
        for loc_id in ctx.missing_locations:
            data = locations_by_id[loc_id]
            checks = 0
            passes_all = True
            if data.chest_index is not None:
                checks += 1
                if chest_data[data.chest_index] != 1:
                    passes_all = False
            if data.ram_location is not None:
                checks += 1
                if flags_data[data.ram_location - QUEST_FLAG_START] != data.ram_check:
                    passes_all = False
            if data.extra_location is not None:
                checks += 1
                if flags_data[data.extra_location - QUEST_FLAG_START] != data.extra_check:
                    passes_all = False
            # remove this once everything has an actual client check
            if passes_all and checks > 0:
                locations_checked.add(loc_id)

        found_locations = await ctx.check_locations(locations_checked)
        for loc_id in found_locations:
            ctx.locations_checked.add(loc_id)
            name = ctx.location_names.lookup_in_game(loc_id)
            logger.debug(
                f'New Check: {name} ({len(ctx.locations_checked)})/{len(ctx.missing_locations) + len(ctx.checked_locations)}')

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

    def debug_flag_changes(self, flags_data: bytes, chest_data: bytes):
        if self.prev_flags:
            self._debug_flag_ch('Flags', QUEST_FLAG_START,
                                self.prev_flags, flags_data)
        if self.prev_chest:
            self._debug_flag_ch('Chest', CHEST_FLAG_START,
                                self.prev_chest, chest_data)
        self.prev_flags = flags_data
        self.prev_chest = chest_data

    def _debug_flag_ch(self, name: str, offset: int, old: bytes, new: bytes):
        for i in range(len(old)):
            ol = old[i]
            nu = new[i]
            if ol != nu:
                logger.debug('%s %04x: %02x -> %02x (%02x flipped)' %
                             (name, offset+i, ol, nu, ol ^ nu))
