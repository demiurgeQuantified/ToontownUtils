from panda3d.core import Vec4

defaultTextureExtension = "jpg"
defaultModelExtension = "bam"


def readColor(col: list) -> Vec4:
    return Vec4(col[0], col[1], col[2], 1)


def addExtensionIfMissing(tex: str, ext: str) -> str:
    if "." not in tex.split("/")[-1]:
        tex = tex + "." + ext
    return tex
