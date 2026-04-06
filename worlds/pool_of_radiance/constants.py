from .laglib import IntSpan, StrSpan, nes_ram, nes_rom, nes_sram

game_name = "Pool of Radiance"
patch_file_ending = ".apadndpor"

# Helpers


def ram_label(offset: int):
    return f"{nes_ram}:{offset:04x}"


def ram(offset: int, size: int):
    return IntSpan(nes_ram, offset, size)


def sram_label(offset: int):
    return f"{nes_sram}:{offset - 0x6000:04x}"


def sram(offset: int, size: int):
    return IntSpan(nes_sram, offset - 0x6000, size)


def rom(bank: int, offset: int, size: int):
    return IntSpan(nes_rom, bank * 0x2000 + offset % 0x2000, size)


def rom_str(bank: int, offset: int, size: int, encoding: str = "ascii"):
    return StrSpan(nes_rom, bank * 0x2000 + offset % 0x2000, size, encoding)


# RAM addresses

ram_names = {
    ram_label(0x00A6): "gameMode",
    sram_label(0x766A): "slums.foughtShopGuards",
    sram_label(0x7692): "slums.fightCount",
    sram_label(0x7693): "slums.ohlo",
    sram_label(0x7694): "slums.gypsyDead",
    sram_label(0x7695): "slums.floorboardTreasure",
    sram_label(0x7680): "gems[0]",
    sram_label(0x7681): "gems[1]",
    sram_label(0x7682): "gold[0]",
    sram_label(0x7683): "gold[1]",
    sram_label(0x7684): "gold[2]",
    sram_label(0x76B8): "sewers.norris",
    sram_label(0x76B9): "sokal.cleared",
    sram_label(0x76BA): "wealthy.cleared",
    sram_label(0x76BB): "buccaneer.bivant",
    sram_label(0x76BC): "mendor.book1",
    sram_label(0x76BD): "mendor.book2",
    sram_label(0x76BE): "mendor.book3",
    sram_label(0x76BF): "mendor.book4",
    sram_label(0x76C0): "mendor.book5",
    sram_label(0x76C1): "mendor.badBook",
    sram_label(0x76C2): "podol.auction",
    sram_label(0x76C3): "valhingen.cleared",
    sram_label(0x76C4): "kovel.cleared",
    sram_label(0x76C5): "yarash.cleared",
    sram_label(0x76C6): "zhentil.cleared",
    sram_label(0x76C7): "lizardmen.cleared",
    sram_label(0x76C8): "kobolds.cleared",
    sram_label(0x76C9): "nomads.cleared",
    sram_label(0x76CA): "cadorna.treasureTaken",
    sram_label(0x76CB): "stojanow.cleared",
    sram_label(0x76CC): "valjevo.cleared",
    sram_label(0x76CD): "slums.cleared",
    sram_label(0x76CF): "bane.cleared",
    sram_label(0x76D1): "cadorna.dead",
    sram_label(0x76D2): "phlan.foughtTheLaw",
    sram_label(0x76D3): "phlan.questsDone",
    sram_label(0x76D4): "mendor.cleared",
    sram_label(0x76D5): "slums.encountersDone",
    sram_label(0x76DE): "slums.dirtyRoomTreasure",
    sram_label(0x76E8): "slums.secretTreasureRoom",
    sram_label(0x76EB): "slums.killedFlourTroll",
    sram_label(0x7FEE): "receivedItemStorage",
}

game_mode = ram(0xA6, 1)

# TODO this is a bit large
progress_flags = sram(0x7633, 0x100)

current_gems = sram(0x7680, 2)
current_money = sram(0x7682, 3)

# TODO check safety!
received_item_storage = sram(0x7FEE, 2)

# ROM addresses

rom_name = rom_str(63, 0xFFE0, 16)

name_space = StrSpan(nes_rom, 0x6BE00, 0x200, "utf-8")
goal_space = IntSpan(nes_rom, 0x6BEFF, 1)
