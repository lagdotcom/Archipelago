from enum import IntEnum
from typing import NamedTuple

from .Data import item_name as i

ART_PORTRAIT_LIBRARIAN = 0x2D9AA
ART_PORTRAIT_SAVE_EMPLOYEE = 0x2E13A
ART_PORTRAIT_DOCTOR = 0x2E8B2
ART_PORTRAIT_GRANDMA = 0x2EF70
ART_PORTRAIT_ITEM_SELLER = 0x2F73E
ART_PORTRAIT_WEAPON_SELLER = 0x2FDEA
ART_PORTRAIT_ARMOR_SELLER = 0x3060E
ART_PORTRAIT_USTVESTIA = 0x30E38
ART_PORTRAIT_DEZOLIAN = 0x314D8
ART_PORTRAIT_ITEM_KEEPER = 0x32ACC
ART_PORTRAIT_GOVERNOR = 0x32410
ART_PORTRAIT_ROLF = 0x346C8
ART_PORTRAIT_NEI = 0x34F6A
ART_PORTRAIT_RUDO = 0x35798
ART_PORTRAIT_AMY = 0x35EDA
ART_PORTRAIT_HUGH = 0x3664E
ART_PORTRAIT_ANNA = 0x36D76
ART_PORTRAIT_KAIN = 0x3751A
ART_PORTRAIT_SHIR = 0x37C4E
ART_PORTRAIT_TELEPORT_EMPLOYEE = 0x38F22

ART_BATTLE_ROLF = 0x71E8E
ART_BATTLE_NEI = 0x7271C
ART_BATTLE_RUDO = 0x72ECA
ART_BATTLE_AMY_SHIR = 0x738FC
ART_BATTLE_ANNA = 0x7400A
ART_BATTLE_HUGH_KAIN = 0x7485A

ART_WALK_ROLF = 0xFF3000
ART_WALK_NEI = 0xFF3900
ART_WALK_RUDO = 0xFF5400
ART_WALK_AMY_SHIR = 0xFF4200
ART_WALK_ANNA = 0xFF4B00
ART_WALK_HUGH_KAIN = 0xFF5D00

MAPPING_PORTRAIT_LIBRARIAN = 0x149BC
MAPPING_PORTRAIT_SAVE_EMPLOYEE = 0x14A34
MAPPING_PORTRAIT_DOCTOR = 0x14AAC
MAPPING_PORTRAIT_GRANDMA = 0x14B24
MAPPING_PORTRAIT_ITEM_SELLER = 0x14B9C
MAPPING_PORTRAIT_WEAPON_SELLER = 0x14C14
MAPPING_PORTRAIT_ARMOR_SELLER = 0x14C8C
MAPPING_PORTRAIT_USTVESTIA = 0x14D04
MAPPING_PORTRAIT_DEZOLIAN = 0x14D7C
MAPPING_PORTRAIT_ITEM_KEEPER = 0x14F5C
MAPPING_PORTRAIT_GOVERNOR = 0x14EE4
MAPPING_PORTRAIT_TELEPORT_EMPLOYEE = 0x1504C
MAPPING_PORTRAIT_ROLF = 0x150C4
MAPPING_PORTRAIT_NEI = 0x1513C
MAPPING_PORTRAIT_RUDO = 0x151B4
MAPPING_PORTRAIT_AMY = 0x1522C
MAPPING_PORTRAIT_HUGH = 0x152A4
MAPPING_PORTRAIT_ANNA = 0x1531C
MAPPING_PORTRAIT_KAIN = 0x15394
MAPPING_PORTRAIT_SHIR = 0x1540C

MAPPING_BATTLE_ROLF = 0x750F8
MAPPING_BATTLE_NEI = 0x751EA
MAPPING_BATTLE_RUDO = 0x752CC
MAPPING_BATTLE_AMY = 0x753CA
MAPPING_BATTLE_SHIR = 0x753D8
MAPPING_BATTLE_KAIN = 0x75494
MAPPING_BATTLE_HUGH = 0x754A2
MAPPING_BATTLE_ANNA = 0x755AE


class Pal(IntEnum):
    Rolf = 0x11
    Nei = 0x12
    Rudo = 0x13
    Amy = 0x14
    Hugh = 0x15
    Anna = 0x16
    Kain = 0x17
    Shir = 0x18
    Librarian = 0x19
    MotaSave = 0x1A
    MotaDoctor = 0x1B
    Grandma = 0x1C
    MotaItem = 0x1D
    MotaWeapon = 0x1E
    MotaArmor = 0x1F
    Ustvestia = 0x20
    Dezolian1 = 0x21
    Dezolian2 = 0x22
    Dezolian3 = 0x23
    Dezolian4 = 0x24
    ItemKeeper = 0x25
    Governor = 0x28
    EndingRUDO = 0x44
    EndingAmy = 0x45
    EndingKain = 0x46
    EndingShir = 0x47
    EndingHugh = 0x48
    EndingAnna = 0x49
    EndingRolf = 0x4A


