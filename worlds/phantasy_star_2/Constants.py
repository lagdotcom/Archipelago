from .laglib import IntSpan, StrSpan, genesis_rom as ROM, genesis_ram as RAM

game_name = "Phantasy Star II"

# RAM addresses

ram_names = {
    0xC027: "Rolf.itemCount",
    0xC028: "Rolf.item[0]",
    0xC029: "Rolf.item[1]",
    0xC02A: "Rolf.item[2]",
    0xC02B: "Rolf.item[3]",
    0xC02C: "Rolf.item[4]",
    0xC02D: "Rolf.item[5]",
    0xC02E: "Rolf.item[6]",
    0xC02F: "Rolf.item[7]",
    0xC030: "Rolf.item[8]",
    0xC031: "Rolf.item[9]",
    0xC032: "Rolf.item[10]",
    0xC033: "Rolf.item[11]",
    0xC034: "Rolf.item[12]",
    0xC035: "Rolf.item[13]",
    0xC036: "Rolf.item[14]",
    0xC037: "Rolf.item[15]",
    0xC601: "partyNum",
    0xC605: "partyJoined",
    0xC607: "partyJoinNext",
    0xC609: "partyChar1",
    0xC60B: "partyChar2",
    0xC60D: "partyChar3",
    0xC60F: "partyChar4",
    0xC620: "meseta.1",
    0xC621: "meseta.2",
    0xC622: "meseta.3",
    0xC623: "meseta.4",
    0xC641: "mapIndex",
    0xC704: "Paseo",
    0xC705: "Arima",
    0xC706: "Oputa",
    0xC707: "Zema",
    0xC708: "Kueri",
    0xC709: "Piata",
    0xC710: "motaviaScene",
    0xC712: "controlTower",
    0xC715: "darumTeim",
    0xC716: "jetScooter",
    0xC717: "musikDoor_c717",
    0xC720: "marueraTree",
    0xC721: "shureCorpse",
    0xC722: "recorder",
    0xC723: "greenCard",
    0xC724: "blueCard",
    0xC725: "yellowCard",
    0xC726: "redCard",
    0xC727: "teim",
    0xC728: "nidoEntrance",
    0xC729: "bioSystemsLabEntrance",
    0xC72A: "bioSystemsLabPitDoor",
    0xC72B: "keyTubeDoor",
    0xC72C: "greenDamEntrance",
    0xC72D: "greenDamOpen",
    0xC72E: "blueDamEntrance",
    0xC72F: "blueDamOpen",
    0xC730: "yellowDamEntrance",
    0xC731: "yellowDamOpen",
    0xC732: "redDamEntrance",
    0xC733: "redDamOpen",
    0xC734: "musikDoor",
    0xC735: "neifirst",
    0xC736: "neiDead",
    0xC737: "climatrol",
    0xC73E: "gairaAlarm",
    0xC73F: "spaceship",
    0xC742: "esperMansion",
    0xC743: "lutz",
    0xC744: "neiWeapons",
    0xC745: "darkForce",
    0xC747: "motherBrain",
    0xC750: "gaveRecorder",
    0xC751: "learnedMusik",
    0xC752: "gaveLeaf",
    0xC781: "Skure15000Meseta",
    0xC782: "SkureMogicCap",
    0xC783: "Skure18000Meseta",
    0xC784: "SkureMagicCap",
    0xC785: "Skure7800Meseta",
    0xC786: "SkureLaconChest",
    0xC787: "Skure5600Meseta",
    0xC788: "SkureGardaBoots",
    0xC789: "Skure8600",
    0xC78A: "SkureMagicCap2",
    0xC78B: "Skure12000",
    0xC78C: "Skure6400",
    0xC78D: "Unknown200Meseta",
    0xC78E: "Prism",
    0xC78F: "NeiSword",
    0xC790: "ShureMonomate",
    0xC791: "Shure150Meseta",
    0xC792: "ShureDynamite",
    0xC793: "ShureDynamite2",
    0xC794: "Shure40Meseta",
    0xC795: "ShureDimate",
    0xC796: "ShureHeadgear",
    0xC797: "Shure200Meseta",
    0xC798: "ShureSilRibbon",
    0xC799: "Nido20Meseta",
    0xC79A: "Nido100Meseta",
    0xC79B: "NidoDimate",
    0xC79C: "NidoTrimate",
    0xC79D: "Nido60Meseta",
    0xC79E: "RoronGarbage",
    0xC79F: "RoronGarbage2",
    0xC7A0: "RoronCeramBar",
    0xC7A1: "RoronGarbage3",
    0xC7A2: "RoronCannon",
    0xC7A3: "RoronGarbage4",
    0xC7A4: "YellowDamEscapipe",
    0xC7A5: "YellowDamCrystanish",
    0xC7A6: "YellowDamCrystCape",
    0xC7A7: "YellowDamCrystChest",
    0xC7A8: "YellowDamAmberRobe",
    0xC7A9: "RedDamSwdOfAnger",
    0xC7AA: "RedDamFireSlshr",
    0xC7AB: "RedDamFireStaff",
    0xC7AC: "BlueDamAntidote",
    0xC7AD: "BlueDamCresceGear",
    0xC7AE: "BlueDamSnowCrown",
    0xC7AF: "BlueDamStarMist",
    0xC7B0: "BlueDamWindScarf",
    0xC7B1: "BlueDamColorScarf",
    0xC7B2: "BlueDamTrimate",
    0xC7B3: "BlueDamStormGear",
    0xC7B4: "GreenDamStarMist",
    0xC7B5: "GreenDamAegis",
    0xC7B6: "GreenDamTelepipe",
    0xC7B7: "GreenDamGrSleeves",
    0xC7B8: "GreenDamTruthSlvs",
    0xC7B9: "BiosystemTrimate",
    0xC7BA: "BiosystemAntidote",
    0xC7BB: "BiosystemPoisonShot",
    0xC7BC: "BiosystemAntidote2",
    0xC7BD: "BiosystemScalpel",
    0xC7BE: "BiosystemStarMist",
    0xC7BF: "BiosystemDynamite",
    0xC7C0: "ClimatrolJwlRibbon",
    0xC7C1: "ClimatrolFiberVest",
    0xC7C2: "ClimatrolKnifeBoots",
    0xC7C3: "ClimatrolSilRibbon",
    0xC7C4: "ClimatrolSandals",
    0xC7C5: "ClimatrolLaserBar",
    0xC7C6: "ClimatrolCeramBar",
    0xC7C7: "NeiShield",
    0xC7C8: "NeiEmel",
    0xC7C9: "NavalTruthSlvs",
    0xC7CA: "NavalTrimate",
    0xC7CB: "NavalMirEmel",
    0xC7CC: "NavalLaconEmel",
    0xC7CD: "NavalGrSleeves",
    0xC7CE: "NeiCrown",
    0xC7CF: "MenobeStormGear",
    0xC7D0: "NeiMet",
    0xC7D1: "MenobeColorScarf",
    0xC7D2: "NeiSlasher",
    0xC7D3: "NeiShot",
    0xC7D4: "IkutoFireStaff",
    0xC7D5: "IkutoLacnMace",
    0xC7D6: "IkutoPlsCannon",
    0xC7D7: "IkutoLacDagger",
    0xC7D8: "GuaronAmberRobe",
    0xC7D9: "GuaronLaconinish",
    0xC7DA: "GuaronCrystChest",
    0xC7DB: "NeiCape",
    0xC7DC: "GuaronCrystCape",
    0xC7DD: "NeiArmor",
    0xC7FF: "apItemCount",
    0xCD00: "scriptId",
    0xCD01: "textId",
    0xDE55: "windowIndex",
    0xDE57: "windowRoutine1",
    0xDE59: "windowRoutine2",
    0xDE5B: "windowRoutine3",
    0xDE5D: "windowRoutine4",
    0xDE6E: "interactionType",
    0xDE6F: "interactionSubtype",
    0xDE71: "interactionRoutine1",
    0xDE73: "interactionRoutine2",
    0xF600: "gameMode",
    0xF751: "cutsceneFlag",
    0xF753: "cutsceneIndex",
    0xFFF0: "openingEndingFlag",
}

