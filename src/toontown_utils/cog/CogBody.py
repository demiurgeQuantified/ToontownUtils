from typing import NamedTuple


class Skelecog(NamedTuple):
    model: str
    loseModel: str = None


class CogBody(NamedTuple):
    model: str
    headsModel: str
    animations: dict[str, str] = None
    loseModel: str = None
    skelecog: Skelecog = None
    loseAnim: str = "lose"
    sizeFactor: float = 1
