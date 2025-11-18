import hashlib
from typing import Iterable, TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Constants import NAME_SPACE, NAME_SPACE_LEN, GOAL_SPACE
from .Items import items_by_id

if TYPE_CHECKING:
    from . import SITDWorld
    from .Locations import LD

SITD_UE_HASH = '522b689a1b2f0ea8578fa9d888554b82'

AP_ITEM_CODE = 0xe0

DO_OPEN_CHEST = 0x0826e
DO_OPEN_CHEST_JSR_DO_CHESTBEAK_ANIM = DO_OPEN_CHEST + 0x15a

CASTLE_STATE00_02_03_06_08 = 0x220b2
CASTLE_STATE00_02_03_06_08_OVERWRITE = CASTLE_STATE00_02_03_06_08 + 6

FUN_00022354 = 0x22354
FUN_00022354_OVERWRITE = FUN_00022354 + 0x22

GIVE_ITEM_TO_ANY_PC = 0x22ed0

SCRIPT_TRY_GIVE_ITEM_22e56 = 0x22ef4
SCRIPT_TRY_GIVE_ITEM_22e56_OVERWRITE = SCRIPT_TRY_GIVE_ITEM_22e56 + 8

BATTLE_REWARDS = 0x24abe
BATTLE_REWARDS_MOVE_XP_ARG = BATTLE_REWARDS + 0x342

MSG_B0A = 0x57356

CHECK_AP_ITEM = 0x5a0b8
APPLY_REWARD_MULTIPLIERS = 0x5a0e0
APPLY_REWARD_MULTIPLIERS_GOLD = 0x5a0e0 + 0xc
APPLY_REWARD_MULTIPLIERS_XP = 0x5a0e0 + 0x24

GET_DWARFS_KEY_FROM_MINISTER = 0x5a140
MINISTER_ITEM = GET_DWARFS_KEY_FROM_MINISTER + 1

GIVE_ITEM_TO_ANY_PC_AP_ITEM = 0x5a180


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


