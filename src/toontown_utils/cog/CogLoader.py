from typing import Any

from panda3d.core import Vec4

from toontown_utils import LoaderUtils

from toontown_utils.cog.TemplateCog import TemplateCog
from toontown_utils.cog.Department import Department, Medallion
from toontown_utils.cog.CogBody import CogBody, Skelecog

Cogs: dict[str, TemplateCog] = {}
Departments: dict[str, Department] = {}
Bodies: dict[str, CogBody] = {}


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
            bodyType: CogBody = Bodies[body]
        except KeyError:
            print(f"Cog {cog} has unknown body {body}")
            continue

        try:
            headColor = LoaderUtils.readColor(data.get("headColor"))

            gloveColor: list | Vec4 = data.get("gloveColor", dept.gloveColor)
            if gloveColor is None:
                gloveColor = Vec4(0, 0, 0, 1)
                print(
                    f"Cog {cog} does not have a gloveColor set, and {deptName} does not have a default glove color.")
            if isinstance(gloveColor, list):
                gloveColor = LoaderUtils.readColor(gloveColor)

            headTexture = LoaderUtils.addExtensionIfMissing(data.get("headTexture"), LoaderUtils.defaultTextureExtension)

            Cogs[cog] = TemplateCog(
                name=cog,
                department=dept,
                body=bodyType,
                size=data["size"],
                gloveColor=gloveColor,
                head=data["head"],
                head2=data.get("head2"),
                headTexture=headTexture,
                headColor=headColor
            )
        except KeyError as e:
            print(f"Cog {cog} is missing required field {e.args[0]}.")


def loadDepartments(depts: dict[str, Any]) -> None:
    for dept, data in depts.items():
        try:
            gloveColor = LoaderUtils.readColor(data.get("gloveColor"))
            medallionColor = LoaderUtils.readColor(data["medallion"].get("color"))

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
                LoaderUtils.addExtensions(animations, LoaderUtils.defaultModelExtension)
            else:
                print(f"WARN: Body {bodyType} has no animations.")

            loseModel = LoaderUtils.addExtensionIfMissing(data.get("loseModel"), LoaderUtils.defaultModelExtension)

            skelecog: Skelecog = None
            skelecogData = data.get("skelecog")
            if skelecogData is not None:
                try:
                    skeleLoseModel = LoaderUtils.addExtensionIfMissing(skelecogData.get("loseModel"), LoaderUtils.defaultModelExtension)
                    skelecog = Skelecog(
                        LoaderUtils.addExtensionIfMissing(skelecogData["model"], LoaderUtils.defaultModelExtension),
                        skeleLoseModel
                    )
                except KeyError as e:
                    print(f"Body {bodyType} skelecog is missing required field {e.args[0]}, skipping.")

            Bodies[bodyType] = CogBody(
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

