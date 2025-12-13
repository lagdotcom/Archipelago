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
    0xC067: "Nei.itemCount",
    0xC068: "Nei.item[0]",
    0xC069: "Nei.item[1]",
    0xC06A: "Nei.item[2]",
    0xC06B: "Nei.item[3]",
    0xC06C: "Nei.item[4]",
    0xC06D: "Nei.item[5]",
    0xC06E: "Nei.item[6]",
    0xC06F: "Nei.item[7]",
    0xC070: "Nei.item[8]",
    0xC071: "Nei.item[9]",
    0xC072: "Nei.item[10]",
    0xC073: "Nei.item[11]",
    0xC074: "Nei.item[12]",
    0xC075: "Nei.item[13]",
    0xC076: "Nei.item[14]",
    0xC077: "Nei.item[15]",
    0xC0A7: "Rudolf.itemCount",
    0xC0A8: "Rudolf.item[0]",
    0xC0A9: "Rudolf.item[1]",
    0xC0AA: "Rudolf.item[2]",
    0xC0AB: "Rudolf.item[3]",
    0xC0AC: "Rudolf.item[4]",
    0xC0AD: "Rudolf.item[5]",
    0xC0AE: "Rudolf.item[6]",
    0xC0AF: "Rudolf.item[7]",
    0xC0B0: "Rudolf.item[8]",
    0xC0B1: "Rudolf.item[9]",
    0xC0B2: "Rudolf.item[10]",
    0xC0B3: "Rudolf.item[11]",
    0xC0B4: "Rudolf.item[12]",
    0xC0B5: "Rudolf.item[13]",
    0xC0B6: "Rudolf.item[14]",
    0xC0B7: "Rudolf.item[15]",
    0xC0E7: "Amy.itemCount",
    0xC0E8: "Amy.item[0]",
    0xC0E9: "Amy.item[1]",
    0xC0EA: "Amy.item[2]",
    0xC0EB: "Amy.item[3]",
    0xC0EC: "Amy.item[4]",
    0xC0ED: "Amy.item[5]",
    0xC0EE: "Amy.item[6]",
    0xC0EF: "Amy.item[7]",
    0xC0F0: "Amy.item[8]",
    0xC0F1: "Amy.item[9]",
    0xC0F2: "Amy.item[10]",
    0xC0F3: "Amy.item[11]",
    0xC0F4: "Amy.item[12]",
    0xC0F5: "Amy.item[13]",
    0xC0F6: "Amy.item[14]",
    0xC0F7: "Amy.item[15]",
    0xC127: "Hugh.itemCount",
    0xC128: "Hugh.item[0]",
    0xC129: "Hugh.item[1]",
    0xC12A: "Hugh.item[2]",
    0xC12B: "Hugh.item[3]",
    0xC12C: "Hugh.item[4]",
    0xC12D: "Hugh.item[5]",
    0xC12E: "Hugh.item[6]",
    0xC12F: "Hugh.item[7]",
    0xC130: "Hugh.item[8]",
    0xC131: "Hugh.item[9]",
    0xC132: "Hugh.item[10]",
    0xC133: "Hugh.item[11]",
    0xC134: "Hugh.item[12]",
    0xC135: "Hugh.item[13]",
    0xC136: "Hugh.item[14]",
    0xC137: "Hugh.item[15]",
    0xC167: "Anna.itemCount",
    0xC168: "Anna.item[0]",
    0xC169: "Anna.item[1]",
    0xC16A: "Anna.item[2]",
    0xC16B: "Anna.item[3]",
    0xC16C: "Anna.item[4]",
    0xC16D: "Anna.item[5]",
    0xC16E: "Anna.item[6]",
    0xC16F: "Anna.item[7]",
    0xC170: "Anna.item[8]",
    0xC171: "Anna.item[9]",
    0xC172: "Anna.item[10]",
    0xC173: "Anna.item[11]",
    0xC174: "Anna.item[12]",
    0xC175: "Anna.item[13]",
    0xC176: "Anna.item[14]",
    0xC177: "Anna.item[15]",
    0xC1A7: "Kain.itemCount",
    0xC1A8: "Kain.item[0]",
    0xC1A9: "Kain.item[1]",
    0xC1AA: "Kain.item[2]",
    0xC1AB: "Kain.item[3]",
    0xC1AC: "Kain.item[4]",
    0xC1AD: "Kain.item[5]",
    0xC1AE: "Kain.item[6]",
    0xC1AF: "Kain.item[7]",
    0xC1B0: "Kain.item[8]",
    0xC1B1: "Kain.item[9]",
    0xC1B2: "Kain.item[10]",
    0xC1B3: "Kain.item[11]",
    0xC1B4: "Kain.item[12]",
    0xC1B5: "Kain.item[13]",
    0xC1B6: "Kain.item[14]",
    0xC1B7: "Kain.item[15]",
    0xC1E7: "Shir.itemCount",
    0xC1E8: "Shir.item[0]",
    0xC1E9: "Shir.item[1]",
    0xC1EA: "Shir.item[2]",
    0xC1EB: "Shir.item[3]",
    0xC1EC: "Shir.item[4]",
    0xC1ED: "Shir.item[5]",
    0xC1EE: "Shir.item[6]",
    0xC1EF: "Shir.item[7]",
    0xC1F0: "Shir.item[8]",
    0xC1F1: "Shir.item[9]",
    0xC1F2: "Shir.item[10]",
    0xC1F3: "Shir.item[11]",
    0xC1F4: "Shir.item[12]",
    0xC1F5: "Shir.item[13]",
    0xC1F6: "Shir.item[14]",
    0xC1F7: "Shir.item[15]",
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
    0xC702: "SkureB1",
    0xC703: "Skure",
    0xC704: "Paseo",
    0xC705: "Arima",
    0xC706: "Oputa",
    0xC707: "Zema",
    0xC708: "Kueri",
    0xC709: "Piata",
    0xC70A: "Aukba",
    0xC70B: "Zosa",
    0xC70C: "Ryuon",
    0xC710: "mapEventLoad",
    0xC711: "mapEventRun",
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
    0xC753: "jetScooterGuy",
    0xC754: "gairaControlPanel",
    0xC781: "Skure.15000Meseta",
    0xC782: "Skure.MogicCap",
    0xC783: "Skure.18000Meseta",
    0xC784: "Skure.MagicCap",
    0xC785: "Skure.7800Meseta",
    0xC786: "Skure.LaconChest",
    0xC787: "Skure.5600Meseta",
    0xC788: "Skure.GardaBoots",
    0xC789: "Skure.8600",
    0xC78A: "Skure.MagicCap2",
    0xC78B: "Skure.12000",
    0xC78C: "Skure.6400",
    0xC78D: "Unknown.200Meseta",
    0xC78E: "EsperMansion.Prism",
    0xC78F: "EsperMansion.NeiSword",
    0xC790: "Shure.Monomate",
    0xC791: "Shure.150Meseta",
    0xC792: "Shure.Dynamite",
    0xC793: "Shure.Dynamite2",
    0xC794: "Shure.40Meseta",
    0xC795: "Shure.Dimate",
    0xC796: "Shure.Headgear",
    0xC797: "Shure.200Meseta",
    0xC798: "Shure.SilRibbon",
    0xC799: "Nido.20Meseta",
    0xC79A: "Nido.100Meseta",
    0xC79B: "Nido.Dimate",
    0xC79C: "Nido.Trimate",
    0xC79D: "Nido.60Meseta",
    0xC79E: "Roron.Garbage",
    0xC79F: "Roron.Garbage2",
    0xC7A0: "Roron.CeramBar",
    0xC7A1: "Roron.Garbage3",
    0xC7A2: "Roron.Cannon",
    0xC7A3: "Roron.Garbage4",
    0xC7A4: "YellowDam.Escapipe",
    0xC7A5: "YellowDam.Crystanish",
    0xC7A6: "YellowDam.CrystCape",
    0xC7A7: "YellowDam.CrystChest",
    0xC7A8: "YellowDam.AmberRobe",
    0xC7A9: "RedDam.SwdOfAnger",
    0xC7AA: "RedDam.FireSlshr",
    0xC7AB: "RedDam.FireStaff",
    0xC7AC: "BlueDam.Antidote",
    0xC7AD: "BlueDam.CresceGear",
    0xC7AE: "BlueDam.SnowCrown",
    0xC7AF: "BlueDam.StarMist",
    0xC7B0: "BlueDam.WindScarf",
    0xC7B1: "BlueDam.ColorScarf",
    0xC7B2: "BlueDam.Trimate",
    0xC7B3: "BlueDam.StormGear",
    0xC7B4: "GreenDam.StarMist",
    0xC7B5: "GreenDam.Aegis",
    0xC7B6: "GreenDam.Telepipe",
    0xC7B7: "GreenDam.GrSleeves",
    0xC7B8: "GreenDam.TruthSlvs",
    0xC7B9: "Biosystem.Trimate",
    0xC7BA: "Biosystem.Antidote",
    0xC7BB: "Biosystem.PoisonShot",
    0xC7BC: "Biosystem.Antidote2",
    0xC7BD: "Biosystem.Scalpel",
    0xC7BE: "Biosystem.StarMist",
    0xC7BF: "Biosystem.Dynamite",
    0xC7C0: "Climatrol.JwlRibbon",
    0xC7C1: "Climatrol.FiberVest",
    0xC7C2: "Climatrol.KnifeBoots",
    0xC7C3: "Climatrol.SilRibbon",
    0xC7C4: "Climatrol.Sandals",
    0xC7C5: "Climatrol.LaserBar",
    0xC7C6: "Climatrol.CeramBar",
    0xC7C7: "Naval.NeiShield",
    0xC7C8: "Naval.NeiEmel",
    0xC7C9: "Naval.TruthSlvs",
    0xC7CA: "Naval.Trimate",
    0xC7CB: "Naval.MirEmel",
    0xC7CC: "Naval.LaconEmel",
    0xC7CD: "Naval.GrSleeves",
    0xC7CE: "Menobe.NeiCrown",
    0xC7CF: "Menobe.StormGear",
    0xC7D0: "Menobe.NeiMet",
    0xC7D1: "Menobe.ColorScarf",
    0xC7D2: "Ikuto.NeiSlasher",
    0xC7D3: "Ikuto.NeiShot",
    0xC7D4: "Ikuto.FireStaff",
    0xC7D5: "Ikuto.LacnMace",
    0xC7D6: "Ikuto.PlsCannon",
    0xC7D7: "Ikuto.LacDagger",
    0xC7D8: "Guaron.AmberRobe",
    0xC7D9: "Guaron.Laconinish",
    0xC7DA: "Guaron.CrystChest",
    0xC7DB: "Guaron.NeiCape",
    0xC7DC: "Guaron.CrystCape",
    0xC7DD: "Guaron.NeiArmor",
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
    0xFFF1: "openingEndingFlag",
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
quest_flags = IntSpan(RAM, 0xC700, 0x55)
jet_scooter_flag = IntSpan(RAM, 0xC716, 1)
spaceship_flag = IntSpan(RAM, 0xC73F, 1)
chest_flags = IntSpan(RAM, 0xC780, 0x94)
received_item_storage = IntSpan(RAM, 0xC7FE, 2)
script_status = IntSpan(RAM, 0xCD00, 2)
window_status = IntSpan(RAM, 0xDE54, 10)
interaction_status = IntSpan(RAM, 0xDE6E, 4)
game_mode = IntSpan(RAM, 0xF600, 1)
scene_status = IntSpan(RAM, 0xF750, 4)
opening_ending_flag = IntSpan(RAM, 0xFFF0, 2)


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

MOTAVIAN_INIT_DELETE_CHECK = 0x42E8

STARTING_MESETA_AMOUNT = 0x8A58

JUMP_FIX_RECORDER_LOOP_CT_OUTSIDE = 0xC072
JUMP_FIX_RECORDER_LOOP_GOVERNOR = 0xC9BE

JUMP_GET_CARD = 0xDC22

JUMP_GAIRA_CONTROL_PANEL = 0xDFE6

JUMP_JET_SCOOTER_GUY = 0xE690

JUMP_INTERACT_ADD_ITEM = 0xE84E
PATCH_ADD_ITEM2_REARRANGE = 0xE89C

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

MISC_MESSAGES = 0x22BE4

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
PATCH_ADD_ITEM = 0xBF7E4
PATCH_JET_SCOOTER_GUY_TALK = 0xBF838
PATCH_CARD_LOOKUP_TABLE = 0xBF872
PATCH_GET_CARD = 0xBF876
PATCH_GAIRA_CONTROL_PANEL = 0xBF892

name_space = StrSpan(ROM, 0xBFE00, 0x200, "utf-8")
goal_space = IntSpan(ROM, 0xBFDFF, 1)
