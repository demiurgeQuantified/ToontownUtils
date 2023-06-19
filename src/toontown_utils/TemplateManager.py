import json
from typing import Any

from panda3d.core import Vec4

from toontown_utils.cog.TemplateCog import TemplateCog
from toontown_utils.cog.Department import Department, Medallion
from toontown_utils.cog.Body import Body, Skelecog

defaultTextureExtension = "jpg"
defaultModelExtension = "bam"

Cogs: dict[str, TemplateCog] = {}
Departments: dict[str, Department] = {}
Bodies: dict[str, Body] = {}


def readColor(col: list) -> Vec4:
    return Vec4(col[0], col[1], col[2], 1)


def addExtensionIfMissing(tex: str, ext: str) -> str:
    if "." not in tex.split("/")[-1]:
        tex = tex + "." + ext
    return tex


def loadFile(path: str) -> bool:
    try:
        file = open(path, 'r', encoding='utf-8')
    except OSError:
        print(f"CogLoader ERROR: Failed to open {path}")
        return False

    try:
        contents: dict = json.loads(file.read())
    except json.JSONDecodeError:
        file.close()
        print(f"CogLoader ERROR: {path} is not a valid JSON file.")
        return False

    file.close()

    departments: dict = contents.get("departments", None)
    if departments is not None:
        loadDepartments(departments)

    bodies: dict = contents.get("bodies", None)
    if bodies is not None:
        loadBodies(bodies)

    cogs: dict = contents.get("cogs", None)
    if cogs is not None:
        loadCogs(cogs)

    return True


def loadCogs(cogs: dict[str, Any]) -> None:
    for cog, data in cogs.items():
        try:
            deptName: str = data["department"]
        except KeyError:
            print(f"Cog {cog} has no department set!")
            continue

        try:
            dept: Department = Departments[deptName]
        except KeyError:
            print(f"Cog {cog} is member of unknown department {deptName}")
            continue

        try:
            body: str = data["body"]
        except KeyError:
            print(f"Cog {cog} has no body set!")
            continue

        try:
            bodyType: Body = Bodies[body]
        except KeyError:
            print(f"Cog {cog} has unknown body {body}")
            continue

        try:
            headColor: list | Vec4 = data.get("headColor", None)
            if headColor is not None:
                headColor = readColor(headColor)

            gloveColor: list | Vec4 = data.get("gloveColor", dept.gloveColor or None)
            if gloveColor is None:
                gloveColor = Vec4(0, 0, 0, 1)
                print(f"Cog {cog} does not have a gloveColor set, and {deptName} does not have a default glove color.")
            if isinstance(gloveColor, list):
                gloveColor = readColor(gloveColor)

            headTexture: str = data.get("headTexture", None)
            if headTexture is not None:
                headTexture = addExtensionIfMissing(headTexture, defaultTextureExtension)

            Cogs[cog] = TemplateCog(
                cog,
                dept,
                bodyType,
                data["size"],
                gloveColor,
                data["head"],
                head2 = data.get("head2", None),
                headTexture = headTexture,
                headColor = headColor
            )
        except KeyError as e:
            print(f"Cog {cog} is missing required field {e.args[0]}.")


def loadDepartments(depts: dict[str, Any]) -> None:
    for dept, data in depts.items():
        try:
            gloveColor: list | Vec4 = data.get("gloveColor", None)
            if gloveColor is not None:
                gloveColor = readColor(gloveColor)

            medallionColor: list | Vec4 = data["medallion"].get("color", None)
            if medallionColor is not None:
                medallionColor = readColor(medallionColor)

            medallion = Medallion(
                model=addExtensionIfMissing(data["medallion"]["model"], defaultModelExtension),
                color=medallionColor,
                part=data["medallion"].get("part", None)
            )

            Departments[dept] = Department(
                addExtensionIfMissing(data["blazer"], defaultTextureExtension),
                addExtensionIfMissing(data["leg"], defaultTextureExtension),
                addExtensionIfMissing(data["sleeve"], defaultTextureExtension),
                addExtensionIfMissing(data["tie"], defaultTextureExtension),
                medallion,
                gloveColor=gloveColor
            )
        except KeyError as e:
            print(f"Department {dept} is missing required field {e.args[0]}.")


def loadBodies(bodies: dict[str, Any]) -> None:
    for bodyType, data in bodies.items():
        try:
            animations: dict = data.get("animations", None)
            if animations is not None:
                for anim in animations:
                    animations[anim] = addExtensionIfMissing(animations[anim], defaultModelExtension)
            else:
                print(f"WARN: Body {bodyType} has no animations.")

            loseModel: str = data.get("loseModel", None)
            if loseModel is not None:
                loseModel = addExtensionIfMissing(loseModel, defaultModelExtension)

            skelecog: Skelecog = None
            skelecogData = data.get("skelecog", None)
            if skelecogData is not None:
                try:
                    skeleLoseModel = skelecogData.get("loseModel", None)
                    if skeleLoseModel is not None:
                        skeleLoseModel = addExtensionIfMissing(skeleLoseModel, defaultModelExtension)
                    skelecog = Skelecog(
                        addExtensionIfMissing(skelecogData["model"], defaultModelExtension),
                        skeleLoseModel
                    )
                except KeyError as e:
                    print(f"Body {bodyType} skelecog is missing required field {e.args[0]}, skipping.")

            Bodies[bodyType] = Body(
                addExtensionIfMissing(data["model"], defaultModelExtension),
                addExtensionIfMissing(data["headsModel"], defaultModelExtension),
                animations=animations,
                loseModel=loseModel,
                skelecog=skelecog,
                loseAnim=data.get("loseAnim", "lose"),
                sizeFactor=data.get("sizeFactor", 1)
            )
        except KeyError as e:
            print(f"Body {bodyType} is missing required field {e.args[0]}.")