party_size = IntSpan(RAM, 0xC600, 2)
party_composition = [
    IntSpan(RAM, 0xC608, 2),
    IntSpan(RAM, 0xC60A, 2),
    IntSpan(RAM, 0xC60C, 2),
    IntSpan(RAM, 0xC60E, 2),
]
current_money = IntSpan(RAM, 0xC620, 4)

map_index = IntSpan(RAM, 0xC640, 2)
quest_flags = IntSpan(RAM, 0xC700, 0x53)
chest_flags = IntSpan(RAM, 0xC780, 0x94)
received_item_storage = IntSpan(RAM, 0xC7FE, 2)
script_status = IntSpan(RAM, 0xCD00, 2)
window_status = IntSpan(RAM, 0xDE54, 10)
interaction_status = IntSpan(RAM, 0xDE6E, 4)
game_mode = IntSpan(RAM, 0xF600, 1)
scene_status = IntSpan(RAM, 0xF750, 4)
opening_ending_flag = IntSpan(RAM, 0xFFF0, 1)

party_inventories = [
    IntSpan(RAM, 0xC027, 17),
    IntSpan(RAM, 0xC067, 17),
    IntSpan(RAM, 0xC0A7, 17),
    IntSpan(RAM, 0xC0E7, 17),
    IntSpan(RAM, 0xC127, 17),
    IntSpan(RAM, 0xC167, 17),
    IntSpan(RAM, 0xC1A7, 17),
    IntSpan(RAM, 0xC1E7, 17),
]


