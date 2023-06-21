from typing import Any

from toontown_utils import LoaderUtils
from toontown_utils.toon.ToonPart import ToonPart
from toontown_utils.toon.ToonSpecies import ToonSpecies

Species: dict[str, ToonSpecies] = {}
Legs: dict[str, dict[str, ToonPart]] = {
    "all": {},
    "shorts": {},
    "skirt": {}
}
Torsos: dict[str, dict[str, ToonPart]] = {
    "all": {},
    "shorts": {},
    "skirt": {}
}


def readFile(contents: dict[str, dict]) -> None:
    parts: dict = contents.get("parts")
    if parts is not None:
        loadAllParts(parts)

    species: dict = contents.get("species")
    if species is not None:
        loadSpecies(species)


def loadAllParts(parts: dict[str, dict[str, dict[str, Any]]]) -> None:
    areaParts = parts.get("legs")
    if areaParts is not None:
        for cat in ("all", "skirt", "shorts"):
            catData = areaParts.get(cat, None)
            if catData is None:
                continue
            loadParts(catData, Legs[cat])

    areaParts = parts.get("torsos")
    if areaParts is not None:
        for cat in ("all", "skirt", "shorts"):
            catData = areaParts.get(cat, None)
            if catData is None:
                continue
            loadParts(catData, Torsos[cat])


def loadParts(parts: dict[str, Any], partDict: dict[str, ToonPart]) -> None:
    for part, data in parts.items():
        try:
            animations = data.get("anims")
            if animations is not None:
                for anim in animations:
                    animations[anim] = LoaderUtils.addExtensionIfMissing(animations[anim], LoaderUtils.defaultModelExtension)
            else:
                print(f"WARN: ToonPart {part} has no animations.")
            partDict[part] = ToonPart(
                model=LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
                anims=animations)
        except KeyError as e:
            print(f"ToonPart {part} is missing required field {e.args[0]}.")


def loadSpecies(species: dict[str, dict[str, Any]]):
    for speciesName, data in species.items():
        try:
            Species[speciesName] = ToonSpecies(
                heads=LoaderUtils.addExtensionIfMissing(data["heads"], LoaderUtils.defaultModelExtension),
                headAnims=data.get("headAnims"),  # TODO: add extensions
                size=data.get("size", 1))
        except KeyError as e:
            print(f"Species {species} is missing required field {e.args[0]}.")
