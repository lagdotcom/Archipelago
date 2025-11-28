import logging
from typing import TYPE_CHECKING, Callable, Iterable, Mapping, NamedTuple, Sequence

from BaseClasses import CollectionState
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


logger = logging.getLogger("laglib")

# region Platforms

genesis_rom = "MD CART"
genesis_ram = "68K RAM"

# endregion


# region Memory Classes


class MemorySpan(NamedTuple):
    region: str
    address: int
    size: int
    encoding: str = "ascii"

    @property
    def end_address(self):
        return self.address + self.size

    def __repr__(self):
        return "%s[%04x, %d]" % (self.region, self.address, self.size)

    def as_tuple(self):
        return self.address, self.size, self.region


class MemoryBlock:
    def __init__(self, span: MemorySpan, contents: bytes):
        self.span = span
        self.contents = contents

    def contains(self, span: MemorySpan):
        return (
            self.span.address <= span.address
            and self.span.end_address >= span.end_address
        )

    def extract(self, span: MemorySpan):
        start = span.address - self.span.address
        return self.contents[start : start + span.size]

    def patch(self, span: MemorySpan, data: bytes):
        start = span.address - self.span.address
        self.contents = (
            self.contents[:start] + data + self.contents[start + span.size :]
        )


class MemoryManager:
    def __init__(self, names: Mapping[int, str] = {}):
        self.spans: list[MemorySpan] = []
        self.blocks: list[MemoryBlock] = []
        self.names = names

    def request(self, ctx: "BizHawkClientContext", spans: Iterable[MemorySpan]):
        return bizhawk.read(
            ctx.bizhawk_ctx, list(map(lambda span: span.as_tuple(), spans))
        )

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

    def get_bytes(self, span: MemorySpan):
        block = self.get_block_for_span(span)
        if block:
            return block.extract(span)
        raise Exception(f"Manager does not have {span}")

    async def write_span(
        self, ctx: "BizHawkClientContext", span: "IntSpan", new_value: int
    ):
        old_value = span.get(self)
        if await bizhawk.guarded_write(
            ctx.bizhawk_ctx, [span.as_write(new_value)], [span.as_write(old_value)]
        ):
            block = self.get_block_for_span(span)
            if block:
                block.patch(span, span.format(new_value))
            return True

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

    def _log_change(self, old: MemoryBlock, new: MemoryBlock):
        for i in range(len(old.contents)):
            o = old.contents[i]
            n = new.contents[i]
            if o != n:
                addr = old.span.address + i
                if addr in self.names:
                    name = self.names[addr]
                else:
                    name = "?"
                logger.debug(
                    "%04x %s: %02x -> %02x (%02x flipped)" % (addr, name, o, n, o ^ n)
                )


class IntSpan(MemorySpan):
    def parse(self, raw: bytes):
        return int.from_bytes(raw, "big")

    def get(self, mem: MemoryManager):
        return self.parse(mem.get_bytes(self))

    def format(self, value: int):
        return value.to_bytes(self.size, "big")

    def as_write(self, value: int):
        return self.address, self.format(value), self.region


class StrSpan(MemorySpan):
    def parse(self, raw: bytes):
        return raw.split(b"\0")[0].decode(self.encoding)

    def get(self, mem: MemoryManager):
        return self.parse(mem.get_bytes(self))


# endregion

# region Logic


type Predicate[T] = Callable[[T], bool]
type PlayerPredicate[T] = Callable[[int], Predicate[T]]
type StateCheck = PlayerPredicate[CollectionState]


def always[T]() -> PlayerPredicate[T]:
    return lambda player: lambda state: True


def need_all[T](checkers: Iterable[PlayerPredicate[T]]) -> PlayerPredicate[T]:
    def check_constructor(player: int):
        def checker(state: T):
            for ch in checkers:
                if not ch(player)(state):
                    return False
            return True

        return checker

    return check_constructor


def need_one[T](checkers: Iterable[PlayerPredicate[T]]) -> PlayerPredicate[T]:
    def check_constructor(player: int):
        def checker(state: T):
            for ch in checkers:
                if ch(player)(state):
                    return True
            return False

        return checker

    return check_constructor


def has(name: str, count: int = 1) -> PlayerPredicate[CollectionState]:
    return lambda player: lambda state: state.has(name, player, count)


def has_all(names: set[str]) -> PlayerPredicate[CollectionState]:
    return lambda player: lambda state: state.has_all(names, player)


def has_all_counts(item_counts: Mapping[str, int]) -> PlayerPredicate[CollectionState]:
    return lambda player: lambda state: state.has_all_counts(item_counts, player)


# endregion
