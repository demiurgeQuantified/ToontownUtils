from __future__ import annotations
from typing import TYPE_CHECKING
import json

from toontown_utils.cog import CogLoader

from toontown_utils.toon import ToonLoader
if TYPE_CHECKING:
    from toontown_utils.toon.ToonPart import ToonPart

Cogs = CogLoader.Cogs
Departments = CogLoader.Departments
Bodies = CogLoader.Bodies

Legs = ToonLoader.Legs
Torsos = ToonLoader.Torsos
Species = ToonLoader.Species


def getLegs(type: str, clothingType: str = "all") -> ToonPart:
    """
    Gets a legs definition by its name

    :param type: Name of the part
    :param clothingType: Type of clothing (shorts/skirt)
    :return:
    """
    try:
        return Legs[clothingType][type]
    except KeyError:
        # this just does the same thing twice if all was originally passed
        return Legs["all"][type]


def getTorso(type: str, clothingType: str = "all") -> ToonPart:
    """
    Gets a torso definition by its name

    :param type: Name of the part
    :param clothingType: Type of clothing (shorts/skirt)
    :return:
    """
    try:
        return Torsos[clothingType][type]
    except KeyError:
        return Torsos["all"][type]


def readFile(path: str, schema: str = None):
    """
    Reads a ToontownJSON file and loads definitions from it

    :param path: The path of file to read
    :param schema: Valid values are 'toon' and 'cog'
    :return:
    """
    file = open(path, 'r', encoding='utf-8')

    try:
        contents: dict = json.loads(file.read())
    finally:
        file.close()

    # TODO: i don't really like the way i did this, toons and cogs should just use the same schema
    if schema is None:
        schema = contents.get("$schema")
        if schema == "toonschema.json":
            schema = "toon"
        elif schema == "cogschema.json":
            schema = "cog"
        else:
            raise Exception(f"Could not auto-detect schema of {path}")

    if schema == "toon":
        ToonLoader.readFile(contents)
    elif schema == "cog":
        CogLoader.loadFromJson(contents)
