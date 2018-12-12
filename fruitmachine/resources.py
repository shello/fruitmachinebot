"""Functions to load resources."""

from collections import defaultdict
import json
import os
import os.path

from .fruitmachine import MachineStyle, Reel, ReelSymbol


_BASEDIR = os.path.abspath(os.path.join(os.path.basename(__file__), '..'))


class Resources:
    """Resources manager for Fruit Machine."""

    _res: dict

    def __init__(self, res_filename=None):
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

    def get_reels(self) -> tuple:
        """Get a list of reels with symbols loaded in."""
        reels = []

        for reel in self._res['reels']:
            symbols = []
            for path in reel:
                real_path = os.path.join(_BASEDIR, path)

                if not os.path.exists(real_path):
                    raise Exception(f"Path does not exist: {real_path}")

                for root, _, files in os.walk(path):
                    symbols_found = defaultdict(list)
                    for fname in files:
                        fpath = os.path.join(root, fname)

                        fbase = os.path.basename(fpath)
                        fbase = fbase[:fbase.rfind('.')]
                        fbase = self._get_symbol_basename(fbase)

                        symb = ReelSymbol(description=fbase, image_file=fpath)
                        symbols_found[fbase].append(symb)
                    symbols += symbols_found.values()

            reels.append(Reel(symbols))

        return tuple(reels)

    def get_statuses(self) -> list:
        """Get all statuses."""
        return self._res['statuses']
