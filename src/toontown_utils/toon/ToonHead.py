from typing import NamedTuple


class Eyelashes(NamedTuple):
    open: str
    closed: str
    model: str = None


class ToonHead(NamedTuple):
    model: str
    muzzles: dict[str, str]
    colorParts: list[str]
    leftPupil: str
    rightPupil: str
    eyelashes: Eyelashes
    keepParts: list[str] = None
    keepAllParts: bool = False
    extraMuzzles: dict[str, dict[str, str]] = None
    anims: dict[str, str] = None
