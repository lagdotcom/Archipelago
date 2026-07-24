import logging
from collections.abc import Callable, Iterable, Mapping, Sequence
from math import ceil
from random import Random
from typing import TYPE_CHECKING, Any, Literal, NamedTuple

import worlds._bizhawk as bizhawk
from Options import Option
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


logger = logging.getLogger("laglib")

# region Platforms

genesis_rom = "MD CART"
genesis_ram = "68K RAM"

genesis_file_types = [
    ("GEN", [".gen"]),
    ("BIN", [".bin"]),
    ("SMD", [".smd"]),
    ("68K", [".68k"]),
]

nes_ram = "RAM"
nes_sram = "Battery RAM"
nes_rom = "PRG ROM"

nes_file_types = [
    ("NES", [".nes"]),
    ("UNH", [".unh"]),
]

# endregion


# region Memory Classes


class MemorySpan(NamedTuple):
    region: str
    address: int
    size: int
    encoding: str = "ascii"
    byteorder: Literal["little", "big"] = "big"

    @property
    def end_address(self):
        return self.address + self.size

    def __repr__(self):
        return f"{self.region}[{self.address:04x}, {self.size}]"

    def as_tuple(self):
        return self.address, self.size, self.region


class MemoryBlock:
    def __init__(self, span: MemorySpan, contents: bytes):
        self.span = span
        self.contents = contents

    def contains(self, span: MemorySpan):
        return self.span.address <= span.address and self.span.end_address >= span.end_address

    def extract(self, span: MemorySpan):
        start = span.address - self.span.address
        return self.contents[start : start + span.size]

    def patch(self, span: MemorySpan, data: bytes):
        start = span.address - self.span.address
        self.contents = self.contents[:start] + data + self.contents[start + span.size :]


class MemoryManager:
    def __init__(self, names: Mapping[str, str] = {}):
        self.spans: list[MemorySpan] = []
        self.blocks: list[MemoryBlock] = []
        self.names = names
        self.translations: dict[int, Callable[[int], Any]] = {}

    def translate(self, address: int, translator: Callable[[int], Any]):
        self.translations[address] = translator

    def request(self, ctx: "BizHawkClientContext", spans: Iterable[MemorySpan]):
        return bizhawk.read(ctx.bizhawk_ctx, [span.as_tuple() for span in spans])

    async def update(self, ctx: "BizHawkClientContext"):
        results = await self.request(ctx, self.spans)
        new_blocks: list[MemoryBlock] = []
        for i in range(len(results)):
            new_block = MemoryBlock(self.spans[i], results[i])
            new_blocks.append(new_block)
            if i < len(self.blocks):
                old_block = self.blocks[i]
                self._log_change(old_block, new_block)
        self.blocks = new_blocks

    def get(self, region: str, address: int):
        return self.get_bytes(MemorySpan(region, address, 1))[0]

    def get_block_for_span(self, span: MemorySpan):
        for block in self.blocks:
            if block.contains(span):
                return block
        return None

    def get_bytes(self, span: MemorySpan):
        block = self.get_block_for_span(span)
        if block:
            return block.extract(span)
        raise Exception(f"Manager does not have {span}")

    async def write_span(self, ctx: "BizHawkClientContext", span: "IntSpan", new_value: int):
        old_value = span.get(self)
        if await bizhawk.guarded_write(ctx.bizhawk_ctx, [span.as_write(new_value)], [span.as_write(old_value)]):
            block = self.get_block_for_span(span)
            if block:
                block.patch(span, span.format(new_value))
            return True
        return False

    async def write_list(
        self,
        ctx: "BizHawkClientContext",
        write_list: Sequence[tuple[int, bytes, str]],
        guard_list: Sequence[tuple[int, bytes, str]],
    ):
        if await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, guard_list):
            for addr, data, region in write_list:
                span = IntSpan(region, addr, len(data))
                block = self.get_block_for_span(span)
                if block:
                    block.patch(span, data)
            return True
        return False

    def _log_change(self, old: MemoryBlock, new: MemoryBlock):
        for i in range(len(old.contents)):
            o = old.contents[i]
            n = new.contents[i]
            if o != n:
                addr = old.span.address + i
                name = f"{old.span.region}:{addr:04x}"
                if name in self.names:
                    name = self.names[name]
                if addr in self.translations:
                    old_val = self.translations[addr](o)
                    new_val = self.translations[addr](n)
                else:
                    old_val = f"{o:02x}"
                    new_val = f"{n:02x}"
                logger.debug("%04x %s: %s -> %s (%02x flipped)", addr, name, old_val, new_val, o ^ n)


class IntSpan(MemorySpan):
    def parse(self, raw: bytes):
        return int.from_bytes(raw, self.byteorder)

    def get(self, mem: MemoryManager):
        return self.parse(mem.get_bytes(self))

    def format(self, value: int):
        return value.to_bytes(self.size, self.byteorder)

    def as_write(self, value: int):
        return self.address, self.format(value), self.region


class StrSpan(MemorySpan):
    def parse(self, raw: bytes):
        return raw.split(b"\0")[0].decode(self.encoding)

    def get(self, mem: MemoryManager):
        return self.parse(mem.get_bytes(self))


# endregion


# region Common functions


def sample_repeating(random: Random, population: list[str], count: int):
    repeats = ceil(count / len(population))
    return random.sample(population * repeats, count)


def use_re_gen_passthrough(world: World):
    """
    Help Universal Tracker generation by using options passed through slot_data.
    """
    re_gen_passthrough = getattr(world.multiworld, "re_gen_passthrough", {})
    if re_gen_passthrough and world.game in re_gen_passthrough:
        # Get the passed through slot data from the real generation
        slot_data: dict[str, Any] = re_gen_passthrough[world.game]

        slot_options: dict[str, Any] = slot_data.get("options", {})
        # Set all your options here instead of getting them from the yaml
        for key, value in slot_options.items():
            opt: Option[Any] | None = getattr(world.options, key, None)
            if opt is not None:
                # You can also set .value directly but that won't work if you have OptionSets
                setattr(world.options, key, opt.from_any(value))


# endregion
