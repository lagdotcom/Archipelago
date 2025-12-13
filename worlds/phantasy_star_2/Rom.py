import hashlib
from typing import Iterable, TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Characters import character_names
from .Constants import (
    CHECKSUM_FAILED_JUMP,
    ENCOUNTER_RATE_SHIFT,
    game_name,
    goal_space,
    JUMP_APPLY_MESETA_MULTIPLIER,
    JUMP_APPLY_XP_MULTIPLIER,
    JUMP_FIX_RECORDER_LOOP_CT_OUTSIDE,
    JUMP_FIX_RECORDER_LOOP_GOVERNOR,
    JUMP_FOLLOWING_CHARACTER_SPEED,
    JUMP_GAIRA_CONTROL_PANEL,
    JUMP_GET_CARD,
    JUMP_INTERACT_ADD_ITEM,
    JUMP_JET_SCOOTER_GUY,
    JUMP_SET_LEAF_FLAG,
    JUMP_SET_MUSIK_FLAG,
    JUMP_SET_RECORDER_FLAG,
    MISC_MESSAGES,
    MOTAVIAN_INIT_DELETE_CHECK,
    MOVE_FRAME_COUNT,
    MOVE_NEGATIVE,
    MOVE_POSITIVE,
    name_space,
    PATCH_ADD_ITEM,
    PATCH_ADD_ITEM2_REARRANGE,
    PATCH_APPLY_MESETA_MULTIPLIER,
    PATCH_APPLY_XP_MULTIPLIER,
    PATCH_CARD_LOOKUP_TABLE,
    PATCH_FIX_RECORDER_LOOP_CT_OUTSIDE,
    PATCH_FIX_RECORDER_LOOP_GOVERNOR,
    PATCH_FOLLOWING_CHARACTER_SPEED,
    PATCH_GAIRA_CONTROL_PANEL,
    PATCH_GET_CARD,
    PATCH_JET_SCOOTER_GUY_TALK,
    PATCH_MULWW,
    PATCH_SET_LEAF_FLAG,
    PATCH_SET_MUSIK_FLAG,
    PATCH_SET_RECORDER_FLAG,
    STARTING_MESETA_AMOUNT,
    TECH_LEARN_TABLES,
)
from .Items import items_by_id
from .Options import (
    ENCOUNTER_DOUBLE,
    ENCOUNTER_EIGHTH,
    ENCOUNTER_HALF,
    ENCOUNTER_NORMAL,
    ENCOUNTER_QUARTER,
    SPEED_NORMAL,
    SPEED_QUADRUPLE,
)
from .Locations import LocationType
from .Messages import miscellaneous_messages, translate_block


if TYPE_CHECKING:
    from . import PhSt2World
    from .Locations import LocationData


REV02_UE_HASH = "0fa38b12cf0ab0163d865600ac731a9a"

AP_ITEM_CODE = 0xE0


encounter_rate_ops = {
    ENCOUNTER_DOUBLE: bytes([0xE4, 0x49]),  # lsr.w #2,D1w
    ENCOUNTER_HALF: bytes([0xE8, 0x49]),  # lsr.w #4,D1w
    ENCOUNTER_QUARTER: bytes([0xEA, 0x49]),  # lsr.w #5,D1w
    ENCOUNTER_EIGHTH: bytes([0xEC, 0x49]),  # lsr.w #6,D1w
}


