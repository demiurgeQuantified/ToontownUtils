from typing import NamedTuple


class ToonHead(NamedTuple):
    model: str
    muzzles: dict[str, str]
    colorParts: list[str]
    leftPupil: str
    rightPupil: str
    keepParts: list[str] = None
    keepAllParts: bool = False
    muzzleModel: str = None
    anims: dict[str, str] = None
