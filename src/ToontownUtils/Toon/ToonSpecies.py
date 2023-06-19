from typing import NamedTuple


class ToonSpecies(NamedTuple):
    heads: dict[str, str]
    size: float = 1
    headAnims: dict[str, str] = None
