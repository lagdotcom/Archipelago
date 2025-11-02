import hashlib
from typing import Iterable, TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Constants import NAME_SPACE, NAME_SPACE_LEN
from .Items import items_by_id

if TYPE_CHECKING:
    from . import SITDWorld
    from .Locations import LD

SITD_UE_HASH = '522b689a1b2f0ea8578fa9d888554b82'


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

    # TODO this will replace any non-SITD item with 50g instead of 'nothing'
    #      need to patch ROM to show 'found APItem' or whatever?
    for location_data in chest_locations:
        item = world.get_location(location_data.name).item
        item_hex = 0x80  # default to 50g chest - least impactful
        if not item is None:
            if not item.code is None:
                if item.code in items_by_id:
                    item_data = items_by_id[item.code]
                    if not item_data.code is None:
                        item_hex = item_data.code
        patch.write_token(APTokenTypes.WRITE,
                          location_data.rom_location, bytes([item_hex]))

    patch.write_file('token_data.bin', patch.get_token_binary())
