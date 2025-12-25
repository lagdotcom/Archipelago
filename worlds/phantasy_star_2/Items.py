from enum import IntEnum, IntFlag
from operator import attrgetter
from typing import Optional

from BaseClasses import ItemClassification as IC

from .Constants import jet_scooter_flag, spaceship_flag
from .Data import ItemName as I, TechID
from .Data.Types import EquipSlot as S
from .laglib import IntSpan
from .Messages import translate_message


class ItemType(IntEnum):
    Garbage = 0
    Item = 1
    Money = 2
    Flag = 3
    FlagAsItem = 4


class ItemFlags(IntFlag):
    NONE = 0
    Map = 0x8
    Battle = 0x10
    Store = 0x20
    RevertToAttack = 0x40
    Sell = 0x80


class ItemData:
    id: int
    type: ItemType
    name: str
    classification: IC
    code: Optional[int] = None
    slot: S = S.NONE
    meseta: Optional[int] = None
    ram_flag: Optional[IntSpan] = None
    ram_value: int = 1
    price: int = 0
    flags: ItemFlags = ItemFlags.NONE
    at: int = 0
    df: int = 0
    ag: int = 0
    use_tech: int = 0

    def __init__(
        self,
        id: int,
        type: ItemType,
        name: str,
        classification: IC,
        code: Optional[int] = None,
        slot: S = S.NONE,
        meseta: Optional[int] = None,
        ram_flag: Optional[IntSpan] = None,
        ram_value: int = 1,
        price: int = 0,
        flags: ItemFlags = ItemFlags.NONE,
        at: int = 0,
        df: int = 0,
        ag: int = 0,
        use_tech: int = 0,
    ):
        self.id = id
        self.type = type
        self.name = name
        self.classification = classification
        self.code = code
        self.slot = slot
        self.meseta = meseta
        self.ram_flag = ram_flag
        self.ram_value = ram_value
        self.price = price
        self.flags = flags
        self.at = at
        self.df = df
        self.ag = ag  # TODO write this to ROM
        self.use_tech = use_tech

    @property
    def code_as_int(self):
        if self.code is None:
            return -1
        return self.code

    def get_chest_bytes(self):
        raw: Optional[int] = None
        if self.name == I.Garbage:
            raw = 0
        elif self.meseta is not None:
            if self.meseta > 0x7FFF:
                raise Exception(f"meseta amount {self.meseta} too high")
            raw = self.meseta
        elif self.code is not None:
            raw = self.code | 0x8000
        if raw is None:
            raise Exception(f"Item {self.name} cannot be placed in chest!")
        return raw.to_bytes(2, "big")

    def get_data_bytes(self, char_mask: int):
        if len(self.name) > 10:
            raise Exception(f"item {self.name} has name too long (max 10)")
        if self.price > 0xFFFF:
            raise Exception(f"item {self.name} has price over 65536")
        if self.use_tech and not ItemFlags.Battle in self.flags:
            raise Exception(f"item {self.name} has a tech but not ItemFlags.Battle")
        if self.use_tech == 0 and ItemFlags.Battle in self.flags:
            raise Exception(f"item {self.name} has ItemFlags.Battle but no tech")
        name = self.name
        padding = 10 - len(name)
        if padding > 0:
            padding -= 1
            name += "<END>"
        if padding > 0:
            name += " " * padding
        return (
            translate_message(name)
            + self.price.to_bytes(2, "big")
            + bytes([self.slot.value | self.flags.value, char_mask, self.at, self.df])
        )


unused_items = [
    ItemData(452_1_000, ItemType.Item, "", IC.filler, 0),
    ItemData(
        452_1_126,
        ItemType.Item,
        "T",
        IC.filler,
        0x7E,
        flags=ItemFlags.Map
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=62000,
    ),
    ItemData(
        452_1_127,
        ItemType.Item,
        "H",
        IC.filler,
        0x7F,
        flags=ItemFlags.Map
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=46000,
    ),
]