# ROM addresses

rom_international_name = StrSpan(ROM, 0x150, 32)
rom_version = StrSpan(ROM, 0x18C, 2)

CHECKSUM_FAILED_JUMP = 0x250

MOVE_NEGATIVE = [0x3868, 0x38C8, 0x397C, 0x39B0]
MOVE_POSITIVE = [0x388E, 0x38EE, 0x3992, 0x39C6]
MOVE_FRAME_COUNT = 0x38FE

JUMP_FOLLOWING_CHARACTER_SPEED = 0x3B26

STARTING_MESETA_AMOUNT = 0x8A58

JUMP_FIX_RECORDER_LOOP_CT_OUTSIDE = 0xC072
JUMP_FIX_RECORDER_LOOP_GOVERNOR = 0xC9BE

TREASURE_CHEST_CONTENT_ARRAY = 0xE8C2
# 2 bytes each:
#   if high bit of word set, item id
#   otherwise, meseta amount

JUMP_SET_RECORDER_FLAG = 0xC4E2
JUMP_SET_MUSIK_FLAG = 0xC7F6
JUMP_SET_LEAF_FLAG = 0xC960
JUMP_APPLY_XP_MULTIPLIER = 0xF2BE
JUMP_APPLY_MESETA_MULTIPLIER = 0xF30E

TECH_LEARN_TABLES = 0x1150E

ENCOUNTER_RATE_SHIFT = 0x117DA

ENEMY_DATA_ARRAY = 0x2409A
# 64 bytes each:
#   xp at 35-36
#   meseta at 37-38

PATCH_MULWW = 0xBF6FC
PATCH_APPLY_XP_MULTIPLIER = 0xBF724
PATCH_APPLY_MESETA_MULTIPLIER = 0xBF736
PATCH_SET_MUSIK_FLAG = 0xBF756
PATCH_SET_RECORDER_FLAG = 0xBF766
PATCH_SET_LEAF_FLAG = 0xBF776
PATCH_FOLLOWING_CHARACTER_SPEED = 0xBF788
PATCH_FIX_RECORDER_LOOP_CT_OUTSIDE = 0xBF7AC
PATCH_FIX_RECORDER_LOOP_GOVERNOR = 0xBF7C8

name_space = StrSpan(ROM, 0xBFE00, 0x200, "utf-8")
goal_space = IntSpan(ROM, 0xBFDFF, 1)
