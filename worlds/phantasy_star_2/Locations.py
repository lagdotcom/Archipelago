from typing import NamedTuple, Optional

from .Data import Area as A, Item as I


class LocationData(NamedTuple):
    id: int
    region_name: str
    name: str
    chest_index: Optional[int] = None
    rom_location: Optional[int] = None
    fixed_item: Optional[str] = None
    ram_location: Optional[int] = None
    ram_check: Optional[int] = None
    additional_flag_requirement: Optional[int] = None
    required_items: Optional[set[str]] = None

    def fix(self, fixed_item: str, ram_location: int, ram_check: int = 1):
        return LocationData(self.id, self.region_name, self.name, self.chest_index, self.rom_location, fixed_item, ram_location, ram_check, self.additional_flag_requirement, self.required_items)

    def add_flag(self, additional_flag_requirement: int):
        return LocationData(self.id, self.region_name, self.name, self.chest_index, self.rom_location, self.fixed_item, self.ram_location, self.ram_check, additional_flag_requirement, self.required_items)

    def add_items(self, required_items: set[str]):
        return LocationData(self.id, self.region_name, self.name, self.chest_index, self.rom_location, self.fixed_item, self.ram_location, self.ram_check, self.additional_flag_requirement, required_items)


skure_locations = [
    LocationData(452_00_01, A.Dezolis, 'Skure - 15000 meseta', 0x1),
    LocationData(452_00_02, A.Dezolis, 'Skure - MogicCap', 0x2),
    LocationData(452_00_03, A.Dezolis, 'Skure - 18000 meseta', 0x3),
    LocationData(452_00_04, A.Dezolis, 'Skure - MagicCap', 0x4),
    LocationData(452_00_05, A.Dezolis, 'Skure - 7800 meseta', 0x5),
    LocationData(452_00_06, A.Dezolis, 'Skure - LaconChest', 0x6),
    LocationData(452_00_07, A.Dezolis, 'Skure - 5600 meseta', 0x7),
    LocationData(452_00_08, A.Dezolis, 'Skure - GardaBoots', 0x8),
    LocationData(452_00_09, A.Dezolis, 'Skure - 8600 meseta', 0x9),
    LocationData(452_00_10, A.Dezolis, 'Skure - MagicCap 2', 0xA),
    LocationData(452_00_11, A.Dezolis, 'Skure - 12000 meseta', 0xB),
    LocationData(452_00_12, A.Dezolis, 'Skure - 6400 meseta', 0xC),
]

esper_mansion_locations = [
    LocationData(452_00_14, A.Dezolis, 'Esper Mansion - Prism',
                 0xE).add_flag(0xc743),
    LocationData(452_00_15, A.Dezolis, 'Esper Mansion - NeiSword',
                 0xF).add_flag(0xc744).add_items({I.NeiArmor, I.NeiCape, I.NeiCrown, I.NeiEmel, I.NeiMet, I.NeiShield, I.NeiShot, I.NeiSlasher}),
]

shure_locations = [
    LocationData(452_00_16, A.ShureLockedChests,
                 'Shure Locked - Monomate', 0x10),
    LocationData(452_00_17, A.ShureLockedChests,
                 'Shure Locked - 150 meseta', 0x11),
    LocationData(452_00_18, A.ShureLockedChests,
                 'Shure Locked - Dynamite', 0x12),
    LocationData(452_00_19, A.ShureLockedChests,
                 'Shure Locked - Dynamite 2', 0x13),
    LocationData(452_00_20, A.Shure, 'Shure - 40 meseta', 0x14),
    LocationData(452_00_21, A.Shure, 'Shure - Dimate', 0x15),
    LocationData(452_00_22, A.Shure, 'Shure - Headgear', 0x16),
    LocationData(452_00_23, A.Shure, 'Shure - 200 meseta', 0x17),
    LocationData(452_00_24, A.Shure, 'Shure - SilRibbon', 0x18),

    LocationData(452_01_01, A.Shure, 'Shure - Small Key', None, 0xdbe3),
    LocationData(452_01_02, A.Shure, 'Shure - Letter', None, 0xdbf3),
]

