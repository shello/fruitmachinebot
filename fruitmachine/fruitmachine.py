"""A Fruit Machine bot."""

import random
from typing import BinaryIO, Tuple, Optional

from PIL import Image

from fruitmachine.parts import MachineStyle, Reel
from fruitmachine.resources import Resources
from fruitmachine.phrase_generator import PhraseGenerator


class FruitMachine:
    """A Fruit Machine bot."""

    def __init__(self, resources: Optional[Resources] = None):
        """Initialise FruitMachine."""
        if not resources:
            self.res = Resources()
        else:
            self.res = resources

    def get_random_machine(self):
        """Get a random Machine style."""
        return random.choice(self.res.get_machines())

    def get_random_reel_symbols(self, count=3):
        """Get a random set of 'count' symbols for each reel."""
        reels = []

        for reel in self.res.get_reels():
            # Select 'count' symbols from each reel
            symbols = random.sample(reel.symbols, count)

            # Then for each of the symbols choose one of the variants
            reels.append(tuple(random.choice(symbol) for symbol in symbols))

        return tuple(reels)

    def randomize_machine(self) -> Tuple[MachineStyle, Tuple[Reel], str, str]:
        """Generate a machine and its messages."""
        machine = self.get_random_machine()
        reels = self.get_random_reel_symbols(count=len(machine.positions[0]))

        payline = [r[1].description for r in reels]
        description = f"A {machine.description} Fruit Machine with the " \
            f"centre payline showing a combination of {payline[0]}, " \
            f" {payline[1]}, and {payline[2]}."

        status_message = PhraseGenerator(self.res.get_statuses())\
            .generate_phrase(machine=machine, reels=reels)

        return machine, reels, description, status_message

    def generate_image(self, machine: MachineStyle, reels: Tuple[Reel],
                       fp: BinaryIO):
        """Generate and write the Fruit Machine image to a file pointer."""
        img = Image.open(machine.background).convert(mode='RGBA')
        for reel, reel_pos in zip(reels, machine.positions):
            for symbol, position in zip(reel, reel_pos):
                im_symb = Image.new(mode='RGBA', size=img.size)
                im_symb.paste(Image.open(symbol.image_file), position)
                img = Image.alpha_composite(img, im_symb)

        im_fg = Image.open(machine.foreground).convert(mode='RGBA')
        img = Image.alpha_composite(img, im_fg)

        img.save(fp, format='PNG')

    def generate(self, image_fp: BinaryIO) -> Tuple[str, str]:
        """Generate a random fruit machine image, description and status."""
        machine, reels, description, status_message = self.randomize_machine()

        self.generate_image(machine=machine, reels=reels, fp=image_fp)

        return description, status_message
