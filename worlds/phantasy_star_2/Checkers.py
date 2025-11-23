from typing import Callable, Iterable, Mapping

from BaseClasses import CollectionState


CheckFn = Callable[[CollectionState], bool]
CheckConstructorFn = Callable[[int], CheckFn]


def Always() -> CheckConstructorFn:
    return lambda player: lambda state: True


def And(checkers: Iterable[CheckConstructorFn]) -> CheckConstructorFn:
    def check_constructor(player: int):
        def checker(state: CollectionState):
            for ch in checkers:
                if not ch(player)(state):
                    return False
            return True
        return checker
    return check_constructor


def Has(name: str, count: int = 1) -> CheckConstructorFn:
    return lambda player: lambda state: state.has(name, player, count)


def HasAll(names: set[str]) -> CheckConstructorFn:
    return lambda player: lambda state: state.has_all(names, player)


def HasAllCounts(item_counts: Mapping[str, int]) -> CheckConstructorFn:
    return lambda player: lambda state: state.has_all_counts(item_counts, player)


def Or(checkers: Iterable[CheckConstructorFn]) -> CheckConstructorFn:
    def check_constructor(player: int):
        def checker(state: CollectionState):
            for ch in checkers:
                if ch(player)(state):
                    return True
            return False
        return checker
    return check_constructor
