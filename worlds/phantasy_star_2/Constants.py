game_name = 'Phantasy Star II'

# RAM addresses

QUEST_FLAG_START = 0xc700
QUEST_FLAG_LEN = 0x48

CHEST_FLAG_START = 0xc780
CHEST_FLAG_LEN = 94

GAME_MODE = 0xf600
OPENING_ENDING_FLAG = 0xfff0

# ROM addresses

ROM_INTERNATIONAL_NAME = 0x150
ROM_VERSION = 0x18c

TREASURE_CHEST_CONTENT_ARRAY = 0xe8c2
# 2 bytes each:
#   if high bit of word set, item id
#   otherwise, meseta amount

CHECKSUM_FAILED_JUMP = 0x250

NAME_SPACE = 0xbf700
NAME_SPACE_LEN = 0x200

GOAL_SPACE = 0xbf6ff