key_items = [
    ItemData(
        452_1_001,
        ItemType.Item,
        I.SmallKey,
        IC.progression,
        0x1,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_002,
        ItemType.Item,
        I.Dynamite,
        IC.progression,
        0x2,
        flags=ItemFlags.Map | ItemFlags.RevertToAttack,
    ),
    ItemData(
        452_1_003,
        ItemType.Item,
        I.KeyTube,
        IC.progression,
        0x3,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_004,
        ItemType.Item,
        I.MarueraGum,
        IC.progression,
        0x4,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_005,
        ItemType.Item,
        I.GreenCard,
        IC.progression,
        0x5,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_006,
        ItemType.Item,
        I.BlueCard,
        IC.progression,
        0x6,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_007,
        ItemType.Item,
        I.YellowCard,
        IC.progression,
        0x7,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_008,
        ItemType.Item,
        I.RedCard,
        IC.progression,
        0x8,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_009, ItemType.Item, I.Letter, IC.progression, 0x9, flags=ItemFlags.Map
    ),
    ItemData(
        452_1_010, ItemType.Item, I.Recorder, IC.progression, 0xA, flags=ItemFlags.Map
    ),
    ItemData(
        452_1_011,
        ItemType.Item,
        I.MarueraLeaf,
        IC.progression,
        0xB,
        flags=ItemFlags.Map | ItemFlags.Store,
    ),
    ItemData(
        452_1_013, ItemType.Item, I.Prism, IC.progression, 0xD, flags=ItemFlags.Map
    ),
    ItemData(
        452_1_039,
        ItemType.Item,
        I.NeiMet,
        IC.progression,
        0x27,
        S.Head,
        flags=ItemFlags.Store,
        df=50,
    ),
    ItemData(
        452_1_040,
        ItemType.Item,
        I.NeiCrown,
        IC.progression,
        0x28,
        S.Head,
        flags=ItemFlags.Store,
        df=48,
    ),
    ItemData(
        452_1_061,
        ItemType.Item,
        I.NeiArmor,
        IC.progression,
        0x3D,
        S.Body,
        flags=ItemFlags.Store,
        df=95,
    ),
    ItemData(
        452_1_062,
        ItemType.Item,
        I.NeiCape,
        IC.progression,
        0x3E,
        S.Body,
        flags=ItemFlags.Store,
        df=88,
    ),
    ItemData(
        452_1_084,
        ItemType.Item,
        I.NeiShield,
        IC.progression,
        0x54,
        S.OneHand,
        flags=ItemFlags.Store,
        df=95,
    ),
    ItemData(
        452_1_085,
        ItemType.Item,
        I.NeiEmel,
        IC.progression,
        0x55,
        S.OneHand,
        flags=ItemFlags.Store,
        df=118,
    ),
    # this isn't actually needed, but good luck beating Dark Force without it
    ItemData(
        452_1_108,
        ItemType.Item,
        I.NeiSword,
        IC.progression,
        0x6C,
        S.TwoHand,
        flags=ItemFlags.Map | ItemFlags.Store,
        at=75,
        df=24,
    ),
    ItemData(
        452_1_109,
        ItemType.Item,
        I.NeiSlasher,
        IC.progression,
        0x6D,
        S.OneHand,
        flags=ItemFlags.Store,
        at=60,
    ),
    ItemData(
        452_1_122,
        ItemType.Item,
        I.NeiShot,
        IC.progression,
        0x7A,
        S.TwoHand,
        flags=ItemFlags.Store,
        at=60,
    ),
    ItemData(
        452_1_124, ItemType.Item, I.Teim, IC.progression, 0x7C, flags=ItemFlags.Map
    ),
]

flag_items = [
    ItemData(452_9_000, ItemType.Flag, I.MusikFlag, IC.progression),
    ItemData(
        452_9_001,
        ItemType.FlagAsItem,
        I.JetScooterFlag,
        IC.progression,
        0xE1,
        ram_flag=jet_scooter_flag,
        ram_value=2,
    ),
    ItemData(452_9_002, ItemType.Flag, I.NeifirstFlag, IC.progression),
    ItemData(452_9_003, ItemType.Flag, I.RedDamFlag, IC.progression),
    ItemData(452_9_004, ItemType.Flag, I.YellowDamFlag, IC.progression),
    ItemData(452_9_005, ItemType.Flag, I.BlueDamFlag, IC.progression),
    ItemData(452_9_006, ItemType.Flag, I.GreenDamFlag, IC.progression),
    ItemData(
        452_9_007,
        ItemType.FlagAsItem,
        I.SpaceshipFlag,
        IC.progression,
        0xE2,
        ram_flag=spaceship_flag,
    ),
    ItemData(452_9_008, ItemType.Flag, I.WinTheGameFlag, IC.progression),
]


