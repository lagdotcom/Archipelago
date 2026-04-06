from enum import IntEnum


class GameMode(IntEnum):
    MakeParty = 0
    Explore = 1
    Combat = 2
    Intro = 3
    BattleBegins = 4
    Spoils = 5
    BadEnding = 7
    GoodEnding = 8
    Resting = 9