nido_locations = [
    LocationData(452_00_25, A.Nido, 'Nido - 20 meseta', 0x19),
    LocationData(452_00_26, A.Nido, 'Nido - 100 meseta', 0x1A),
    LocationData(452_00_27, A.Nido, 'Nido - Dimate', 0x1B),
    LocationData(452_00_28, A.Nido, 'Nido - Trimate', 0x1C),
    LocationData(452_00_29, A.Nido, 'Nido - 60 meseta', 0x1D),

    LocationData(452_01_10, A.Nido, 'Nido - Teim', None,
                 0xdc6d).add_items({I.Letter}),
]

roron_locations = [
    LocationData(452_00_30, A.Roron, 'Roron - Garbage', 0x1E),
    LocationData(452_00_31, A.Roron, 'Roron - Garbage 2', 0x1F),
    LocationData(452_00_32, A.Roron, 'Roron - CeramBar', 0x20),
    LocationData(452_00_33, A.Roron, 'Roron - Garbage 3', 0x21),
    LocationData(452_00_34, A.Roron, 'Roron - Cannon', 0x22),
    LocationData(452_00_35, A.Roron, 'Roron - Garbage 4', 0x23),

    LocationData(452_02_00, A.Roron, 'Roron - Jet Scooter Guy').fix(
        I.JetScooterFlag, 0xc716),
]

yellow_dam_locations = [
    LocationData(452_00_36, A.YellowDam, 'Yellow Dam - Escapipe', 0x24),
    LocationData(452_00_37, A.YellowDam, 'Yellow Dam - Crystanish', 0x25),
    LocationData(452_00_38, A.YellowDam, 'Yellow Dam - CrystCape', 0x26),
    LocationData(452_00_39, A.YellowDam, 'Yellow Dam - CrystChest', 0x27),
    LocationData(452_00_40, A.YellowDam, 'Yellow Dam - AmberRobe', 0x28),

    LocationData(452_02_01, A.YellowDam, 'Yellow Dam - Console').fix(
        I.YellowDamFlag, 0xc731),
]

red_dam_locations = [
    LocationData(452_00_41, A.RedDam, 'Red Dam - SwdOfAnger', 0x29),
    LocationData(452_00_42, A.RedDam, 'Red Dam - FireSlshr', 0x2A),
    LocationData(452_00_43, A.RedDam, 'Red Dam - FireStaff', 0x2B),

    LocationData(452_02_02, A.RedDam, 'Red Dam - Console').fix(
        I.RedDamFlag, 0xc733),
]

blue_dam_locations = [
    LocationData(452_00_44, A.BlueDam, 'Blue Dam - Antidote', 0x2C),
    LocationData(452_00_45, A.BlueDam, 'Blue Dam - CresceGear', 0x2D),
    LocationData(452_00_46, A.BlueDam, 'Blue Dam - SnowCrown', 0x2E),
    LocationData(452_00_47, A.BlueDam, 'Blue Dam - StarMist', 0x2F),
    LocationData(452_00_48, A.BlueDam, 'Blue Dam - WindScarf', 0x30),
    LocationData(452_00_49, A.BlueDam, 'Blue Dam - ColorScarf', 0x31),
    LocationData(452_00_50, A.BlueDam, 'Blue Dam - Trimate', 0x32),
    LocationData(452_00_51, A.BlueDam, 'Blue Dam - StormGear', 0x33),

    LocationData(452_02_03, A.BlueDam, 'Blue Dam - Console').fix(
        I.BlueDamFlag, 0xc72f),
]

green_dam_locations = [
    LocationData(452_00_52, A.GreenDam, 'Green Dam - StarMist', 0x34),
    LocationData(452_00_53, A.GreenDam, 'Green Dam - Aegis', 0x35),
    LocationData(452_00_54, A.GreenDam, 'Green Dam - Telepipe', 0x36),
    LocationData(452_00_55, A.GreenDam, 'Green Dam - GrSleeves', 0x37),
    LocationData(452_00_56, A.GreenDam, 'Green Dam - TruthSlvs', 0x38),

    LocationData(452_02_04, A.GreenDam, 'Green Dam - Console').fix(
        I.GreenDamFlag, 0xc72d),
]

