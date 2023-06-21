from typing import Any

from panda3d.core import Vec4

from toontown_utils import LoaderUtils

from toontown_utils.cog.TemplateCog import TemplateCog
from toontown_utils.cog.Department import Department, Medallion
from toontown_utils.cog.Body import Body, Skelecog

Cogs: dict[str, TemplateCog] = {}
Departments: dict[str, Department] = {}
Bodies: dict[str, Body] = {}


def readFile(contents: dict[str, dict]) -> None:
    departments: dict = contents.get("departments")
    if departments is not None:
        loadDepartments(departments)

    bodies: dict = contents.get("bodies")
    if bodies is not None:
        loadBodies(bodies)

    cogs: dict = contents.get("cogs")
    if cogs is not None:
        loadCogs(cogs)


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
            headColor: list | Vec4 = data.get("headColor")
            if headColor is not None:
                headColor = LoaderUtils.readColor(headColor)

            gloveColor: list | Vec4 = data.get("gloveColor", dept.gloveColor or None)
            if gloveColor is None:
                gloveColor = Vec4(0, 0, 0, 1)
                print(
                    f"Cog {cog} does not have a gloveColor set, and {deptName} does not have a default glove color.")
            if isinstance(gloveColor, list):
                gloveColor = LoaderUtils.readColor(gloveColor)

            headTexture: str = data.get("headTexture")
            if headTexture is not None:
                headTexture = LoaderUtils.addExtensionIfMissing(headTexture, LoaderUtils.defaultTextureExtension)

            Cogs[cog] = TemplateCog(
                cog,
                dept,
                bodyType,
                data["size"],
                gloveColor,
                data["head"],
                head2=data.get("head2"),
                headTexture=headTexture,
                headColor=headColor
            )
        except KeyError as e:
            print(f"Cog {cog} is missing required field {e.args[0]}.")


def loadDepartments(depts: dict[str, Any]) -> None:
    for dept, data in depts.items():
        try:
            gloveColor: list | Vec4 = data.get("gloveColor")
            if gloveColor is not None:
                gloveColor = LoaderUtils.readColor(gloveColor)

            medallionColor: list | Vec4 = data["medallion"].get("color")
            if medallionColor is not None:
                medallionColor = LoaderUtils.readColor(medallionColor)

            medallion = Medallion(
                model=LoaderUtils.addExtensionIfMissing(data["medallion"]["model"], LoaderUtils.defaultModelExtension),
                color=medallionColor,
                part=data["medallion"].get("part")
            )

            Departments[dept] = Department(
                LoaderUtils.addExtensionIfMissing(data["blazer"], LoaderUtils.defaultTextureExtension),
                LoaderUtils.addExtensionIfMissing(data["leg"], LoaderUtils.defaultTextureExtension),
                LoaderUtils.addExtensionIfMissing(data["sleeve"], LoaderUtils.defaultTextureExtension),
                LoaderUtils.addExtensionIfMissing(data["tie"], LoaderUtils.defaultTextureExtension),
                medallion,
                gloveColor=gloveColor
            )
        except KeyError as e:
            print(f"Department {dept} is missing required field {e.args[0]}.")


def loadBodies(bodies: dict[str, Any]) -> None:
    for bodyType, data in bodies.items():
        try:
            animations: dict = data.get("animations")
            if animations is not None:
                for anim in animations:
                    animations[anim] = LoaderUtils.addExtensionIfMissing(animations[anim], LoaderUtils.defaultModelExtension)
            else:
                print(f"WARN: Body {bodyType} has no animations.")

            loseModel: str = data.get("loseModel")
            if loseModel is not None:
                loseModel = LoaderUtils.addExtensionIfMissing(loseModel, LoaderUtils.defaultModelExtension)

            skelecog: Skelecog = None
            skelecogData = data.get("skelecog")
            if skelecogData is not None:
                try:
                    skeleLoseModel = skelecogData.get("loseModel")
                    if skeleLoseModel is not None:
                        skeleLoseModel = LoaderUtils.addExtensionIfMissing(skeleLoseModel, LoaderUtils.defaultModelExtension)
                    skelecog = Skelecog(
                        LoaderUtils.addExtensionIfMissing(skelecogData["model"], LoaderUtils.defaultModelExtension),
                        skeleLoseModel
                    )
                except KeyError as e:
                    print(f"Body {bodyType} skelecog is missing required field {e.args[0]}, skipping.")

            Bodies[bodyType] = Body(
                LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
                LoaderUtils.addExtensionIfMissing(data["headsModel"], LoaderUtils.defaultModelExtension),
                animations=animations,
                loseModel=loseModel,
                skelecog=skelecog,
                loseAnim=data.get("loseAnim", "lose"),
                sizeFactor=data.get("sizeFactor", 1)
            )
        except KeyError as e:
            print(f"Body {bodyType} is missing required field {e.args[0]}.")