class Win(IntEnum):
    RolfProfile = 0x2B
    NeiProfile = 0x2C
    RudoProfile = 0x2D
    AmyProfile = 0x2E
    HughProfile = 0x2F
    AnnaProfile = 0x30
    KainProfile = 0x31
    ShirProfile = 0x32
    RolfPortrait = 0x3B
    NeiPortrait = 0x3C
    RudoPortrait = 0x3D
    AmyPortrait = 0x3E
    HughPortrait = 0x3F
    AnnaPortrait = 0x40
    KainPortrait = 0x41
    ShirPortrait = 0x42
    LibrarianPortrait = 0x43
    SaveEmployeePortrait = 0x44
    DoctorPortrait = 0x45
    GrandmaPortrait = 0x46
    ItemSellerPortrait = 0x47
    WeaponSellerPortrait = 0x48
    ArmorSellerPortrait = 0x49
    UstvestiaPortrait = 0x4A
    Dezolian1Portrait = 0x4B
    Dezolian2Portrait = 0x4C
    Dezolian3Portrait = 0x4D
    Dezolian4Portrait = 0x4E
    ItemKeeperPortrait = 0x4F
    GovernorPortrait = 0x52
    RolfPortrait2 = 0x72


class Level(NamedTuple):
    xp: int
    hp: int
    tp: int
    st: int
    men: int
    agi: int
    luck: int
    dex: int
    at: int
    df: int
    map_tech: list[str]
    battle_tech: list[str]

    def to_bytes(self, name: str, level: int):
        if self.xp > 0xFFFFFF:
            raise Exception(f"{name} level {level} requires {self.xp} xp; too high")
        if len(self.map_tech) > 4:
            raise Exception(f"{name} level {level} has too many map techs")
        if len(self.battle_tech) > 4:
            raise Exception(f"{name} level {level} has too many battle techs")
        techs = len(self.map_tech) | (len(self.battle_tech) << 4)
        return (self.xp | level << 24).to_bytes(4, "big") + bytes(
            [
                self.hp,
                self.tp,
                self.st,
                self.men,
                self.agi,
                self.luck,
                self.dex,
                self.at,
                self.df,
                techs,
            ]
        )


class TextRef(NamedTuple):
    script: int
    num: int


type Text = TextRef | str


class Equipped(NamedTuple):
    item: str
    other_hand: bool = False


type Item = Equipped | str


class BattleSprite(NamedTuple):
    art: int
    mapping: int
    high_byte: int = 0

    def to_bytes(self):
        return self.high_byte.to_bytes(1, "big") + self.mapping.to_bytes(3, "big") + self.art.to_bytes(4, "big")


class Portrait(NamedTuple):
    palette_id: Pal
    art: int
    win_id: Win
    win_addr: int
    mapping: int

    def portrait_bytes(self):
        return self.palette_id.value.to_bytes(1, "big") + self.art.to_bytes(3, "big")

    def win_bytes(self):
        return self.win_addr.to_bytes(2, "big") + self.mapping.to_bytes(4, "big")


class WalkSprite(NamedTuple):
    address: int
    offset: int = 0x3

    def to_bytes(self):
        return self.offset.to_bytes(1, "big") + self.address.to_bytes(3, "big")


class Char:
    def __init__(
        self,
        name: str,
        job: str,
        profile: str,
        portrait: Portrait,
        walk_sprite: WalkSprite,
        battle_sprite: BattleSprite,
        levels: list[Level],
        join_text: Text,
        rename_text: Text,
        starting_items: list[Item],
        can_equip: set[str],
    ):
        self.name = name
        self.job = job
        self.profile = profile.strip()
        self.portrait = portrait
        self.walk_sprite = walk_sprite
        self.battle_sprite = battle_sprite
        self.levels = levels
        self.join_text = join_text
        self.rename_text = rename_text
        self.starting_items = starting_items
        self.can_equip = can_equip
        if len(name) > 4:
            raise Exception("name must be up to 4 chars")
        if len(job) != 8:
            raise Exception("job must be 8 chars")

    def get_tech_learn_set(self):
        techs = set[str]()
        for lvl in self.levels:
            for t in lvl.map_tech:
                techs.add(t)
            for t in lvl.battle_tech:
                techs.add(t)
        return techs

    def get_map_techs(self):
        techs = list[str]()
        for lvl in self.levels:
            for t in lvl.map_tech:
                techs.append(t)
        return techs

    def get_battle_techs(self):
        techs = list[str]()
        for lvl in self.levels:
            for t in lvl.battle_tech:
                techs.append(t)
        return techs