required_items = key_items + flag_items


unique_useful_items = [
    ItemData(
        452_1_042,
        ItemType.Item,
        I.MogicCap,
        IC.useful,
        0x2A,
        S.Head,
        flags=ItemFlags.Store,
        df=2,
    ),
    ItemData(
        452_1_125,
        ItemType.Item,
        I.Visiphone,
        IC.useful,
        0x7D,
        flags=ItemFlags.Map | ItemFlags.Store | ItemFlags.Sell,
        price=3000,
    ),
]

equipment_items = [
    ItemData(
        452_1_023,
        ItemType.Item,
        I.Headgear,
        IC.useful,
        0x17,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=3,
        price=120,
    ),
    ItemData(
        452_1_024,
        ItemType.Item,
        I.Ribbon,
        IC.useful,
        0x18,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=3,
        price=80,
    ),
    ItemData(
        452_1_025,
        ItemType.Item,
        I.FiberGear,
        IC.useful,
        0x19,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=8,
        price=430,
    ),
    ItemData(
        452_1_026,
        ItemType.Item,
        I.SilRibbon,
        IC.useful,
        0x1A,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=12,
        price=380,
    ),
    ItemData(
        452_1_027,
        ItemType.Item,
        I.SilCrown,
        IC.useful,
        0x1B,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=14,
        price=470,
    ),
    ItemData(
        452_1_028,
        ItemType.Item,
        I.TitaniGear,
        IC.useful,
        0x1C,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=14,
        price=1400,
    ),
    ItemData(
        452_1_029,
        ItemType.Item,
        I.TitaniMet,
        IC.useful,
        0x1D,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=16,
        price=3700,
    ),
    ItemData(
        452_1_030,
        ItemType.Item,
        I.JwlCrown,
        IC.useful,
        0x1E,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=17,
        price=4600,
    ),
    ItemData(
        452_1_031,
        ItemType.Item,
        I.JwlRibbon,
        IC.useful,
        0x1F,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=21,
        price=4700,
    ),
    ItemData(
        452_1_032,
        ItemType.Item,
        I.CresceGear,
        IC.useful,
        0x20,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=14,
        price=280,
        use_tech=TechID.GIRES,
    ),
    ItemData(
        452_1_033,
        ItemType.Item,
        I.SnowCrown,
        IC.useful,
        0x21,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=17,
        price=490,
        use_tech=TechID.DEBAN,
    ),
    ItemData(
        452_1_034,
        ItemType.Item,
        I.WindScarf,
        IC.useful,
        0x22,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=17,
        price=120,
        use_tech=TechID.ZAN,
    ),
    ItemData(
        452_1_035,
        ItemType.Item,
        I.ColorScarf,
        IC.useful,
        0x23,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=17,
        price=130,
        use_tech=TechID.SANER,
    ),
    ItemData(
        452_1_036,
        ItemType.Item,
        I.StormGear,
        IC.useful,
        0x24,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=16,
        price=630,
        use_tech=TechID.GIZAN,
    ),
    ItemData(
        452_1_037,
        ItemType.Item,
        I.Laconigear,
        IC.useful,
        0x25,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=27,
        price=28000,
    ),
    ItemData(
        452_1_038,
        ItemType.Item,
        I.LaconiaMet,
        IC.useful,
        0x26,
        S.Head,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=29,
        price=29000,
    ),
    ItemData(
        452_1_043,
        ItemType.Item,
        I.CarbonSuit,
        IC.useful,
        0x2B,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=4,
        price=128,
    ),
    ItemData(
        452_1_044,
        ItemType.Item,
        I.CarbonVest,
        IC.useful,
        0x2C,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=4,
        price=120,
    ),
    ItemData(
        452_1_045,
        ItemType.Item,
        I.FiberCoat,
        IC.useful,
        0x2D,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=8,
        price=300,
    ),
    ItemData(
        452_1_046,
        ItemType.Item,
        I.FiberCape,
        IC.useful,
        0x2E,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=8,
        price=420,
    ),
    ItemData(
        452_1_047,
        ItemType.Item,
        I.FiberVest,
        IC.useful,
        0x2F,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=6,
        price=280,
    ),
    ItemData(
        452_1_048,
        ItemType.Item,
        I.TtnmArmor,
        IC.useful,
        0x30,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=24,
        price=5600,
    ),
    ItemData(
        452_1_049,
        ItemType.Item,
        I.TtnmCape,
        IC.useful,
        0x31,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=28,
        price=6300,
    ),
    ItemData(
        452_1_050,
        ItemType.Item,
        I.TtnmChest,
        IC.useful,
        0x32,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=21,
        price=5400,
    ),
    ItemData(
        452_1_051,
        ItemType.Item,
        I.CrmcArmor,
        IC.useful,
        0x33,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=48,
        price=11700,
    ),
    ItemData(
        452_1_052,
        ItemType.Item,
        I.CrmcCape,
        IC.useful,
        0x34,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=56,
        price=12400,
    ),
    ItemData(
        452_1_053,
        ItemType.Item,
        I.CrmcChest,
        IC.useful,
        0x35,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=46,
        price=10000,
    ),
    ItemData(
        452_1_054,
        ItemType.Item,
        I.AmberRobe,
        IC.useful,
        0x36,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=20,
        price=170,
        use_tech=TechID.GIRES,
    ),
    ItemData(
        452_1_055,
        ItemType.Item,
        I.Crystanish,
        IC.useful,
        0x37,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=60,
        price=630,
        use_tech=TechID.GRA,
    ),
    ItemData(
        452_1_056,
        ItemType.Item,
        I.CrystCape,
        IC.useful,
        0x38,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=62,
        price=840,
        use_tech=TechID.GRA,
    ),
    ItemData(
        452_1_057,
        ItemType.Item,
        I.CrystChest,
        IC.useful,
        0x39,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=60,
        price=670,
        use_tech=TechID.GRA,
    ),
    ItemData(
        452_1_058,
        ItemType.Item,
        I.Laconinish,
        IC.useful,
        0x3A,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=65,
        price=35000,
    ),
    ItemData(
        452_1_059,
        ItemType.Item,
        I.LaconCape,
        IC.useful,
        0x3B,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=70,
        price=36000,
    ),
    ItemData(
        452_1_060,
        ItemType.Item,
        I.LaconChest,
        IC.useful,
        0x3C,
        S.Body,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=80,
        price=28000,
    ),
    ItemData(
        452_1_063,
        ItemType.Item,
        I.Shoes,
        IC.useful,
        0x3F,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=3,
        ag=2,
        price=240,
    ),
    ItemData(
        452_1_064,
        ItemType.Item,
        I.Sandals,
        IC.useful,
        0x40,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=3,
        ag=3,
        price=180,
    ),
    ItemData(
        452_1_065,
        ItemType.Item,
        I.Boots,
        IC.useful,
        0x41,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=7,
        ag=3,
        price=1000,
    ),
    ItemData(
        452_1_066,
        ItemType.Item,
        I.KnifeBoots,
        IC.useful,
        0x42,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=7,
        df=7,
        ag=5,
        price=4200,
    ),
    ItemData(
        452_1_067,
        ItemType.Item,
        I.LongBoots,
        IC.useful,
        0x43,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=5,
        df=7,
        ag=7,
        price=6800,
    ),
    ItemData(
        452_1_068,
        ItemType.Item,
        I.HirzaBoots,
        IC.useful,
        0x44,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=7,
        ag=7,
        price=9800,
    ),
    ItemData(
        452_1_069,
        ItemType.Item,
        I.ShuneBoots,
        IC.useful,
        0x45,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=7,
        ag=10,
        price=7500,
    ),
    ItemData(
        452_1_070,
        ItemType.Item,
        I.GardaBoots,
        IC.useful,
        0x46,
        S.Feet,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=15,
        ag=8,
        price=12400,
    ),
    ItemData(
        452_1_071,
        ItemType.Item,
        I.CrbnShield,
        IC.useful,
        0x47,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=8,
        price=540,
    ),
    ItemData(
        452_1_072,
        ItemType.Item,
        I.CrbnEmel,
        IC.useful,
        0x48,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=7,
        price=420,
    ),
    ItemData(
        452_1_073,
        ItemType.Item,
        I.FibrShild,
        IC.useful,
        0x49,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=15,
        price=1200,
    ),
    ItemData(
        452_1_074,
        ItemType.Item,
        I.FiberEmel,
        IC.useful,
        0x4A,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=17,
        price=1360,
    ),
    ItemData(
        452_1_075,
        ItemType.Item,
        I.MirShield,
        IC.useful,
        0x4B,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=32,
        price=4800,
    ),
    ItemData(
        452_1_076,
        ItemType.Item,
        I.MirEmel,
        IC.useful,
        0x4C,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=30,
        price=5120,
    ),
    ItemData(
        452_1_077,
        ItemType.Item,
        I.CerShield,
        IC.useful,
        0x4D,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=39,
        price=8300,
    ),
    ItemData(
        452_1_078,
        ItemType.Item,
        I.CerEmel,
        IC.useful,
        0x4E,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=40,
        price=9700,
    ),
    ItemData(
        452_1_079,
        ItemType.Item,
        I.Aegis,
        IC.useful,
        0x4F,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=32,
        price=1200,
        use_tech=TechID.GIRES,
    ),
    ItemData(
        452_1_080,
        ItemType.Item,
        I.GrSleeves,
        IC.useful,
        0x50,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=63,
        price=840,
        use_tech=TechID.SHINB,
    ),
    ItemData(
        452_1_081,
        ItemType.Item,
        I.TruthSlvs,
        IC.useful,
        0x51,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        df=59,
        price=720,
        use_tech=TechID.GIRES,
    ),
    ItemData(
        452_1_082,
        ItemType.Item,
        I.LaconEmel,
        IC.useful,
        0x52,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=68,
        price=12000,
    ),
    ItemData(
        452_1_083,
        ItemType.Item,
        I.LacShield,
        IC.useful,
        0x53,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        df=85,
        price=13000,
    ),
    ItemData(
        452_1_086,
        ItemType.Item,
        I.Knife,
        IC.useful,
        0x56,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=5,
        price=100,
    ),
    ItemData(
        452_1_087,
        ItemType.Item,
        I.Dagger,
        IC.useful,
        0x57,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=8,
        df=1,
        price=200,
    ),
    ItemData(
        452_1_088,
        ItemType.Item,
        I.Scalpel,
        IC.useful,
        0x58,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=7,
        price=180,
    ),
    ItemData(
        452_1_089,
        ItemType.Item,
        I.SteelBar,
        IC.useful,
        0x59,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=7,
        df=2,
        price=80,
    ),
    ItemData(
        452_1_090,
        ItemType.Item,
        I.Boomerang,
        IC.useful,
        0x5A,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=12,
        price=480,
    ),
    ItemData(
        452_1_091,
        ItemType.Item,
        I.Slasher,
        IC.useful,
        0x5B,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=17,
        price=2000,
    ),
    ItemData(
        452_1_092,
        ItemType.Item,
        I.Sword,
        IC.useful,
        0x5C,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=18,
        df=4,
        price=1200,
    ),
    ItemData(
        452_1_093,
        ItemType.Item,
        I.Whip,
        IC.useful,
        0x5D,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=20,
        df=2,
        price=1400,
    ),
    ItemData(
        452_1_094,
        ItemType.Item,
        I.CeramSwrd,
        IC.useful,
        0x5E,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=30,
        df=5,
        price=3200,
    ),
    ItemData(
        452_1_095,
        ItemType.Item,
        I.CeramKnfe,
        IC.useful,
        0x5F,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=20,
        df=3,
        price=2800,
    ),
    ItemData(
        452_1_096,
        ItemType.Item,
        I.CeramBar,
        IC.useful,
        0x60,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=27,
        df=2,
        price=1200,
    ),
    ItemData(
        452_1_097,
        ItemType.Item,
        I.LasrSlshr,
        IC.useful,
        0x61,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=30,
        price=6700,
    ),
    ItemData(
        452_1_098,
        ItemType.Item,
        I.LasrSword,
        IC.useful,
        0x62,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=50,
        df=9,
        price=5400,
    ),
    ItemData(
        452_1_099,
        ItemType.Item,
        I.LaserBar,
        IC.useful,
        0x63,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=38,
        df=3,
        price=3100,
    ),
    ItemData(
        452_1_100,
        ItemType.Item,
        I.LaserKnfe,
        IC.useful,
        0x64,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=28,
        df=5,
        price=4400,
    ),
    ItemData(
        452_1_101,
        ItemType.Item,
        I.SwdOfAng,
        IC.useful,
        0x65,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=58,
        price=280,
    ),
    ItemData(
        452_1_102,
        ItemType.Item,
        I.FireSlshr,
        IC.useful,
        0x66,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=36,
        price=340,
    ),
    ItemData(
        452_1_103,
        ItemType.Item,
        I.FireStaff,
        IC.useful,
        0x67,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell | ItemFlags.Battle,
        at=32,
        df=11,
        price=670,
        use_tech=TechID.FOI,
    ),
    ItemData(
        452_1_104,
        ItemType.Item,
        I.LacnMace,
        IC.useful,
        0x68,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=40,
        df=8,
        price=16800,
    ),
    ItemData(
        452_1_105,
        ItemType.Item,
        I.LacDagger,
        IC.useful,
        0x69,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=4,
        df=22,
        price=18400,
    ),
    ItemData(
        452_1_106,
        ItemType.Item,
        I.ACSlashr,
        IC.useful,
        0x6A,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=42,
        price=24000,
    ),
    ItemData(
        452_1_107,
        ItemType.Item,
        I.LacSword,
        IC.useful,
        0x6B,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=62,
        df=7,
        price=22000,
    ),
    ItemData(
        452_1_110,
        ItemType.Item,
        I.BowGun,
        IC.useful,
        0x6E,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=8,
        price=300,
    ),
    ItemData(
        452_1_111,
        ItemType.Item,
        I.SonicGun,
        IC.useful,
        0x6F,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=17,
        price=640,
    ),
    ItemData(
        452_1_112,
        ItemType.Item,
        I.Shotgun,
        IC.useful,
        0x70,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=10,
        price=800,
    ),
    ItemData(
        452_1_113,
        ItemType.Item,
        I.SilentShot,
        IC.useful,
        0x71,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=10,
        price=920,
    ),
    ItemData(
        452_1_114,
        ItemType.Item,
        I.PoisonShot,
        IC.useful,
        0x72,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=15,
        price=1700,
    ),
    ItemData(
        452_1_115,
        ItemType.Item,
        I.AcidShot,
        IC.useful,
        0x73,
        S.OneHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=25,
        price=4800,
    ),
    ItemData(
        452_1_116,
        ItemType.Item,
        I.Cannon,
        IC.useful,
        0x74,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=18,
        price=2200,
    ),
    ItemData(
        452_1_117,
        ItemType.Item,
        I.Vulcan,
        IC.useful,
        0x75,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=28,
        price=12600,
    ),
    ItemData(
        452_1_118,
        ItemType.Item,
        I.LaserShot,
        IC.useful,
        0x76,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=20,
        price=6200,
    ),
    ItemData(
        452_1_119,
        ItemType.Item,
        I.LsrCannon,
        IC.useful,
        0x77,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=30,
        price=20000,
    ),
    ItemData(
        452_1_120,
        ItemType.Item,
        I.PlsCannon,
        IC.useful,
        0x78,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=35,
        price=32000,
    ),
    ItemData(
        452_1_121,
        ItemType.Item,
        I.PulseVlcn,
        IC.useful,
        0x79,
        S.TwoHand,
        flags=ItemFlags.Store | ItemFlags.Sell,
        at=38,
        price=48000,
    ),
]

