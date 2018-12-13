"""Fruit Machine parts."""

from typing import MutableSequence, NamedTuple, Sequence, Tuple


class ConcreteReelSymbol(NamedTuple):
    """A concrete reel symbol."""

    description: str
    image_file: str


class ReelSymbol(NamedTuple):
    """A symbol to be used on a Fruit Machine reel."""

    description: str
    image_files: MutableSequence[str]  # Variants of the same symbol


class MachineStyle(NamedTuple):
    """A Fruit Machine style."""

    description: str
    background: str
    foreground: str
    positions: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]


class Reel(NamedTuple):
    """A fruit machine reel."""

    symbols: Sequence[ReelSymbol]


SpunReel = Sequence[ConcreteReelSymbol]
SpunReels = Sequence[SpunReel]
