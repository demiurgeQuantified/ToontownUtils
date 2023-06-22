from typing import NamedTuple


class ToonHead(NamedTuple):
    model: str
    muzzles: dict[str, str]
    parts: list[str] = None
    muzzleModel: str = None
    anims: dict[str, str] = None