useful_items = unique_useful_items + equipment_items
useful_item_names = [item.name for item in useful_items]

consumable_items = [
    ItemData(
        452_1_014,
        ItemType.Item,
        I.Telepipe,
        IC.filler,
        0xE,
        flags=ItemFlags.Map
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=130,
    ),
    ItemData(
        452_1_015,
        ItemType.Item,
        I.Escapipe,
        IC.filler,
        0xF,
        flags=ItemFlags.Map
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=70,
    ),
    ItemData(
        452_1_016,
        ItemType.Item,
        I.Hidapipe,
        IC.filler,
        0x10,
        flags=ItemFlags.Map
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=280,
    ),
    ItemData(
        452_1_017,
        ItemType.Item,
        I.Monomate,
        IC.filler,
        0x11,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=20,
        use_tech=TechID.RES,
    ),
    ItemData(
        452_1_018,
        ItemType.Item,
        I.Dimate,
        IC.filler,
        0x12,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=50,
        use_tech=TechID.GIRES,
    ),
    ItemData(
        452_1_019,
        ItemType.Item,
        I.Trimate,
        IC.filler,
        0x13,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=160,
        use_tech=TechID.NARES,
    ),
    ItemData(
        452_1_020,
        ItemType.Item,
        I.Antidote,
        IC.filler,
        0x14,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=10,
        use_tech=TechID.ANTI,
    ),
    ItemData(
        452_1_021,
        ItemType.Item,
        I.StarMist,
        IC.filler,
        0x15,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=1000,
        use_tech=TechID.NASAR,
    ),
    ItemData(
        452_1_022,
        ItemType.Item,
        I.MoonDew,
        IC.filler,
        0x16,
        flags=ItemFlags.Map
        | ItemFlags.Battle
        | ItemFlags.Store
        | ItemFlags.RevertToAttack
        | ItemFlags.Sell,
        price=12000,
        use_tech=TechID.REVER,
    ),
]