Rolf = Char(
    "Rolf",
    " Agent  ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

LOST PARENTS AT AGE

10. HEALTHY AND HAS

BROAD RANGE OF

KNOWLEDGE.


▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Rolf, ART_PORTRAIT_ROLF, Win.RolfPortrait, 0x4102, MAPPING_PORTRAIT_ROLF),
    walk_sprite=WalkSprite(ART_WALK_ROLF),
    battle_sprite=BattleSprite(ART_BATTLE_ROLF, MAPPING_BATTLE_ROLF),
    join_text="ROLF_INTRO_TEXT",  # TODO
    rename_text="ROLF_RENAME_TEXT",  # TODO
    starting_items=[Equipped(i.Knife), Equipped(i.CarbonSuit), Equipped(i.Shoes)],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.TitaniGear,
        i.TitaniMet,
        i.NeiMet,
        i.MagicCap,
        i.MogicCap,
        i.CarbonSuit,
        i.FiberCoat,
        i.TtnmChest,
        i.CrmcChest,
        i.CrystChest,
        i.LaconChest,
        i.Shoes,
        i.Boots,
        i.GardaBoots,
        i.CrbnShield,
        i.FibrShild,
        i.MirShield,
        i.CerShield,
        i.Knife,
        i.Sword,
        i.CeramSwrd,
        i.CeramKnfe,
        i.LasrSword,
        i.LaserKnfe,
        i.SwdOfAng,
        i.LacSword,
        i.NeiSword,
        i.BowGun,
        i.SonicGun,
        i.PrsnClths,
    },
    levels=[
        Level(0, 19, 15, 20, 28, 15, 13, 20, 12, 10, [], ["FOI"]),
        Level(29, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(83, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(170, 9, 6, 13, 10, 8, 10, 10, 7, 5, ["RYUKA"], []),
        Level(289, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], ["GIFOI", "TSU"]),
        Level(504, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(808, 7, 3, 5, 4, 3, 4, 4, 6, 5, ["HINAS"], ["ZAN"]),
        Level(1260, 9, 6, 13, 10, 8, 10, 10, 7, 6, ["RES"], ["RES"]),
        Level(1930, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(2924, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], ["GRA"]),
        Level(4375, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], ["GITHU"]),
        Level(6504, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], []),
        Level(9622, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(14164, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], ["NAFOI"]),
        Level(20783, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(30427, 9, 6, 13, 10, 8, 10, 10, 7, 6, ["GIRES"], ["GIZAN", "GIRES"]),
        Level(44475, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(64881, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(86896, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(110999, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], ["NATHU"]),
        Level(138112, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(168140, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(203229, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(243327, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], ["NAZAN"]),
        Level(288460, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(338688, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(393651, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(453784, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], ["GIGRA"]),
        Level(518785, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(588907, 7, 3, 5, 4, 3, 4, 4, 5, 4, ["REVER"], []),
        Level(679300, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(767609, 9, 6, 12, 10, 8, 10, 10, 7, 6, [], []),
        Level(867398, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(980160, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(1107581, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], ["MEGID"]),
        Level(1251567, 9, 6, 14, 10, 8, 10, 10, 7, 6, [], []),
        Level(1414270, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(1598125, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(1805882, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(2040647, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], []),
        Level(2305931, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(2605702, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(2944443, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(3327221, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], []),
        Level(3759759, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(4248528, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
        Level(4800837, 7, 3, 5, 4, 3, 4, 4, 6, 5, [], []),
        Level(5424946, 9, 6, 13, 10, 8, 10, 10, 7, 6, [], []),
        Level(6130189, 6, 3, 5, 4, 3, 4, 4, 4, 3, [], []),
        Level(6927113, 7, 3, 5, 4, 3, 4, 4, 5, 4, [], []),
    ],
)
Nei = Char(
    "Nei",
    " Kitty! ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

"NEI" MEANS "THE HUMAN

WHO WAS NOT A HUMAN."

LITHE AND AGILE LIKE

AN ANIMAL, SHE HATES

CARRYING A HEAVY LOAD.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Nei, ART_PORTRAIT_NEI, Win.NeiPortrait, 0x4102, MAPPING_PORTRAIT_NEI),
    walk_sprite=WalkSprite(ART_WALK_NEI, 0x23),
    battle_sprite=BattleSprite(ART_BATTLE_NEI, MAPPING_BATTLE_NEI, 0x20),
    join_text="NEI_INTRO_TEXT",  # TODO
    rename_text="NEI_RENAME_TEXT",  # TODO
    starting_items=[Equipped(i.Ribbon), Equipped(i.CarbonVest), Equipped(i.Sandals)],
    can_equip={
        i.Ribbon,
        i.SilRibbon,
        i.JwlRibbon,
        i.CarbonVest,
        i.FiberVest,
        i.Sandals,
        i.KnifeBoots,
        i.SteelBar,
        i.CeramBar,
        i.LaserBar,
        i.PrsnClths,
    },
    levels=[
        Level(0, 12, 10, 14, 18, 27, 10, 14, 7, 12, ["RES"], ["RES"]),
        Level(12, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(25, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(56, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(83, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(124, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(169, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(233, 6, 4, 15, 9, 2, 10, 10, 6, 5, [], []),
        Level(303, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(396, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(510, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(657, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(832, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(1054, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(1310, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(1629, 6, 4, 15, 9, 2, 10, 10, 6, 5, ["ANTI"], []),
        Level(2020, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(2506, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(3083, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(3793, 4, 2, 2, 1, 2, 1, 1, 2, 2, ["SAK"], ["SAK"]),
        Level(4591, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(5557, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(6672, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(8013, 6, 4, 15, 9, 2, 10, 10, 6, 5, ["NASAK"], ["NASAK"]),
        Level(9601, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(11506, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(13802, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(16558, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(20212, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(24674, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(30207, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(36983, 6, 4, 15, 9, 2, 10, 10, 6, 5, [], []),
        Level(45128, 4, 2, 2, 1, 2, 1, 1, 2, 1, [], []),
        Level(55069, 4, 2, 2, 1, 2, 1, 1, 2, 2, [], []),
        Level(66406, 4, 1, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(80078, 4, 2, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(97299, 4, 1, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(118224, 4, 2, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(143368, 4, 1, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(173862, 6, 6, 15, 9, 8, 10, 10, 6, 5, [], []),
        Level(201646, 4, 1, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(233871, 4, 2, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(248608, 4, 1, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(264274, 4, 2, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(280926, 4, 1, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(298629, 4, 2, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(317447, 4, 1, 2, 1, 1, 1, 1, 2, 2, [], []),
        Level(337451, 6, 6, 15, 9, 8, 10, 10, 6, 5, [], []),
        Level(358715, 4, 1, 2, 1, 1, 1, 1, 2, 1, [], []),
        Level(381320, 4, 2, 2, 1, 1, 1, 1, 1, 2, [], []),
    ],
)
Rudo = Char(
    "Rudo",
    " Hunter ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

LEFT THE ARMY AND

BECAME A HUNTER AFTER

WIFE AND CHILD DIED.

VERY STRONG, CAN USE

HEAVY GUNS WITH EASE.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(
        Pal.Rudo,
        ART_PORTRAIT_RUDO,
        Win.RudoPortrait,
        0x4102,
        MAPPING_PORTRAIT_RUDO,
    ),
    walk_sprite=WalkSprite(ART_WALK_RUDO),
    battle_sprite=BattleSprite(ART_BATTLE_RUDO, MAPPING_BATTLE_RUDO),
    join_text=TextRef(9, 28),
    rename_text=TextRef(9, 22),
    starting_items=[
        Equipped(i.Headgear),
        Equipped(i.BowGun),
        Equipped(i.FiberCoat),
        Equipped(i.Boots),
    ],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.TitaniGear,
        i.CresceGear,
        i.Laconigear,
        i.LaconiaMet,
        i.CarbonSuit,
        i.FiberCoat,
        i.TtnmArmor,
        i.CrmcArmor,
        i.Crystanish,
        i.Laconinish,
        i.NeiArmor,
        i.Shoes,
        i.Boots,
        i.GardaBoots,
        i.CrbnShield,
        i.FibrShild,
        i.MirShield,
        i.CerShield,
        i.LacShield,
        i.Knife,
        i.Dagger,
        i.CeramKnfe,
        i.LaserKnfe,
        i.BowGun,
        i.SonicGun,
        i.Shotgun,
        i.Cannon,
        i.Vulcan,
        i.LaserShot,
        i.LsrCannon,
        i.PlsCannon,
        i.PulseVlcn,
        i.NeiShot,
        i.PrsnClths,
    },
    levels=[
        Level(0, 44, 0, 60, 28, 15, 7, 12, 10, 12, [], []),
        Level(32, 6, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(91, 7, 0, 13, 6, 6, 8, 6, 5, 8, [], []),
        Level(186, 6, 0, 4, 3, 3, 2, 3, 3, 6, [], []),
        Level(316, 8, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(551, 9, 0, 13, 6, 6, 8, 6, 6, 8, [], []),
        Level(883, 6, 0, 4, 3, 3, 2, 3, 3, 6, [], []),
        Level(1376, 8, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(2108, 9, 0, 13, 6, 6, 8, 6, 6, 8, [], []),
        Level(3195, 6, 0, 6, 3, 3, 2, 3, 3, 6, [], []),
        Level(4781, 8, 0, 6, 3, 3, 2, 3, 4, 7, [], []),
        Level(7107, 9, 0, 9, 6, 6, 8, 6, 6, 8, [], []),
        Level(10514, 6, 0, 4, 3, 3, 2, 3, 3, 6, [], []),
        Level(15477, 8, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(22710, 9, 0, 13, 6, 6, 8, 6, 6, 8, [], []),
        Level(33248, 6, 0, 4, 3, 3, 2, 3, 3, 6, [], []),
        Level(48599, 8, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(70897, 9, 0, 13, 6, 6, 8, 6, 6, 8, [], []),
        Level(94953, 6, 0, 2, 3, 3, 2, 3, 3, 6, [], []),
        Level(121291, 8, 0, 4, 3, 3, 2, 3, 4, 7, [], []),
        Level(150918, 9, 0, 15, 6, 6, 8, 6, 6, 4, [], []),
        Level(183731, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(222073, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(265889, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(315208, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(370093, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(430153, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(495862, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(566890, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(643514, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(742289, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(838787, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(947829, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(1071047, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(1210283, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(1367621, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(1545411, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(1746314, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(1973336, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(2229870, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(2519753, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(2847320, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(3217472, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(3635744, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(4108390, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(4642481, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(5246004, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
        Level(5927984, 9, 0, 13, 6, 6, 8, 6, 6, 4, [], []),
        Level(6698623, 6, 0, 4, 3, 3, 2, 3, 3, 2, [], []),
        Level(7569443, 8, 0, 4, 3, 3, 2, 3, 4, 3, [], []),
    ],
)
Amy = Char(
    "Amy",
    " Doctor ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

A DOCTOR FROM A NORMAL

HOME. SPECIALIZES IN

BOTH HEALING WOUNDS

AND CURING POISON;

NOT STRONG IN BATTLE.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Amy, ART_PORTRAIT_AMY, Win.AmyPortrait, 0x4102, MAPPING_PORTRAIT_AMY),
    walk_sprite=WalkSprite(ART_WALK_AMY_SHIR),
    battle_sprite=BattleSprite(ART_BATTLE_AMY_SHIR, MAPPING_BATTLE_AMY),
    join_text=TextRef(9, 30),
    rename_text=TextRef(9, 23),
    starting_items=[Equipped(i.Scalpel), Equipped(i.CarbonSuit), Equipped(i.Shoes)],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.SilCrown,
        i.TitaniGear,
        i.JwlCrown,
        i.SnowCrown,
        i.NeiCrown,
        i.CarbonSuit,
        i.FiberCape,
        i.TtnmCape,
        i.CrmcCape,
        i.CrystCape,
        i.NeiCape,
        i.Shoes,
        i.Boots,
        i.HirzaBoots,
        i.CrbnEmel,
        i.FiberEmel,
        i.MirEmel,
        i.CerEmel,
        i.LaconEmel,
        i.Knife,
        i.Scalpel,
        i.CeramKnfe,
        i.LaserKnfe,
        i.FireStaff,
        i.SilentShot,
        i.PoisonShot,
        i.AcidShot,
        i.PrsnClths,
    },
    levels=[
        Level(0, 10, 18, 13, 24, 5, 8, 16, 7, 4, ["RES"], ["RES"]),
        Level(35, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], ["SHU"]),
        Level(99, 7, 3, 6, 3, 4, 8, 7, 3, 3, [], []),
        Level(203, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], ["DEBAN"]),
        Level(345, 5, 3, 3, 3, 2, 4, 3, 2, 3, ["ANTI"], ["FOI"]),
        Level(601, 7, 6, 6, 7, 4, 8, 7, 3, 3, ["GIRES"], ["GIRES"]),
        Level(965, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(1504, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(2304, 7, 6, 6, 7, 4, 8, 17, 3, 3, ["SAR"], ["SAR"]),
        Level(3491, 5, 3, 3, 3, 2, 4, 3, 2, 2, ["SAK"], ["SAK"]),
        Level(5225, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(7766, 7, 6, 6, 7, 4, 8, 7, 3, 3, ["NASAK"], ["NASAK"]),
        Level(11489, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(16912, 5, 4, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(24815, 7, 5, 6, 7, 4, 8, 7, 3, 3, ["NARES"], ["SASHU", "NARES"]),
        Level(36331, 5, 4, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(53105, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(75771, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], []),
        Level(103758, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(132538, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(164912, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], []),
        Level(200767, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(242666, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(290545, 7, 6, 6, 7, 4, 8, 7, 3, 3, ["REVER"], ["SANER"]),
        Level(344436, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(404411, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(470039, 7, 6, 6, 7, 4, 8, 7, 3, 3, ["GISAR"], ["GISAR"]),
        Level(541841, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(619456, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(703185, 7, 6, 6, 7, 4, 8, 7, 3, 3, ["NASAR"], ["NASAR"]),
        Level(811119, 5, 3, 3, 3, 2, 6, 3, 2, 2, [], []),
        Level(916565, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(1035718, 7, 6, 6, 7, 4, 6, 7, 3, 3, [], []),
        Level(1170362, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(1322509, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(1494436, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], []),
        Level(1688712, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(1908244, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(2156317, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], ["GRA"]),
        Level(2416639, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(2753402, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(3111344, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], []),
        Level(3515818, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(3972875, 5, 4, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(4489348, 7, 5, 6, 7, 4, 8, 7, 3, 3, [], []),
        Level(5072964, 5, 4, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(5732450, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
        Level(6477669, 7, 6, 6, 7, 4, 8, 7, 3, 3, [], ["GIGRA"]),
        Level(7319766, 5, 3, 3, 3, 2, 4, 3, 2, 2, [], []),
        Level(8271335, 5, 3, 3, 3, 2, 4, 3, 2, 3, [], []),
    ],
)
Hugh = Char(
    "Hugh",
    "Biologst",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

HAS BEEN INTRIGUED BY

NATURE SINCE HIS

CHILDHOOD; NOW THE

LEADING EXPERT ON

PLANTS AND ANIMALS.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Hugh, ART_PORTRAIT_HUGH, Win.HughPortrait, 0x4102, MAPPING_PORTRAIT_HUGH),
    walk_sprite=WalkSprite(ART_WALK_HUGH_KAIN, 0x23),
    battle_sprite=BattleSprite(ART_BATTLE_HUGH_KAIN, MAPPING_BATTLE_HUGH, 0x20),
    join_text=TextRef(9, 31),
    rename_text=TextRef(9, 23),
    starting_items=[
        Equipped(i.Scalpel, True),
        Equipped(i.CarbonSuit),
        Equipped(i.Shoes),
    ],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.TitaniGear,
        i.Laconigear,
        i.LaconiaMet,
        i.CarbonSuit,
        i.FiberCoat,
        i.TtnmChest,
        i.CrmcChest,
        i.AmberRobe,
        i.Shoes,
        i.Boots,
        i.GardaBoots,
        i.CrbnShield,
        i.FibrShild,
        i.MirShield,
        i.CerShield,
        i.Aegis,
        i.LacShield,
        i.NeiShield,
        i.Knife,
        i.Dagger,
        i.Scalpel,
        i.CeramKnfe,
        i.LaserKnfe,
        i.LacnMace,
        i.BowGun,
        i.SonicGun,
        i.PoisonShot,
        i.AcidShot,
        i.PrsnClths,
    },
    levels=[
        Level(0, 16, 19, 14, 26, 8, 6, 10, 7, 6, [], []),
        Level(34, 4, 3, 3, 3, 2, 4, 2, 3, 3, [], ["RIMIT"]),
        Level(96, 6, 5, 7, 5, 4, 8, 7, 3, 3, [], ["DORAN", "GEN"]),
        Level(197, 5, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(335, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], ["SAGEN", "SHINB"]),
        Level(584, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], ["SHIZA"]),
        Level(937, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(1460, 6, 3, 3, 3, 2, 4, 2, 3, 2, ["RES"], ["RES"]),
        Level(2237, 7, 4, 7, 5, 4, 8, 7, 3, 4, [], ["FOI"]),
        Level(3389, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(5072, 6, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(7539, 7, 5, 7, 5, 4, 8, 7, 3, 3, [], ["GIFOI"]),
        Level(11154, 5, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(16419, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(24093, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], ["VOL"]),
        Level(35273, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(51558, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(75214, 7, 4, 7, 5, 4, 8, 7, 3, 4, [], ["ZAN"]),
        Level(100736, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(128678, 6, 4, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(160109, 7, 4, 7, 5, 4, 8, 7, 3, 3, [], []),
        Level(194920, 5, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(235598, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(282082, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], ["SAVOL"]),
        Level(334404, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(392632, 6, 0, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(456349, 7, 7, 7, 5, 4, 8, 7, 3, 4, [], ["GRA"]),
        Level(526060, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(601414, 6, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(682704, 7, 5, 7, 5, 4, 8, 7, 3, 3, [], ["GIRES"]),
        Level(787494, 5, 2, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(889869, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(1005552, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], ["GIGRA"]),
        Level(1136274, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(1283989, 6, 2, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(1450909, 7, 6, 7, 5, 4, 8, 7, 3, 4, [], ["GIZAN"]),
        Level(1639526, 5, 2, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(1852664, 6, 2, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(2093512, 7, 7, 7, 5, 4, 8, 7, 3, 3, [], []),
        Level(2365669, 5, 2, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(2673206, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(3020722, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], []),
        Level(3413416, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(3857161, 6, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(4358591, 7, 5, 7, 5, 4, 8, 7, 3, 4, [], []),
        Level(4925208, 5, 3, 3, 3, 2, 4, 2, 3, 2, [], []),
        Level(5565485, 6, 2, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(6288999, 7, 6, 7, 5, 4, 8, 7, 3, 3, [], []),
        Level(7106569, 5, 3, 3, 3, 2, 4, 2, 3, 3, [], []),
        Level(8030422, 6, 2, 3, 3, 2, 4, 2, 3, 2, [], []),
    ],
)
Anna = Char(
    "Anna",
    "Guardian",
    profile="""
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

OF UNCERTAIN AGE AND

BACKGROUND, SHE IS A

VICIOUS FIGHTER WITH

A SLICER OR WHIP.

TAKES NO PRISONERS.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Anna, ART_PORTRAIT_ANNA, Win.AnnaPortrait, 0x4102, MAPPING_PORTRAIT_ANNA),
    walk_sprite=WalkSprite(ART_WALK_ANNA),
    battle_sprite=BattleSprite(ART_BATTLE_ANNA, MAPPING_BATTLE_ANNA),
    join_text=TextRef(9, 33),
    rename_text=TextRef(9, 23),
    starting_items=[
        Equipped(i.Headgear),
        Equipped(i.Boomerang),
        Equipped(i.FiberCape),
        Equipped(i.Boots),
    ],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.SilCrown,
        i.TitaniGear,
        i.JwlCrown,
        i.ColorScarf,
        i.CarbonSuit,
        i.FiberCape,
        i.TtnmCape,
        i.CrmcCape,
        i.CrystCape,
        i.LaconCape,
        i.Shoes,
        i.Boots,
        i.KnifeBoots,
        i.LongBoots,
        i.ShuneBoots,
        i.CrbnEmel,
        i.FiberEmel,
        i.MirEmel,
        i.CerEmel,
        i.GrSleeves,
        i.LaconEmel,
        i.NeiEmel,
        i.Knife,
        i.Boomerang,
        i.Slasher,
        i.Whip,
        i.CeramKnfe,
        i.LasrSlshr,
        i.LaserKnfe,
        i.FireSlshr,
        i.ACSlashr,
        i.NeiSlasher,
        i.PrsnClths,
    },
    levels=[
        Level(0, 18, 12, 20, 27, 20, 9, 15, 12, 11, [], ["FOI"]),
        Level(31, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(88, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(180, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(306, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(535, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], ["NER"]),
        Level(857, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(1336, 7, 6, 16, 13, 20, 17, 25, 4, 11, [], ["SHIFT"]),
        Level(2047, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(3102, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(4642, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(6900, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(10207, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(15026, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(22048, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(32280, 7, 7, 16, 13, 20, 17, 25, 4, 11, [], ["FANBI"]),
        Level(47183, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(68832, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(92187, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(117758, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(146523, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(178379, 6, 1, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(215605, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(258145, 7, 6, 16, 13, 20, 17, 25, 4, 11, [], []),
        Level(306027, 6, 2, 4, 2, 2, 3, 3, 2, 2, [], []),
        Level(359314, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(417624, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(481419, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(550379, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(624771, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(720669, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(814356, 7, 6, 16, 13, 20, 17, 25, 4, 11, [], ["ZAN"]),
        Level(920222, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(1039851, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(1175032, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(1327787, 6, 1, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(1500339, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(1695450, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(1915860, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(2164922, 7, 6, 16, 13, 20, 17, 25, 4, 11, [], []),
        Level(2446362, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(2764389, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(3123759, 6, 1, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(3529848, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(3988728, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(4507263, 6, 2, 4, 2, 2, 3, 3, 3, 3, [], []),
        Level(5093207, 6, 2, 4, 2, 2, 3, 3, 3, 2, [], []),
        Level(5755325, 7, 6, 16, 13, 20, 17, 25, 4, 11, [], []),
        Level(6503517, 3, 2, 4, 2, 2, 3, 3, 2, 2, [], []),
        Level(7348974, 4, 1, 4, 2, 2, 3, 3, 2, 2, [], []),
    ],
)
Kain = Char(
    "Kain",
    "Wrecker ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

WANTED TO BE A

MECHANIC, BUT ALWAYS

BROKE WHATEVER HE

TRIED TO FIX; DECIDED

TO MAKE THAT HIS JOB.
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Kain, ART_PORTRAIT_KAIN, Win.KainPortrait, 0x4102, MAPPING_PORTRAIT_KAIN),
    walk_sprite=WalkSprite(ART_WALK_HUGH_KAIN),
    battle_sprite=BattleSprite(ART_BATTLE_HUGH_KAIN, MAPPING_BATTLE_KAIN),
    join_text=TextRef(9, 33),
    rename_text=TextRef(9, 24),
    starting_items=[Equipped(i.Dagger), Equipped(i.FiberCoat), Equipped(i.Shoes)],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.TitaniGear,
        i.TitaniMet,
        i.StormGear,
        i.NeiMet,
        i.CarbonSuit,
        i.FiberCoat,
        i.TtnmArmor,
        i.CrmcArmor,
        i.Crystanish,
        i.Laconinish,
        i.NeiArmor,
        i.Shoes,
        i.Boots,
        i.GardaBoots,
        i.CrbnShield,
        i.FibrShild,
        i.MirShield,
        i.CerShield,
        i.Aegis,
        i.LacShield,
        i.NeiShield,
        i.Knife,
        i.Dagger,
        i.CeramKnfe,
        i.LaserKnfe,
        i.LacnMace,
        i.BowGun,
        i.SonicGun,
        i.Shotgun,
        i.Cannon,
        i.LaserShot,
        i.PrsnClths,
    },
    levels=[
        Level(0, 16, 8, 15, 10, 14, 11, 8, 8, 8, [], ["FOI", "FORSA"]),
        Level(33, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(93, 6, 3, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(191, 7, 2, 3, 2, 2, 3, 3, 3, 2, [], ["EIJIA"]),
        Level(325, 6, 3, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(567, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(909, 7, 12, 18, 15, 12, 18, 17, 7, 7, [], ["RIMET", "GAJ"]),
        Level(1418, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(2172, 6, 2, 3, 2, 2, 3, 3, 3, 2, [], ["CONTE"]),
        Level(3290, 7, 3, 3, 2, 2, 3, 3, 2, 2, [], ["ZAN", "GIGAJ"]),
        Level(4925, 6, 2, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(7320, 6, 3, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(10829, 6, 2, 3, 2, 2, 3, 3, 3, 2, [], ["SAG"]),
        Level(15941, 7, 11, 18, 15, 12, 18, 17, 7, 7, [], ["GRA"]),
        Level(23391, 6, 3, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(34245, 6, 2, 3, 2, 2, 3, 3, 3, 4, [], []),
        Level(50057, 7, 3, 3, 2, 2, 3, 3, 2, 2, [], ["NAGAJ"]),
        Level(73024, 6, 2, 3, 2, 2, 3, 3, 3, 3, [], []),
        Level(97802, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(124938, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(155446, 7, 11, 18, 15, 12, 18, 17, 7, 7, [], ["GISAG"]),
        Level(189243, 6, 3, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(228736, 6, 2, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(273866, 6, 3, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(324664, 7, 2, 3, 2, 2, 3, 3, 3, 4, [], ["BROSE"]),
        Level(381196, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(443057, 6, 3, 3, 2, 2, 3, 3, 3, 3, [], []),
        Level(510737, 7, 11, 18, 15, 12, 18, 17, 9, 7, [], ["NASAG"]),
        Level(583897, 6, 3, 3, 2, 2, 3, 3, 2, 4, [], []),
        Level(662820, 6, 2, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(764558, 7, 2, 3, 2, 2, 3, 3, 2, 3, [], ["GIZAN"]),
        Level(863950, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(976264, 6, 2, 3, 2, 2, 3, 3, 2, 4, [], []),
        Level(1103178, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(1246592, 7, 11, 18, 15, 12, 18, 17, 9, 7, [], []),
        Level(1408649, 6, 3, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(1591773, 6, 2, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(1798703, 7, 2, 3, 2, 2, 3, 3, 2, 4, [], []),
        Level(2032536, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(2296776, 6, 2, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(2595345, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(2932740, 7, 11, 18, 15, 12, 18, 17, 9, 7, [], []),
        Level(3313996, 6, 2, 3, 2, 2, 3, 3, 2, 4, [], []),
        Level(3744816, 6, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(4231641, 6, 2, 3, 2, 2, 3, 3, 2, 3, [], []),
        Level(4781755, 7, 3, 3, 2, 2, 3, 3, 3, 2, [], []),
        Level(5403384, 6, 2, 3, 2, 2, 3, 3, 2, 2, [], []),
        Level(6105824, 6, 2, 3, 2, 2, 3, 3, 3, 4, [], []),
        Level(6899581, 7, 12, 18, 15, 12, 18, 17, 9, 7, [], []),
        Level(7796526, 3, 2, 3, 2, 2, 3, 3, 2, 3, [], []),
    ],
)
Shir = Char(
    "Shir",
    " Thief  ",
    profile="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

ALTHOUGH WELL-TO-DO,

SHE ENJOYS THE THRILL

OF STEALING.




▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
    portrait=Portrait(Pal.Shir, ART_PORTRAIT_SHIR, Win.ShirPortrait, 0x4102, MAPPING_PORTRAIT_SHIR),
    walk_sprite=WalkSprite(ART_WALK_AMY_SHIR, 0x23),
    battle_sprite=BattleSprite(ART_BATTLE_AMY_SHIR, MAPPING_BATTLE_SHIR, 0x20),
    join_text=TextRef(9, 37),
    rename_text=TextRef(9, 25),
    starting_items=[Equipped(i.Dagger), Equipped(i.CarbonSuit), Equipped(i.Shoes)],
    can_equip={
        i.Headgear,
        i.FiberGear,
        i.SilCrown,
        i.TitaniGear,
        i.JwlCrown,
        i.WindScarf,
        i.CarbonSuit,
        i.FiberCape,
        i.CrmcCape,
        i.CrystCape,
        i.NeiCape,
        i.Shoes,
        i.Boots,
        i.HirzaBoots,
        i.ShuneBoots,
        i.CrbnEmel,
        i.FiberEmel,
        i.MirEmel,
        i.CerEmel,
        i.TruthSlvs,
        i.NeiEmel,
        i.Knife,
        i.Dagger,
        i.CeramKnfe,
        i.LaserKnfe,
        i.LacDagger,
        i.PrsnClths,
    },
    levels=[
        Level(0, 13, 6, 18, 10, 15, 12, 18, 9, 9, [], ["FOI"]),
        Level(33, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(85, 5, 3, 7, 3, 6, 6, 6, 3, 4, [], []),
        Level(175, 10, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(298, 4, 2, 3, 2, 4, 2, 3, 5, 3, [], []),
        Level(519, 6, 2, 7, 3, 6, 6, 6, 4, 4, ["RYUKA"], []),
        Level(832, 8, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(1297, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(1987, 5, 3, 7, 3, 6, 6, 6, 3, 4, ["HINAS"], []),
        Level(3011, 10, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(4507, 2, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(6699, 8, 2, 7, 3, 6, 6, 6, 4, 4, ["RES"], ["RES"]),
        Level(9910, 8, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(14588, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(21406, 5, 3, 7, 3, 6, 6, 6, 3, 4, [], ["GIFOI"]),
        Level(31339, 10, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(45809, 2, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(66827, 8, 2, 7, 3, 6, 6, 6, 4, 4, [], ["ZAN"]),
        Level(89502, 8, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(114328, 4, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(142255, 8, 3, 7, 3, 6, 6, 6, 4, 4, [], []),
        Level(173184, 6, 2, 3, 2, 4, 2, 3, 5, 3, [], []),
        Level(209325, 2, 2, 3, 2, 4, 2, 3, 1, 3, [], []),
        Level(250626, 8, 2, 7, 3, 6, 6, 6, 4, 4, [], ["GRA"]),
        Level(297113, 8, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(348848, 4, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(405460, 6, 3, 7, 3, 6, 6, 6, 3, 4, [], ["GIZAN"]),
        Level(467397, 8, 2, 3, 2, 4, 2, 3, 4, 3, [], []),
        Level(534348, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(606574, 5, 2, 7, 3, 6, 6, 6, 4, 4, ["GIRES"], ["GIRES"]),
        Level(699679, 10, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(790637, 2, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(893419, 8, 3, 7, 3, 6, 6, 6, 3, 4, [], ["NAZAN"]),
        Level(1009564, 8, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(1140808, 3, 2, 3, 2, 4, 2, 3, 4, 3, [], []),
        Level(1289114, 5, 2, 7, 3, 6, 6, 6, 4, 4, [], ["GIGRA"]),
        Level(1456698, 10, 2, 4, 2, 4, 2, 3, 3, 3, [], []),
        Level(1646068, 4, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(1860058, 6, 3, 6, 3, 6, 6, 6, 3, 4, [], []),
        Level(2101866, 8, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(2375108, 5, 2, 3, 2, 4, 2, 3, 3, 3, [], []),
        Level(2683873, 10, 2, 7, 3, 6, 6, 6, 4, 4, [], []),
        Level(3032776, 3, 2, 3, 2, 4, 2, 3, 1, 3, [], []),
        Level(3427037, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(3872551, 5, 3, 7, 3, 6, 6, 6, 3, 4, [], ["NAGRA"]),
        Level(4375983, 10, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
        Level(4944862, 4, 2, 3, 2, 4, 2, 3, 1, 3, [], []),
        Level(5587694, 4, 2, 7, 3, 6, 6, 6, 4, 4, [], []),
        Level(6314094, 10, 2, 3, 2, 4, 2, 3, 1, 3, [], []),
        Level(7134926, 3, 2, 3, 2, 4, 2, 3, 2, 3, [], []),
    ],
)

vanilla_characters = [Rolf, Nei, Rudo, Amy, Hugh, Anna, Kain, Shir]


character_names = [char.name for char in vanilla_characters]