bio_systems_lab_locations = [
    LocationData(452_00_57, A.BioSystemsLab,
                 'Bio-Systems Lab - Trimate', 0x39),
    LocationData(452_00_58, A.BioSystemsLab,
                 'Bio-Systems Lab - Antidote', 0x3A),
    LocationData(452_00_59, A.BioSystemsLab,
                 'Bio-Systems Lab - PoisonShot', 0x3B),
    LocationData(452_00_60, A.BioSystemsLab,
                 'Bio-Systems Lab - Antidote2', 0x3C),
    LocationData(452_00_61, A.BioSystemsLab,
                 'Bio-Systems Lab - Scalpel', 0x3D),
    LocationData(452_00_62, A.BioSystemsLab,
                 'Bio-Systems Lab - StarMist', 0x3E),
    LocationData(452_00_63, A.BioSystemsLab,
                 'Bio-Systems Lab - Dynamite', 0x3F),

    LocationData(452_01_03, A.BioSystemsLabBasement,
                 'Bio-Systems Lab - Recorder', None, 0xdbfd),
]

climatrol_locations = [
    LocationData(452_00_64, A.Climatrol, 'Climatrol - JwlRibbon', 0x40),
    LocationData(452_00_65, A.Climatrol, 'Climatrol - FiberVest', 0x41),
    LocationData(452_00_66, A.Climatrol, 'Climatrol - KnifeBoots', 0x42),
    LocationData(452_00_67, A.Climatrol, 'Climatrol - SilRibbon', 0x43),
    LocationData(452_00_68, A.Climatrol, 'Climatrol - Sandals', 0x44),
    LocationData(452_00_69, A.Climatrol, 'Climatrol - LaserBar', 0x45),
    LocationData(452_00_70, A.Climatrol, 'Climatrol - CeramBar', 0x46),

    LocationData(452_02_05, A.Climatrol, 'Climatrol - Neifirst').fix(
        I.NeifirstFlag, 0xc735),
]

naval_locations = [
    LocationData(452_00_71, A.DezolisDungeons, 'Naval - NeiShield', 0x47),
    LocationData(452_00_72, A.DezolisDungeons, 'Naval - NeiEmel', 0x48),
    LocationData(452_00_73, A.DezolisDungeons, 'Naval - TruthSlvs', 0x49),
    LocationData(452_00_74, A.DezolisDungeons, 'Naval - Trimate', 0x4A),
    LocationData(452_00_75, A.DezolisDungeons, 'Naval - MirEmel', 0x4B),
    LocationData(452_00_76, A.DezolisDungeons, 'Naval - LaconEmel', 0x4C),
    LocationData(452_00_77, A.DezolisDungeons, 'Naval - GrSleeves', 0x4D),
]

menobe_locations = [
    LocationData(452_00_78, A.DezolisDungeons, 'Menobe - NeiCrown', 0x4E),
    LocationData(452_00_79, A.DezolisDungeons, 'Menobe - StormGear', 0x4F),
    LocationData(452_00_80, A.DezolisDungeons, 'Menobe - Neimet', 0x50),
    LocationData(452_00_81, A.DezolisDungeons, 'Menobe - ColorScarf', 0x51),
]

ikuto_locations = [
    LocationData(452_00_82, A.DezolisDungeons, 'Ikuto - NeiSlasher', 0x52),
    LocationData(452_00_83, A.DezolisDungeons, 'Ikuto - NeiShot', 0x53),
    LocationData(452_00_84, A.DezolisDungeons, 'Ikuto - FireStaff', 0x54),
    LocationData(452_00_85, A.DezolisDungeons, 'Ikuto - LacnMace', 0x55),
    LocationData(452_00_86, A.DezolisDungeons, 'Ikuto - PlsCannon', 0x56),
    LocationData(452_00_87, A.DezolisDungeons, 'Ikuto - LacDagger', 0x57),
]

