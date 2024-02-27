from typing import Any

from panda3d.core import Vec4

from toontown_utils import LoaderUtils

from toontown_utils.cog.TemplateCog import TemplateCog
from toontown_utils.cog.Department import Department, Medallion
from toontown_utils.cog.CogBody import CogBody, Skelecog

Cogs: dict[str, TemplateCog] = {}
Departments: dict[str, Department] = {}
Bodies: dict[str, CogBody] = {}


def loadFromJson(contents: dict[str, dict]):
    """
    Loads definitions from a ToontownJSON file

    :param contents: ToontownJSON cog file root object
    :return:
    """
    departments: dict = contents.get("departments")
    if departments is not None:
        loadDepartments(departments)

    bodies: dict = contents.get("bodies")
    if bodies is not None:
        loadBodies(bodies)

    cogs: dict = contents.get("cogs")
    if cogs is not None:
        loadCogs(cogs)


def getHeadColor(data: dict[str, list[float]]) -> Vec4 | None:
    """
    Returns the processed head colour from a ToontownJSON cog object

    :param data: The ToontownJSON cog object
    :return: The resulting colour
    """
    headColor = data.get("headColor")
    if headColor is None:
        return None
    return LoaderUtils.readColor(headColor)


def getGloveColor(data: dict[str, list[float]]) -> Vec4 | None:
    """
    Returns the processed glove colour from a ToontownJSON cog object

    :param data: The ToontownJSON cog object
    :return: The resulting colour, or none if none is defined
    """
    gloveColor: list = data.get("gloveColor")
    if gloveColor is None:
        return None
    return LoaderUtils.readColor(gloveColor)


def loadCog(name: str, data: dict[str, Any]):
    """
    Creates a TemplateCog from a ToontownJSON cog definition and adds it to the Cogs dictionary

    :param name: Name of the cog type
    :param data: ToontownJSON cog definition
    :return:
    """
    try:
        deptName: str = data["department"]
    except KeyError:
        raise Exception(f"Cog {name} has no department set!")

    try:
        dept: Department = Departments[deptName]
    except KeyError:
        raise Exception(f"Cog {name} is member of unknown department {deptName}")

    try:
        body: str = data["body"]
    except KeyError:
        raise Exception(f"Cog {name} has no body set!")

    try:
        bodyType: CogBody = Bodies[body]
    except KeyError:
        raise Exception(f"Cog {name} has unknown body {body}")

    try:
        headTexture: str = data.get("headTexture")
        if headTexture is not None:
            headTexture = LoaderUtils.addExtensionIfMissing(headTexture, LoaderUtils.defaultTextureExtension)

        Cogs[name] = TemplateCog(
            name=name,
            department=dept,
            body=bodyType,
            size=data["size"],
            gloveColor=getGloveColor(data) or dept.gloveColor,
            head=data["head"],
            head2=data.get("head2"),
            headTexture=headTexture,
            headColor=getHeadColor(data)
        )
    except KeyError as e:
        raise Exception(f"Cog {name} is missing required property {e.args[0]}.")


def loadCogs(cogs: dict[str, Any]):
    """
    Loads cog definitions from a ToontownJSON formatted cogs dictionary and adds them to the Cogs dictionary

    :param cogs: ToontownJSON cogs object
    :return:
    """
    for name, data in cogs.items():
        try:
            loadCog(name, data)
        except Exception as e:
            raise Exception("Error loading cog definitions: " + str(e))


def createMedallion(data: dict[str, Any]) -> Medallion:
    """
    Creates and returns a Medallion from a ToontownJSON medallion definition

    :param data: ToontownJSON medallion definition
    :return: the resulting Medallion
    """
    color = data.get("color")
    if color is not None:
        color = LoaderUtils.readColor(color)

    return Medallion(
        model=LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
        color=color,
        part=data.get("part")
    )


def loadDepartment(name: str, data: dict[str, Any]):
    """
    Creates a Department from a ToontownJSON department definition and adds it to the Departments dictionary

    :param name: Name of the department
    :param data: ToontownJSON department definition
    :return:
    """
    try:
        gloveColor = data.get("gloveColor")
        if gloveColor is not None:
            gloveColor = LoaderUtils.readColor(gloveColor)
        else:
            gloveColor = Vec4(0, 0, 0, 1)

        Departments[name] = Department(
            LoaderUtils.addExtensionIfMissing(data["blazer"], LoaderUtils.defaultTextureExtension),
            LoaderUtils.addExtensionIfMissing(data["leg"], LoaderUtils.defaultTextureExtension),
            LoaderUtils.addExtensionIfMissing(data["sleeve"], LoaderUtils.defaultTextureExtension),
            LoaderUtils.addExtensionIfMissing(data["tie"], LoaderUtils.defaultTextureExtension),
            medallion=createMedallion(data["medallion"]),
            gloveColor=gloveColor
        )
    except KeyError as e:
        raise Exception(f"Department {name} is missing required field {e.args[0]}.")


def loadDepartments(departments: dict[str, Any]):
    """
    Loads department definitions from a ToontownJSON formatted departments dictionary and adds them to the Departments
    dictionary

    :param departments: ToontownJSON formatted departments object
    :return:
    """
    for name, data in departments.items():
        try:
            loadDepartment(name, data)
        except Exception as e:
            raise Exception("Error loading department definitions: " + str(e))


def createSkelecog(data: dict[str, Any]) -> Skelecog:
    """
    Creates and returns a skelecog from a ToontownJSON skelecog definition

    :param data: ToontownJSON skelecog definition
    :return: the resulting Skelecog
    """
    loseModel: str | None = data.get("loseModel")
    if loseModel is not None:
        loseModel = LoaderUtils.addExtensionIfMissing(loseModel, LoaderUtils.defaultModelExtension)

    return Skelecog(
        LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
        loseModel
    )


def loadBody(name: str, data: dict[str, Any]):
    """
    Creates a CogBody from a ToontownJSON cog body definition and adds it to the Bodies dictionary

    :param name: Name of the body
    :param data: ToontownJSON cog body definition
    :return:
    """
    try:
        animations: dict = data.get("animations")
        if animations is not None:
            LoaderUtils.addExtensions(animations, LoaderUtils.defaultModelExtension)
        else:
            raise Exception(f"Body {name} has no animations.")

        loseModel: str | None = data.get("loseModel")
        if loseModel is not None:
            loseModel = LoaderUtils.addExtensionIfMissing(loseModel, LoaderUtils.defaultModelExtension)

        skelecog: Skelecog | None = None
        skelecogData = data.get("skelecog")
        if skelecogData is not None:
            skelecog = createSkelecog(skelecogData)

        Bodies[name] = CogBody(
            LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
            LoaderUtils.addExtensionIfMissing(data["headsModel"], LoaderUtils.defaultModelExtension),
            animations=animations,
            loseModel=loseModel,
            skelecog=skelecog,
            loseAnim=data.get("loseAnim", "lose"),
            sizeFactor=data.get("sizeFactor", 1)
        )
    except KeyError as e:
        raise Exception(f"Body {name} is missing required field {e.args[0]}.")


def loadBodies(bodies: dict[str, Any]):
    """
    Loads cog body definitions from a ToontownJSON formatted departments dictionary and adds them to the Bodies
    dictionary

    :param bodies: ToontownJSON formatted bodies object
    :return:
    """
    for name, data in bodies.items():
        try:
            loadBody(name, data)
        except Exception as e:
            raise Exception("Error loading cog body definitions: " + str(e))
