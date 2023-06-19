from typing import NamedTuple

from panda3d.core import Vec4


class Medallion(NamedTuple):
    model: str
    part: str = None
    color: Vec4 = None


class Department(NamedTuple):
    blazer: str
    leg: str
    sleeve: str
    tie: str
    medallion: Medallion
    gloveColor: Vec4 = None
