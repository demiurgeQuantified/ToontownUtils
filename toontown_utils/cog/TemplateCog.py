from typing import NamedTuple

from panda3d.core import Vec4

from toontown_utils.cog.Department import Department
from toontown_utils.cog.CogBody import CogBody


class TemplateCog(NamedTuple):
    name: str
    department: Department

    body: CogBody
    size: float
    gloveColor: Vec4

    head: str
    head2: str = None
    headTexture: str = None
    headColor: Vec4 = None
