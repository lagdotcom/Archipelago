import hashlib
from typing import Iterable, TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Constants import NAME_SPACE, NAME_SPACE_LEN, GOAL_SPACE
from .Items import items_by_id


if TYPE_CHECKING:
    from . import PhSt2World
    from .Locations import LocationData


REV02_UE_HASH = 'TODO'

AP_ITEM_CODE = 0  # TODO this makes it show up as Garbage


class PhSt2ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = 'Phantasy Star II'
    hash = REV02_UE_HASH
    patch_file_ending = '.apphst2'
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
        if REV02_UE_HASH != base_md5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US+Europe REV02 release. '
                            'Get the correct game and version, then dump it')
        setattr(get_base_rom_bytes, 'base_rom_bytes', base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path():
    from . import PhSt2World
    return PhSt2World.settings.rom_file


def write_tokens(world: 'PhSt2World', patch: PhSt2ProcedurePatch, locations: Iterable['LocationData']):
    # write player name
    raw_name = patch.player_name.encode('utf-8') + b'\0'
    if len(raw_name) > NAME_SPACE_LEN:
        raise Exception("Name too long!")
    patch.write_token(APTokenTypes.WRITE, NAME_SPACE, raw_name)

    # write goal number
    patch.write_token(APTokenTypes.WRITE, GOAL_SPACE,
                      bytes([world.options.goal]))

    # apply specific multipliers
    # patch.write_token(APTokenTypes.WRITE, APPLY_REWARD_MULTIPLIERS_GOLD, world.options.gold_multi.value.to_bytes(4, 'big'))
    # patch.write_token(APTokenTypes.WRITE, APPLY_REWARD_MULTIPLIERS_XP, world.options.xp_multi.value.to_bytes(4, 'big'))

    # patch items
    valid_locations = set([l.name for l in world.get_locations()])
    for location_data in locations:
        if not location_data.name in valid_locations:
            continue
        item = world.get_location(location_data.name).item
        item_hex = AP_ITEM_CODE
        if not item is None:
            # don't bother replacing an item that is the same
            if location_data.fixed_item == item.code:
                continue
            if not item.code is None:
                if item.code in items_by_id:
                    item_data = items_by_id[item.code]
                    if not item_data.code is None:
                        item_hex = item_data.code
            # print(item.name, 'in', location_data.name, ':', hex(item_hex))
            if location_data.rom_location == None:
                raise Exception(
                    f'Do not know how to put {item.name} at {location_data.name}')

            patch.write_token(APTokenTypes.WRITE,
                              location_data.rom_location, bytes([item_hex]))

    patch.write_file('token_data.bin', patch.get_token_binary())