def write_tokens(world: 'SITDWorld', patch: SITDProcedurePatch, locations: Iterable['LD']):
    # write player name
    raw_name = patch.player_name.encode('utf-8') + b'\0'
    if len(raw_name) > NAME_SPACE_LEN:
        raise Exception("Name too long!")
    patch.write_token(APTokenTypes.WRITE, NAME_SPACE, raw_name)

    # write goal number
    patch.write_token(APTokenTypes.WRITE, GOAL_SPACE,
                      bytes([world.options.goal]))

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

    # patch BattleRewards
    patch.write_token(APTokenTypes.WRITE, BATTLE_REWARDS_MOVE_XP_ARG, bytes([
        0x4e, 0xf9, 0x00, 0x05, 0xa0, 0xe0,     # jmp ApplyRewardMultipliers
        0x4e, 0x71,                             # nop
        0x4e, 0x71,                             # nop
    ]))

    # write ApplyRewardMultipliers
    patch.write_token(APTokenTypes.WRITE, APPLY_REWARD_MULTIPLIERS, bytes([
        # movem.l {D3 D2},-(SP)
        0x48, 0xe7, 0x30, 0x00,
        # move.l (BattleGold).l,D3
        0x26, 0x39, 0x00, 0xff, 0x3e, 0x00,
        # move.l #1,D2
        0x24, 0x3c, 0x00, 0x00, 0x00, 0x01,
        # jsr Mul64
        0x4e, 0xb9, 0x00, 0x00, 0x2a, 0xc6,
        # move.l D3,(BattleGold).l
        0x23, 0xc3, 0x00, 0xff, 0x3e, 0x00,
        # move.l (BattleXP).l,D3
        0x26, 0x39, 0x00, 0xff, 0x3e, 0x04,
        # move.l #1,D2
        0x24, 0x3c, 0x00, 0x00, 0x00, 0x01,
        # jsr Mul64
        0x4e, 0xb9, 0x00, 0x00, 0x2a, 0xc6,
        # move.l D3,(BattleXP).l
        0x23, 0xc3, 0x00, 0xff, 0x3e, 0x04,
        # movem.l (SP)+,{D2 D3}
        0x4c, 0xdf, 0x00, 0x0c,
        # move.l (BattleXP).l,(MESSAGE_ARG_NUMBER).l
        0x23, 0xf9, 0x00, 0xff, 0x3e, 0x04, 0x00, 0xff, 0x3a, 0x54,
        # jmp 0x24e0a
        0x4e, 0xf9, 0x00, 0x02, 0x4e, 0x0a,
    ]))

    # patch Castle_State00_2/3/6/8
    patch.write_token(APTokenTypes.WRITE, CASTLE_STATE00_02_03_06_08_OVERWRITE, bytes([
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # move.b (#0x16,A6),D5b
        0x1a, 0x2e, 0x00, 0x16,
        # andi.b #3,D5b
        0x02, 0x05, 0x00, 0x03,
        # cmpi.b #2,D5b
        0x0c, 0x05, 0x00, 0x02,
        # bne.b +0xc
        0x66, 0x0c,
        # lea (Script_WaitHereIsTheDwarfsKey,PC),A0
        0x41, 0xfa, 0xfa, 0x3b,
        # trap #3
        0x4e, 0x43,
        # jsr GetDwarfsKeyFromMinister_FIXED.l
        0x4e, 0xb9, 0x00, 0x05, 0xa1, 0x40,
    ]))

    # patch FUN_00022354
    patch.write_token(APTokenTypes.WRITE, FUN_00022354, bytes([
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # nop
        0x4e, 0x71,
        # move.b (#0x16,A6),D5b
        0x1a, 0x2e, 0x00, 0x16,
        # andi.b #3,D5b
        0x02, 0x05, 0x00, 0x03,
        # cmpi.b #2,D5b
        0x0c, 0x05, 0x00, 0x02,
    ]))
    patch.write_token(APTokenTypes.WRITE, FUN_00022354_OVERWRITE, bytes([
        # nop
        0x4e, 0x71,
        # jsr GetDwarfsKeyFromMinister_FIXED.l
        0x4e, 0xb9, 0x00, 0x05, 0xa1, 0x40,
    ]))

    # write GetDwarfsKeyFromMinister_FIXED
    patch.write_token(APTokenTypes.WRITE, GET_DWARFS_KEY_FROM_MINISTER, bytes([
        # moveq #0x5f,D1
        0x72, 0x5f,
        # jsr Script_TryGiveItem_22e5b.l
        0x4e, 0xb9, 0x00, 0x02, 0x2f, 0x12,
        # bcs.b +0x10
        0x65, 0x10,
        # movea.l #Script_WishYouSuccessInTheTrials,A0
        0x20, 0x7c, 0x00, 0x02, 0x1b, 0x24,
        # trap #3
        0x4e, 0x43,
        # ori.b #1,(0x16,A6)
        0x00, 0x2e, 0x00, 0x01, 0x00, 0x16,
        # bra.b +0x8
        0x60, 0x08,
        # movea.l #Script_InventoryFull_Minister,A0
        0x20, 0x7c, 0x00, 0x02, 0x1b, 0x1f,
        # trap #3
        0x4e, 0x43,
        # rts
        0x4e, 0x75,
    ]))

    # patch GiveItemToAnyPC
    patch.write_token(APTokenTypes.WRITE, GIVE_ITEM_TO_ANY_PC, bytes([
        # jmp GiveItemToAnyPC_APItem
        0x4e, 0xf9, 0x00, 0x05, 0xa1, 0x80,
    ]))

    # patch Script_TryGiveItem_22e56
    patch.write_token(APTokenTypes.WRITE, SCRIPT_TRY_GIVE_ITEM_22e56_OVERWRITE, bytes([
        # bra.b GiveItemToAnyPC
        0x60, 0xd2,
    ]))

    # write GiveItemToAnyPC_APItem
    patch.write_token(APTokenTypes.WRITE, GIVE_ITEM_TO_ANY_PC_AP_ITEM, bytes([
        # cmpi.b #0x80,D1b
        0x0c, 0x01, 0x00, 0xe0,
        # beq.b +0x2a
        0x67, 0x2a,
        # clr.w D0w
        0x42, 0x40,
        # bsr.l CheckHasPartyMember
        0x61, 0xff, 0xff, 0xfc, 0x8c, 0x10,
        # bcs.b +0x0e
        0x65, 0x0e,
        # move.l D0,-(SP)
        0x2f, 0x00,
        # trap #1 (GIVE_ITEM_TO_PC_2e)
        0x4e, 0x41, 0x00, 0xb8,
        # tst.w D0w
        0x4a, 0x40,
        # movem.l (SP)+,{D0}
        0x4c, 0xdf, 0x00, 0x01,
        # beq.b +0x0c
        0x67, 0x0c,
        # addq.w #1,D0w
        0x52, 0x40,
        # cmpi.w #3,D0w
        0x0c, 0x40, 0x00, 0x03,
        # bcs.b -0x1e
        0x65, 0xe2,
        # ori #1,CCR
        0x00, 0x3c, 0x00, 0x01,
        # jmp 0x22efe
        0x4e, 0xf9, 0x00, 0x02, 0x2e, 0xfe,
        # move.w #0xb0a,D0w
        0x30, 0x3c, 0x0b, 0x0a,
        # jsr ShowDialog.l
        0x4e, 0xb9, 0x00, 0x01, 0x80, 0x18,
        # clr.w D0w
        0x42, 0x40,
        # tst.w D0w
        0x4a, 0x40,
        # rts
        0x4e, 0x75,
    ]))

    # apply specific multipliers
    patch.write_token(
        APTokenTypes.WRITE, APPLY_REWARD_MULTIPLIERS_GOLD, world.options.gold_multi.value.to_bytes(4, 'big'))
    patch.write_token(APTokenTypes.WRITE,
                      APPLY_REWARD_MULTIPLIERS_XP, world.options.xp_multi.value.to_bytes(4, 'big'))

    # patch items
    valid_locations = set([l.name for l in world.get_locations()])
    for location_data in locations:
        if not location_data.name in valid_locations:
            continue
        item = world.get_location(location_data.name).item
        item_hex = AP_ITEM_CODE
        if not item is None:
            # don't bother replacing an item that is the same
            if location_data.fixed_item == item.name:
                continue
            if not item.code is None:
                if item.code in items_by_id:
                    item_data = items_by_id[item.code]
                    if not item_data.code is None:
                        item_hex = item_data.code
            # print(item.name, 'in', location_data.name, ':', hex(item_hex))
            for replacement in location_data.rom_locations:
                patch.write_token(APTokenTypes.WRITE,
                                  replacement.address, replacement.format(item_hex))

    # write "Found AP Item!" to message b0a address
    patch.write_token(APTokenTypes.WRITE, MSG_B0A, bytes(
        [0x09, 0x13, 0xd6, 0xdb, 0x7f, 0x59, 0x0d, 0x3b, 0x9f]))

    patch.write_file('token_data.bin', patch.get_token_binary())