guaron_locations = [
    LocationData(452_00_88, A.DezolisDungeons, 'Guaron - AmberRobe', 0x58),
    LocationData(452_00_89, A.DezolisDungeons, 'Guaron - Laconinish', 0x59),
    LocationData(452_00_90, A.DezolisDungeons, 'Guaron - CrystChest', 0x5A),
    LocationData(452_00_91, A.DezolisDungeons, 'Guaron - NeiCape', 0x5B),
    LocationData(452_00_92, A.DezolisDungeons, 'Guaron - CrystCape', 0x5C),
    LocationData(452_00_93, A.DezolisDungeons, 'Guaron - NeiArmor', 0x5D),
]

uzo_locations = [
    LocationData(452_01_00, A.Uzo, 'Uzo - Maruera Tree', None, 0xdbad),
]

paseo_locations = [
    LocationData(452_01_08, A.Motavia, 'Paseo - Give Recorder to Governor',
                 None, 0xc4d1).add_items({I.Recorder}),
]

oputa_locations = [
    # TODO this will be a weird Client check...
    LocationData(452_02_06, A.Oputa, 'Oputa - Ustvestia').fix(I.MusikFlag, -1),
]

control_tower_locations = [
    # TODO all four card locations are handled by one function; hard to change
    LocationData(452_01_04, A.ControlTower,
                 'Control Tower - Green Card').fix(I.GreenCard, -1),
    LocationData(452_01_05, A.ControlTower,
                 'Control Tower - Blue Card').fix(I.BlueCard, -1),
    LocationData(452_01_06, A.ControlTower,
                 'Control Tower - Yellow Card').fix(I.YellowCard, -1),
    LocationData(452_01_07, A.ControlTower,
                 'Control Tower - Red Card').fix(I.RedCard, -1),
]

kueri_locations = [
    LocationData(452_01_09, A.Kueri, 'Kueri - Give MruraLeaf to Researcher',
                 None, 0xc94f).add_items({I.MruraLeaf}),
]

gaira_locations = [
    LocationData(452_02_00, A.Gaira, 'Gaira - Console').fix(
        I.SpaceshipFlag, 0xc73f),
]

noah_locations = [
    LocationData(452_02_00, A.Noah, 'Noah - Mother Brain').fix(
        I.WinTheGameFlag, 0xf600, 8),
]

# TODO LocationData(452_00_13, 'Unknown200Meseta', 0xD),
# TODO change item Shir steals? d100-d107

all_locations = skure_locations + esper_mansion_locations + shure_locations + nido_locations + roron_locations + yellow_dam_locations + red_dam_locations + blue_dam_locations + green_dam_locations + bio_systems_lab_locations + \
    climatrol_locations + naval_locations + menobe_locations + ikuto_locations + guaron_locations + \
    uzo_locations + paseo_locations + oputa_locations + control_tower_locations + \
    kueri_locations + gaira_locations + noah_locations

locations_by_id = {location.id: location for location in all_locations}
locations_by_name = {location.name: location for location in all_locations}

location_name_groups = {
    'Shure': {loc.name for loc in shure_locations},
    'Tower of Nido': {loc.name for loc in nido_locations},
    'Skure': {loc.name for loc in skure_locations},
    'Roron': {loc.name for loc in roron_locations},
    'Bio-Systems Lab': {loc.name for loc in bio_systems_lab_locations},
    'Yellow Dam': {loc.name for loc in yellow_dam_locations},
    'Red Dam': {loc.name for loc in red_dam_locations},
    'Blue Dam': {loc.name for loc in blue_dam_locations},
    'Green Dam': {loc.name for loc in green_dam_locations},
    'Climatrol': {loc.name for loc in climatrol_locations},
    'Esper Mansion': {loc.name for loc in esper_mansion_locations},
    'Naval': {loc.name for loc in naval_locations},
    'Menobe': {loc.name for loc in menobe_locations},
    'Ikuto': {loc.name for loc in ikuto_locations},
    'Guaron': {loc.name for loc in guaron_locations},
    'Other': {loc.name for loc in uzo_locations + paseo_locations + oputa_locations + control_tower_locations + kueri_locations + gaira_locations + noah_locations},
}
