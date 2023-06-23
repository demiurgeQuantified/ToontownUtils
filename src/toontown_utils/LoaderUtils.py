from typing import Any

from panda3d.core import Vec4

defaultTextureExtension = "jpg"
defaultModelExtension = "bam"


def readColor(col: list | None) -> Vec4 | None:
    if col is None:
        return None
    return Vec4(col[0], col[1], col[2], 1)


def addExtensionIfMissing(tex: str | None, ext: str) -> None | str:
    if tex is None:
        return None
    if "." not in tex.split("/")[-1]:
        tex = tex + "." + ext
    return tex


def addExtensions(data: dict[Any, str], ext: str):
    for k, v in data.items():
        data[k] = addExtensionIfMissing(v, ext)
