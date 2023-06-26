from typing import NamedTuple


class ToonPart(NamedTuple):
    model: str
    anims: dict[str, str]
