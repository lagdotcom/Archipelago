import hashlib
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, ClassVar

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .constants import game_name, goal_space, name_space, patch_file_ending
from .items import items_by_id

if TYPE_CHECKING:
    from . import PRWorld
    from .locations import LocationData


U_HASH = ""


class PRProcedurePatch(APProcedurePatch, APTokenMixin):
    game = game_name
    hash = U_HASH
    patch_file_ending = patch_file_ending
    result_file_ending = ".nes"

    procedure: ClassVar[list[tuple[str, list[Any]]]] = [
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls):
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path()
        base_rom_bytes = bytes(open(file_name, "rb").read())

        base_md5 = hashlib.md5()
        base_md5.update(base_rom_bytes)
        if U_HASH != base_md5.hexdigest():
            raise Exception(
                "Supplied Base Rom does not match known MD5 for US+Europe REV02 release. "
                "Get the correct game and version, then dump it"
            )
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes  # type: ignore
    return base_rom_bytes


def get_base_rom_path():
    from . import PRWorld

    return PRWorld.settings.rom_file


def write_tokens(
    world: "PRWorld",
    patch: PRProcedurePatch,
    locations: Iterable["LocationData"],
):
    # write player name
    raw_name = patch.player_name.encode("utf-8") + b"\0"
    if len(raw_name) > name_space.size:
        raise Exception("Name too long!")
    patch.write_token(APTokenTypes.WRITE, name_space.address, raw_name)

    # write goal number
    patch.write_token(APTokenTypes.WRITE, goal_space.address, bytes([world.options.goal]))

    # patch locations/items
    valid_locations = {loc.name for loc in world.get_locations()}
    for location_data in locations:
        if location_data.name not in valid_locations:
            continue
        item = world.get_location(location_data.name).item
        if item is None:
            raise Exception(f"Location {location_data.name} has no item???")
        # don't bother replacing an item that is the same
        if item.game == game_name and location_data.vanilla_item == item.name:
            continue

        if location_data.rom_location:
            if item.code in items_by_id:
                native = items_by_id[item.code]
                if native.treasure_id is not None:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        location_data.rom_location.address,
                        location_data.rom_location.format(native.treasure_id),
                    )
                    continue

            # default to 0 (no treasure)
            patch.write_token(
                APTokenTypes.WRITE, location_data.rom_location.address, location_data.rom_location.format(0)
            )
            continue

        raise Exception(f"Do not know how to put {item.name} at {location_data.name}")

    patch.write_file("token_data.bin", patch.get_token_binary())
