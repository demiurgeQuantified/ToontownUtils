from typing import NamedTuple

from toontown_utils.toon.ToonHead import ToonHead


class ToonSpecies(NamedTuple):
    heads: dict[str, ToonHead]
    size: float = 1
