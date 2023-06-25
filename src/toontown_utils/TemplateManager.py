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


def getLegs(type: str, clothingType: str) -> ToonPart:
    try:
        return Legs[clothingType][type]
    except KeyError:
        return Legs["all"][type]


def getTorso(type: str, clothingType: str) -> ToonPart:
    try:
        return Torsos[clothingType][type]
    except KeyError:
        return Torsos["all"][type]


def loadFile(path: str, schema: str = None) -> bool:
    try:
        file = open(path, 'r', encoding='utf-8')
    except OSError:
        print(f"TemplateManager ERROR: Failed to open {path}")
        return False

    try:
        contents: dict = json.loads(file.read())
    except json.JSONDecodeError:
        file.close()
        print(f"TemplateManager ERROR: {path} is not a valid JSON file.")
        return False

    file.close()

    if schema is None:
        schema = contents.get("$schema")
        if schema == "toonschema.json":
            schema = "toon"
        elif schema == "cogschema.json":
            schema = "cog"
        else:
            print(f"TemplateManager ERROR: Could not auto-detect schema of {path}")
            return False

    if schema == "toon":
        ToonLoader.readFile(contents)
    elif schema == "cog":
        CogLoader.readFile(contents)

    return True
