from typing import NamedTuple

from panda3d.core import Vec4

from ToontownUtils.Department import Department
from ToontownUtils.Body import Body


class TemplateCog(NamedTuple):
    name: str
    department: Department

    body: Body
    size: float
    gloveColor: Vec4

    head: str
    head2: str = None
    headTexture: str = None
    headColor: Vec4 = None