junk_items = [
    ItemData(
        452_1_012, ItemType.Item, I.PlasmaRing, IC.filler, 0xC, flags=ItemFlags.Map
    ),
    ItemData(
        452_1_041,
        ItemType.Item,
        I.MagicCap,
        IC.filler,
        0x29,
        S.Head,
        flags=ItemFlags.Store,
        df=2,
    ),
    ItemData(
        452_1_123, ItemType.Item, I.PrsnClths, IC.filler, 0x7B, S.Body, df=2, price=100
    ),
    ItemData(452_2_000, ItemType.Garbage, I.Garbage, IC.filler),
]

meseta_items = [
    ItemData(452_2_001, ItemType.Money, I.Meseta(20), IC.filler, meseta=20),
    ItemData(452_2_002, ItemType.Money, I.Meseta(40), IC.filler, meseta=40),
    ItemData(452_2_003, ItemType.Money, I.Meseta(60), IC.filler, meseta=60),
    ItemData(452_2_004, ItemType.Money, I.Meseta(100), IC.filler, meseta=100),
    ItemData(452_2_005, ItemType.Money, I.Meseta(150), IC.filler, meseta=150),
    ItemData(452_2_006, ItemType.Money, I.Meseta(200), IC.filler, meseta=200),
    ItemData(452_2_007, ItemType.Money, I.Meseta(5600), IC.filler, meseta=5600),
    ItemData(452_2_008, ItemType.Money, I.Meseta(6400), IC.filler, meseta=6400),
    ItemData(452_2_009, ItemType.Money, I.Meseta(7800), IC.filler, meseta=7800),
    ItemData(452_2_010, ItemType.Money, I.Meseta(8600), IC.filler, meseta=8600),
    ItemData(452_2_011, ItemType.Money, I.Meseta(12000), IC.filler, meseta=12000),
    ItemData(452_2_012, ItemType.Money, I.Meseta(15000), IC.filler, meseta=15000),
    ItemData(452_2_013, ItemType.Money, I.Meseta(18000), IC.filler, meseta=18000),
]

filler_items = consumable_items + junk_items + meseta_items
filler_item_names = [item.name for item in filler_items]

item_name_groups = {
    "Key Items": {item.name for item in key_items},
    "Unique and Useful": {item.name for item in unique_useful_items},
    "Equipment": {item.name for item in equipment_items},
    "Consumables": {item.name for item in consumable_items},
    "Junk": {item.name for item in junk_items},
    "Quest Flags": {item.name for item in flag_items},
}

all_items = required_items + useful_items + filler_items
items_by_name = {item.name: item for item in all_items}
items_by_id = {item.id: item for item in all_items}

items_with_codes = sorted(
    [
        item
        for item in all_items + unused_items
        if item.type == ItemType.Item and item.code is not None
    ],
    key=attrgetter("code_as_int"),
)