class PhSt2ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = game_name
    hash = REV02_UE_HASH
    patch_file_ending = ".apphst2"
    result_file_ending = ".gen"

    procedure = [
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
        if REV02_UE_HASH != base_md5.hexdigest():
            raise Exception(
                "Supplied Base Rom does not match known MD5 for US+Europe REV02 release. "
                "Get the correct game and version, then dump it"
            )
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path():
    from . import PhSt2World

    return PhSt2World.settings.rom_file


def write_tokens(
    world: "PhSt2World",
    patch: PhSt2ProcedurePatch,
    locations: Iterable["LocationData"],
):
    # write player name
    raw_name = patch.player_name.encode("utf-8") + b"\0"
    if len(raw_name) > name_space.size:
        raise Exception("Name too long!")
    patch.write_token(APTokenTypes.WRITE, name_space.address, raw_name)

    # write goal number
    patch.write_token(
        APTokenTypes.WRITE, goal_space.address, bytes([world.options.goal])
    )

    # apply Recorder conversation loop fix
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_FIX_RECORDER_LOOP_CT_OUTSIDE,
        bytes(
            [
                # jmp PATCH_FixRecorderLoop_CTOutside
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0xAC,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_FIX_RECORDER_LOOP_CT_OUTSIDE,
        bytes(
            [
                # tst.w (cutsceneFlag).l
                0x4A,
                0x79,
                0xFF,
                0xFF,
                0xF7,
                0x50,
                # beq.b +6
                0x67,
                0x06,
                # jmp 0xc086.l
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xC0,
                0x86,
                # moveq #RECORDER,D2
                0x74,
                0x0A,
                # jsr FindInventoryItem.l
                0x4E,
                0xB9,
                0x00,
                0x00,
                0xD0,
                0x2E,
                # jmp 0xc078.l
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xC0,
                0x78,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_FIX_RECORDER_LOOP_GOVERNOR,
        bytes(
            [
                # jmp PATCH_FixRecorderLoop_Governor
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0xC8,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_FIX_RECORDER_LOOP_GOVERNOR,
        bytes(
            [
                # tst.w (cutsceneFlag).l
                0x4A,
                0x79,
                0xFF,
                0xFF,
                0xF7,
                0x50,
                # beq.b +6
                0x67,
                0x06,
                # jmp 0xc9d8.l
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xC9,
                0xD8,
                # moveq #RECORDER,D2
                0x74,
                0x0A,
                # jsr FindInventoryItem.l
                0x4E,
                0xB9,
                0x00,
                0x00,
                0xD0,
                0x2E,
                # jmp 0xc9c4.l
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xC9,
                0xC4,
            ]
        ),
    )

    # apply specific multipliers
    write_mulww = False
    if world.options.xp_multi.value > 1:
        write_mulww = True
        patch.write_token(
            APTokenTypes.WRITE,
            JUMP_APPLY_XP_MULTIPLIER,
            bytes(
                [
                    # jmp PATCH_ApplyXPMultiplier
                    0x4E,
                    0xF9,
                    0x00,
                    0x0B,
                    0xF7,
                    0x24,
                ]
            ),
        )
        patch.write_token(
            APTokenTypes.WRITE,
            PATCH_APPLY_XP_MULTIPLIER,
            bytes(
                [
                    # move.l (enemyTotalXP).l,D0
                    0x20,
                    0x39,
                    0xFF,
                    0xFF,
                    0xCB,
                    0x30,
                    # moveq #XP_MULTI,D1
                    0x72,
                    world.options.xp_multi.value,
                    # jsr mulww
                    0x4E,
                    0xBA,
                    0xFF,
                    0xCE,
                    # jmp JUMP_ApplyXPMultiplier+6
                    0x4E,
                    0xF9,
                    0x00,
                    0x00,
                    0xF2,
                    0xC4,
                ]
            ),
        )

    if world.options.meseta_multi.value > 1:
        write_mulww = True
        patch.write_token(
            APTokenTypes.WRITE,
            JUMP_APPLY_MESETA_MULTIPLIER,
            bytes(
                [
                    # jmp PATCH_ApplyMesetaMultiplier
                    0x4E,
                    0xF9,
                    0x00,
                    0x0B,
                    0xF7,
                    0x36,
                    # nop
                    0x4E,
                    0x71,
                ]
            ),
        )
        patch.write_token(
            APTokenTypes.WRITE,
            PATCH_APPLY_MESETA_MULTIPLIER,
            bytes(
                [
                    # movem.l { D1 },-(SP)
                    0x48,
                    0xE7,
                    0x40,
                    0x00,
                    # move.l (enemyTotalMeseta).l,D0
                    0x20,
                    0x39,
                    0xFF,
                    0xFF,
                    0xCB,
                    0x34,
                    # moveq #MESETA_MULTI,D1
                    0x72,
                    world.options.meseta_multi.value,
                    # jsr mulww
                    0x4E,
                    0xBA,
                    0xFF,
                    0xB8,
                    # add.l D0,(currentMoney).l
                    0xD1,
                    0xB9,
                    0xFF,
                    0xFF,
                    0xC6,
                    0x20,
                    # movem.l (SP)+{ D1 }
                    0x4C,
                    0xDF,
                    0x00,
                    0x02,
                    # jmp JUMP_ApplyMesetaMultiplier+8
                    0x4E,
                    0xF9,
                    0x00,
                    0x00,
                    0xF3,
                    0x16,
                ]
            ),
        )

    if write_mulww:
        patch.write_token(
            APTokenTypes.WRITE,
            PATCH_MULWW,
            bytes(
                [
                    # movem.l { D4 D3 D2 D1 },-(SP)
                    0x48,
                    0xE7,
                    0x78,
                    0x00,
                    # moveq #0,D2
                    0x74,
                    0x00,
                    # bra.b +0x14
                    0x60,
                    0x14,
                    # moveq #0,D3
                    0x76,
                    0x00,
                    # move.w D0w,D3w
                    0x36,
                    0x00,
                    # moveq #1,D4
                    0x78,
                    0x01,
                    # and.l D4,D3
                    0xC6,
                    0x84,
                    # beq.b +6
                    0x67,
                    0x06,
                    # moveq #0,D3
                    0x76,
                    0x00,
                    # move.w D1w,D3w
                    0x36,
                    0x01,
                    # add.l D3,D2
                    0xD4,
                    0x83,
                    # lsr.w #1,D0w
                    0xE2,
                    0x48,
                    # add.w D1w,D1w
                    0xD2,
                    0x41,
                    # tst.w D0w
                    0x4A,
                    0x40,
                    # bne.b -0x18
                    0x66,
                    0xE8,
                    # move.l D2,D0
                    0x20,
                    0x02,
                    # movem.l (SP)+,{ D1 D2 D3 D4 }
                    0x4C,
                    0xDF,
                    0x00,
                    0x1E,
                    # rts
                    0x4E,
                    0x75,
                ]
            ),
        )

    # patch checksum failed jump out
    patch.write_token(
        APTokenTypes.WRITE,
        CHECKSUM_FAILED_JUMP,
        bytes(
            [
                # nop
                0x4E,
                0x71,
                # nop
                0x4E,
                0x71,
            ]
        ),
    )

    # patch event flags in to events we care about
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_SET_MUSIK_FLAG,
        bytes(
            [
                # jmp PATCH_SetMusikFlag.l
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0x56,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_SET_MUSIK_FLAG,
        bytes(
            [
                # bset.b #0,(PATCH_learnedMusik).l
                0x08,
                0xF9,
                0x00,
                0x00,
                0xFF,
                0xFF,
                0xC7,
                0x51,
                # addq.w #2,(windowRoutine3).l
                0x54,
                0x79,
                0xFF,
                0xFF,
                0xDE,
                0x5A,
                # rts
                0x4E,
                0x75,
            ]
        ),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_SET_RECORDER_FLAG,
        bytes(
            [
                # jmp PATCH_SetRecorderFlag.l
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0x66,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_SET_RECORDER_FLAG,
        bytes(
            [
                # bset.b #0,(PATCH_giveRecorder).l
                0x08,
                0xF9,
                0x00,
                0x00,
                0xFF,
                0xFF,
                0xC7,
                0x50,
                # addq.w #2,(windowRoutine3).l
                0x54,
                0x79,
                0xFF,
                0xFF,
                0xDE,
                0x5A,
                # rts
                0x4E,
                0x75,
            ]
        ),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_SET_LEAF_FLAG,
        bytes(
            [
                # jmp PATCH_SetLeafFlag.l
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0x76,
                # nop
                0x4E,
                0x71,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_SET_LEAF_FLAG,
        bytes(
            [
                # bset.b #0,(PATCH_gaveLeaf).l
                0x08,
                0xF9,
                0x00,
                0x00,
                0xFF,
                0xFF,
                0xC7,
                0x52,
                # move.w #0xb06,(scriptQueue).l
                0x33,
                0xFC,
                0x0B,
                0x06,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # rts
                0x4E,
                0x75,
            ]
        ),
    )

    if world.options.encounter_rate.value != ENCOUNTER_NORMAL:
        patch.write_token(
            APTokenTypes.WRITE,
            ENCOUNTER_RATE_SHIFT,
            encounter_rate_ops[world.options.encounter_rate.value],
        )

    if world.options.movement_speed.value != SPEED_NORMAL:
        pos = world.options.movement_speed.value.to_bytes(2, "big")
        neg = (-world.options.movement_speed.value).to_bytes(2, "big", signed=True)
        for addr in MOVE_POSITIVE:
            patch.write_token(APTokenTypes.WRITE, addr, pos)
        for addr in MOVE_NEGATIVE:
            patch.write_token(APTokenTypes.WRITE, addr, neg)

        frames = (16 // world.options.movement_speed.value) - 1
        patch.write_token(
            APTokenTypes.WRITE, MOVE_FRAME_COUNT, frames.to_bytes(2, "big")
        )

        patch.write_token(
            APTokenTypes.WRITE,
            JUMP_FOLLOWING_CHARACTER_SPEED,
            bytes(
                [
                    # jmp PATCH_FollowingCharacterSpeed
                    0x4E,
                    0xF9,
                    0x00,
                    0x0B,
                    0xF7,
                    0x88,
                ]
            ),
        )

        lsr_byte = 0xE2
        if world.options.movement_speed.value == SPEED_QUADRUPLE:
            lsr_byte = 0xE4
        patch.write_token(
            APTokenTypes.WRITE,
            PATCH_FOLLOWING_CHARACTER_SPEED,
            bytes(
                [
                    # move.l (-0x3c,A0),(0x4,A0)
                    0x21,
                    0x68,
                    0xFF,
                    0xC4,
                    0x00,
                    0x04,
                    # lea (characterPosTable).l,A2
                    0x45,
                    0xF9,
                    0xFF,
                    0xFF,
                    0xDD,
                    0x00,
                    # move.w (characterPosTableIndex).l,D0
                    0x30,
                    0x39,
                    0xFF,
                    0xFF,
                    0xF7,
                    0x40,
                    # moveq #0,D1
                    0x72,
                    0x00,
                    # move.w A0w,D1w
                    0x32,
                    0x08,
                    # subi.w #0xe400,D1w
                    0x04,
                    0x41,
                    0xE4,
                    0x00,
                    # lsr.w #SPEED_SHIFT,D1w
                    lsr_byte,
                    0x49,
                    # sub.w D1w,D0w
                    0x90,
                    0x41,
                    # jmp 0x3b3c
                    0x4E,
                    0xF9,
                    0x00,
                    0x00,
                    0x3B,
                    0x3C,
                ]
            ),
        )

    patch.write_token(
        APTokenTypes.WRITE,
        STARTING_MESETA_AMOUNT,
        world.options.starting_meseta.value.to_bytes(4, "big"),
    )

    if world.map_techs and world.battle_techs:
        offset = TECH_LEARN_TABLES
        for name in character_names:
            patch.write_token(APTokenTypes.WRITE, offset, bytes(world.map_techs[name]))
            patch.write_token(
                APTokenTypes.WRITE, offset + 16, bytes(world.battle_techs[name])
            )
            offset += 32

    # add our custom messages
    misc = miscellaneous_messages[:]
    misc.append("You got an APItem!<END>")
    misc.append("You got access to<NL>the Jet Scooter!<END>")
    misc.append("You got access to<NL>the Spaceship!<END>")
    patch.write_token(APTokenTypes.WRITE, MISC_MESSAGES, translate_block(misc))

    # patch Interact_AddItem to allow for new item codes
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_INTERACT_ADD_ITEM,
        bytes(
            [
                # jmp PATCH_AddItem
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF7,
                0xE4,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_ADD_ITEM2_REARRANGE,
        bytes(
            [
                # move.w (characterIndex).w,D1w
                0x32,
                0x38,
                0xDE,
                0x60,
                # bsr.w AddItemToInventory2
                0x61,
                0x00,
                0xC6,
                0x2C,
                # addq.b #1,(pFlag)
                0x52,
                0x10,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_ADD_ITEM,
        bytes(
            [
                # cmp.b #0xe0,D0b
                0xB0,
                0x3C,
                0x00,
                0xE0,
                # bne.b +10
                0x66,
                0x0A,
                # move.w #0x1914,(scriptQueue).l
                0x33,
                0xFC,
                0x19,
                0x14,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # bra.b +62
                0x60,
                0x3E,
                # cmp.b #0xe1,D0b
                0xB0,
                0x3C,
                0x00,
                0xE1,
                # bne.b +18
                0x66,
                0x12,
                # move.w #0x1915,(scriptQueue).l
                0x33,
                0xFC,
                0x19,
                0x15,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # move.b 0x2,(eventFlagJetScooter).l
                0x13,
                0xFC,
                0x00,
                0x02,
                0xFF,
                0xFF,
                0xC7,
                0x16,
                # bra.b +38
                0x60,
                0x26,
                # cmp.b #0xe2,D0b
                0xB0,
                0x3C,
                0x00,
                0xE2,
                # bne.b +18
                0x66,
                0x12,
                # move.w #0x1916,(scriptQueue).l
                0x33,
                0xFC,
                0x19,
                0x16,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # move.b 0x1,(eventFlagSpaceship).l
                0x13,
                0xFC,
                0x00,
                0x01,
                0xFF,
                0xFF,
                0xC7,
                0x3F,
                # bra.b +14
                0x60,
                0x0E,
                # move.w #0x1702,(scriptQueue).l
                0x33,
                0xFC,
                0x17,
                0x02,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # jmp Interact_AddItem+10
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xE8,
                0x54,
                # jmp Patch_AddItem2+8
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xE8,
                0xA4,
            ]
        ),
    )

    # patch jet scooter guy to use new flag and give different items
    patch.write_token(
        APTokenTypes.WRITE,
        MOTAVIAN_INIT_DELETE_CHECK,
        bytes(
            [
                # cmpi.b #0x1,(PATCH_eventFlagJetScooterGuy).w
                0x0C,
                0x38,
                0x00,
                0x01,
                0xC7,
                0x53,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_JET_SCOOTER_GUY,
        bytes(
            [
                # jmp PATCH_JetScooterGuyTalk
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF8,
                0x38,
                # could also put 14 nop here to reclaim space sometime
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_JET_SCOOTER_GUY_TALK,
        bytes(
            [
                # move.w #0x1,(interactionRoutine2).l
                0x33,
                0xFC,
                0x00,
                0x01,
                0xFF,
                0xFF,
                0xDE,
                0x72,
                # movea.l #PATCH_eventFlagJetScooterGuy,A0
                0x20,
                0x7C,
                0xFF,
                0xFF,
                0xC7,
                0x53,
                # tst.b (A0)
                0x4A,
                0x10,
                # beq.b +10
                0x67,
                0x0A,
                # move.w #0x1684,(scriptQueue).l
                0x33,
                0xFC,
                0x16,
                0x85,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # rts
                0x4E,
                0x75,
                # move.b #JET_SCOOTER_ITEM,D0b
                0x10,
                0x3C,
                0x00,
                0xE1,
                # cmp.b #JET_SCOOTER_ITEM,D0b
                0xB0,
                0x3C,
                0x00,
                0xE1,
                # bne.b +6
                0x67,
                0x06,
                # jmp Interact_AddItem
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xE8,
                0x4A,
                # move.w #0x1685,(scriptQueue).l
                0x33,
                0xFC,
                0x16,
                0x85,
                0xFF,
                0xFF,
                0xCD,
                0x00,
                # jmp Interact_NPC.jetScooterGuy+6
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xE6,
                0x96,
            ]
        ),
    )

    # patch Event_GairaControlPanel to use new flag and possibly give an item
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_GAIRA_CONTROL_PANEL,
        bytes(
            [
                # jmp PATCH_GairaControlPanel.l
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF8,
                0x92,
            ]
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_GAIRA_CONTROL_PANEL,
        bytes(
            [
                # tst.b (PATCH_eventFlagGairaControlPanel).l
                0x4A,
                0x39,
                0xFF,
                0xFF,
                0xC7,
                0x54,
                # bne.b +42
                0x66,
                0x2A,
                # move.b #SPACESHIP_ITEM,D0b
                0x10,
                0x3C,
                0x00,
                0xE2,
                # cmp.b #SPACESHIP_ITEM,D0b
                0xB0,
                0x3C,
                0x00,
                0xE2,
                # bne.b +6
                0x66,
                0x06,
                # move.b #1,(A0)
                0x10,
                0xBC,
                0x00,
                0x01,
                # bra.b +18
                0x60,
                0x12,
                # jsr Interact_AddItem.l
                0x4E,
                0xB9,
                0x00,
                0x00,
                0xE8,
                0x4A,
                # beq.b +8
                0x66,
                0x08,
                # move.b #1,(PATCH_eventFlagGairaControlPanel).l
                0x13,
                0xFC,
                0x00,
                0x01,
                0xFF,
                0xFF,
                0xC7,
                0x54,
                # rts
                0x4E,
                0x75,
                # move.b #1,(PATCH_eventFlagGairaControlPanel).l
                0x13,
                0xFC,
                0x00,
                0x01,
                0xFF,
                0xFF,
                0xC7,
                0x54,
                # move.w #0x10,(sceneIndex).l
                0x33,
                0xFC,
                0x00,
                0x10,
                0xFF,
                0xFF,
                0xF7,
                0x60,
                # jmp Event_GairaControlPanel+10
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xDF,
                0xF0,
            ]
        ),
    )

    # patch Event_GetCard to allow custom item IDs
    patch.write_token(
        APTokenTypes.WRITE,
        JUMP_GET_CARD,
        bytes(
            [
                # jmp PATCH_GetCard.l
                0x4E,
                0xF9,
                0x00,
                0x0B,
                0xF8,
                0x76,
                # nop
                0x4E,
                0x71,
            ]
        ),
    )
    patch.write_token(APTokenTypes.WRITE, PATCH_CARD_LOOKUP_TABLE, bytes([5, 6, 7, 8]))
    patch.write_token(
        APTokenTypes.WRITE,
        PATCH_GET_CARD,
        bytes(
            [
                # movem.l { A1 },-(SP)
                0x48,
                0xE7,
                0x00,
                0x40,
                # subi.w #0x13,D0w
                0x04,
                0x40,
                0x00,
                0x13,
                # movea.l #PATCH_CardLookupTable,A1
                0x22,
                0x7C,
                0x00,
                0x0B,
                0xF8,
                0x72,
                # adda.w D0w,A1
                0xD2,
                0xC0,
                # move.b (A1),D0b
                0x10,
                0x11,
                # movem.l (SP)+,{ A1 }
                0x4C,
                0xDF,
                0x02,
                0x00,
                # jmp Interact_AddItem.l
                0x4E,
                0xF9,
                0x00,
                0x00,
                0xE8,
                0x4A,
            ]
        ),
    )

    # patch items
    valid_locations = set([l.name for l in world.get_locations()])
    for location_data in locations:
        if not location_data.name in valid_locations:
            continue
        item = world.get_location(location_data.name).item
        if item is None:
            raise Exception(f"Location {location_data.name} has no item???")
        # don't bother replacing an item that is the same
        if item.game == game_name and location_data.fixed_item == item.name:
            continue
        item_hex = AP_ITEM_CODE
        item_data = None
        if item.code is not None:
            if item.code in items_by_id:
                item_data = items_by_id[item.code]
                if item_data.code is not None:
                    item_hex = item_data.code
        # print(item.name, 'in', location_data.name, ':', hex(item_hex))
        rom = location_data.rom_location
        if rom is not None:
            if location_data.type == LocationType.CHEST:
                if item_data:
                    patch.write_token(
                        APTokenTypes.WRITE, rom.address, item_data.get_chest_bytes()
                    )
                else:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        rom.address,
                        (item_hex | 0x8000).to_bytes(2, "big"),
                    )
                continue
            else:
                patch.write_token(APTokenTypes.WRITE, rom.address, rom.format(item_hex))
        else:
            raise Exception(
                f"Do not know how to put {item.name} at {location_data.name}"
            )

    patch.write_file("token_data.bin", patch.get_token_binary())
