"""Functions to load resources."""

import json
import os
import os.path
from typing import Iterable, MutableMapping, MutableSequence, Optional
from typing import Sequence

from fruitmachine.parts import MachineStyle, Reel, ReelSymbol

_BASEDIR = os.path.abspath(os.path.join(os.path.basename(__file__), '..'))


class Resources:
    """Resources manager for Fruit Machine."""

    _res: dict

    def __init__(self, res_filename: Optional[str] = None):
        """Initialise resources."""
        if res_filename is None:
            res_file = os.path.join(_BASEDIR, 'data', 'resources.json')

        with open(res_file) as infile:
            self._res = json.load(infile)

    def get_machines(self) -> list:
        """Get the machine styles."""
        machines = []

        reel_positions = self._res['reel_positions']

        for machine in self._res['machines']:
            machines.append(MachineStyle(
                description=machine['description'],
                foreground=os.path.join(_BASEDIR, machine['foreground']),
                background=os.path.join(_BASEDIR, machine['background']),
                positions=reel_positions))

        return machines

    @classmethod
    def _get_symbol_basename(cls, filename: str) -> str:
        """Get the basename of a symbol with modifiers (MutantStd)."""
        if '_' in filename:
            possible_base, possible_mod = filename.rsplit('_', 1)
            if possible_mod[-1].isdigit():
                return possible_base

        return filename

    @classmethod
    def get_symbol_description(cls, name):
        """Transform the filename into a description."""
        return name.replace('_', ' ').title()

    @classmethod
    def get_reel_symbols(cls, path: str) -> Iterable[ReelSymbol]:
        """Get all the reel symbols from a given path."""
        real_path = os.path.join(_BASEDIR, path)

        if not os.path.exists(real_path):
            raise Exception(f"Path does not exist: {real_path}")

        symbols_found: MutableMapping[str, ReelSymbol] = {}
        for root, _, files in os.walk(path):
            for fname in files:
                fpath = os.path.join(root, fname)
                raw_name, ext = os.path.basename(fpath).rsplit('.', 1)

                if ext.lower() != 'png':
                    continue

                name = cls._get_symbol_basename(raw_name)

                if name in symbols_found:
                    symbols_found[name].image_files.append(fpath)
                else:
                    description = cls.get_symbol_description(name)
                    symbols_found[name] = ReelSymbol(description=description,
                                                     image_files=[fpath])

        return symbols_found.values()

    def get_reels(self) -> Sequence[Reel]:
        """Get a list of reels with symbols loaded in."""
        reels = []

        for reel in self._res['reels']:
            symbols: MutableSequence[ReelSymbol] = []
            for path in reel:
                symbols += self.get_reel_symbols(path)

            reels.append(Reel(symbols))

        return tuple(reels)

    def get_status_templates(self) -> Iterable:
        """Get all status templates."""
        return self._res['status_templates']
