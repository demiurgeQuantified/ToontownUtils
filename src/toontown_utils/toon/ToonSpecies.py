from typing import NamedTuple


class ToonSpecies(NamedTuple):
    heads: str
    size: float = 1
    headAnims: dict[str, str] = None
