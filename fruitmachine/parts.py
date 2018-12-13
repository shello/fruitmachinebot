"""Fruit Machine parts."""

from typing import Iterable, NamedTuple, Tuple

class ReelSymbol(NamedTuple):
    """A symbol to be used on a Fruit Machine reel."""

    description: str
    image_file: str


class MachineStyle(NamedTuple):
    """A Fruit Machine style."""

    description: str
    background: str
    foreground: str
    positions: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]


class Reel(NamedTuple):
    """A fruit machine reel."""

    symbols: Iterable[ReelSymbol]
