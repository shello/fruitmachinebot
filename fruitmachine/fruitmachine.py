"""A Fruit Machine bot."""

import random
from typing import Iterable, NamedTuple, Tuple, BinaryIO

from PIL import Image


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


class FruitMachine:
    """A Fruit Machine bot."""

    def __init__(self, machines, reels):
        """Initialise FruitMachine."""
        self.machines = machines
        self.reels = reels

    @classmethod
    def get_description(cls, name):
        """Transform the filename into a description."""
        return name.replace('_', ' ').title()

    def get_random_machine(self):
        """Get a random Machine style."""
        return random.choice(self.machines)

    def get_random_reel_symbols(self, count=3):
        """Get a random set of 'count' symbols for each reel."""
        reels = []

        for reel in self.reels:
            # Select 'count' symbols from each reel
            symbols = random.sample(reel.symbols, count)

            # Then for each of the symbols choose one of the variants
            reels.append(tuple(random.choice(symbol) for symbol in symbols))

        return tuple(reels)

    def generate(self, fp: BinaryIO) -> Tuple[str, MachineStyle, Tuple]:
        """Generate a random fruit machine image, returning a description."""
        machine = self.get_random_machine()
        reels = self.get_random_reel_symbols(count=len(machine.positions[0]))

        img = Image.open(machine.background).convert(mode='RGBA')
        for reel, reel_pos in zip(reels, machine.positions):
            for symbol, position in zip(reel, reel_pos):
                im_symb = Image.new(mode='RGBA', size=img.size)
                im_symb.paste(Image.open(symbol.image_file), position)
                img = Image.alpha_composite(img, im_symb)

        im_fg = Image.open(machine.foreground).convert(mode='RGBA')
        img = Image.alpha_composite(img, im_fg)

        img.save(fp, format='PNG')

        payline = [self.get_description(r[1].description) for r in reels]

        description = f"A {machine.description} Fruit Machine with the " \
            f"centre payline showing a combination of {payline[0]}, " \
            f" {payline[1]}, and {payline[2]}."

        return description, machine, reels
