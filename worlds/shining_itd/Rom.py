import hashlib
from typing import Iterable, TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Constants import NAME_SPACE, NAME_SPACE_LEN
from .Items import items_by_id

if TYPE_CHECKING:
    from . import SITDWorld
    from .Locations import LD

SITD_UE_HASH = '522b689a1b2f0ea8578fa9d888554b82'

AP_ITEM_CODE = 0xe0

DO_OPEN_CHEST = 0x0826e
DO_OPEN_CHEST_JSR_DO_CHESTBEAK_ANIM = DO_OPEN_CHEST + 0x15a
MSG_B0A = 0x57356
CHECK_AP_ITEM = 0x5a0b8


class SITDProcedurePatch(APProcedurePatch, APTokenMixin):
    game = 'Shining in the Darkness'
    hash = SITD_UE_HASH
    patch_file_ending = '.apsitd'
    result_file_ending = '.gen'

    procedure = [
        ('apply_tokens', ['token_data.bin']),
    ]

    @classmethod
    def get_source_data(cls):
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = '') -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, 'base_rom_bytes', None)
    if not base_rom_bytes:
        file_name = get_base_rom_path()
        base_rom_bytes = bytes(open(file_name, 'rb').read())

        base_md5 = hashlib.md5()
        base_md5.update(base_rom_bytes)
        if SITD_UE_HASH != base_md5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US+Europe release. '
                            'Get the correct game and version, then dump it')
        setattr(get_base_rom_bytes, 'base_rom_bytes', base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path():
    from . import SITDWorld
    return SITDWorld.settings.rom_file


def write_tokens(world: 'SITDWorld', patch: SITDProcedurePatch, chest_locations: Iterable['LD']):
    raw_name = world.player_name.encode('utf-8') + b'\0'
    if len(raw_name) > NAME_SPACE_LEN:
        raise Exception("Name too long!")
    patch.write_token(APTokenTypes.WRITE, NAME_SPACE, raw_name)

    # patch DoOpenChest
    patch.write_token(APTokenTypes.WRITE, DO_OPEN_CHEST_JSR_DO_CHESTBEAK_ANIM, bytes([
        0x4e, 0xf9, 0x00, 0x05, 0xa0, 0xb8,     # jmp CheckAPItem
    ]))

    # write CheckAPItem
    patch.write_token(APTokenTypes.WRITE, CHECK_AP_ITEM, bytes([
        0x0c, 0x01, 0x00, 0xe0,                 # cmpi.b #e0,D1b
        0x67, 0x08,                             # beq.b +8
        0x4e, 0xb9, 0x00, 0x01, 0x00, 0x6c,     # jsr DoChestbeakAnim
        0x4e, 0x75,                             # rts
        0x30, 0x3c, 0x0b, 0x0a,                 # move.w #b0a,D0w
        0x4e, 0xf9, 0x00, 0x00, 0x83, 0x54,     # jmp 0x8354
    ]))

    for location_data in chest_locations:
        item = world.get_location(location_data.name).item
        item_hex = AP_ITEM_CODE
        if not item is None:
            if not item.code is None:
                if item.code in items_by_id:
                    item_data = items_by_id[item.code]
                    if not item_data.code is None:
                        item_hex = item_data.code
        patch.write_token(APTokenTypes.WRITE,
                          location_data.rom_location, bytes([item_hex]))

    # write "Found AP Item!" to message b0a address
    patch.write_token(APTokenTypes.WRITE, MSG_B0A, bytes(
        [0x09, 0x13, 0xd6, 0xdb, 0x7f, 0x59, 0x0d, 0x3b, 0x9f]))

    patch.write_file('token_data.bin', patch.get_token_binary())
