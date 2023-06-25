from typing import Any

from toontown_utils import LoaderUtils
from toontown_utils.toon.ToonPart import ToonPart
from toontown_utils.toon.ToonSpecies import ToonSpecies
from toontown_utils.toon.ToonHead import ToonHead, Eyelashes

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
                LoaderUtils.addExtensions(animations, LoaderUtils.defaultModelExtension)
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
            heads: dict[str, ToonHead] = {}
            for head, headData in data["heads"].items():
                try:
                    heads[head] = loadHead(headData)
                except KeyError as e:
                    print(f"{speciesName} head {head} is missing required field {e.args[0]}.")

            Species[speciesName] = ToonSpecies(
                heads=heads,
                size=data.get("size", 1)
            )
        except KeyError as e:
            print(f"Species {speciesName} is missing required field {e.args[0]}.")


def loadHead(data: dict[str, Any]) -> ToonHead:
    anims = data.get("anims")
    if anims is not None:
        LoaderUtils.addExtensions(anims, LoaderUtils.defaultModelExtension)

    extraMuzzles = {}
    extraMuzzlesRaw = data.get("extraMuzzles")
    if extraMuzzlesRaw is not None:
        for modelName, parts in extraMuzzlesRaw.items():
            modelName = LoaderUtils.addExtensionIfMissing(modelName, LoaderUtils.defaultModelExtension)
            extraMuzzles[modelName] = parts

    eyelashModel = LoaderUtils.addExtensionIfMissing(data["eyelashes"].get("model"), LoaderUtils.defaultModelExtension)

    eyelashes = Eyelashes(
        model=eyelashModel,
        open=data["eyelashes"]["open"],
        closed=data["eyelashes"]["closed"]
    )

    partData = data["parts"]

    return ToonHead(
        model=LoaderUtils.addExtensionIfMissing(data["model"], LoaderUtils.defaultModelExtension),
        colorParts=partData["color"],
        leftPupil=partData["pupil_L"],
        rightPupil=partData["pupil_R"],
        eyes=partData["eyes"],
        keepParts=partData.get("keep"),
        keepAllParts=data.get("keepAllParts", False),
        extraMuzzles=extraMuzzles,
        muzzles=data.get("muzzles"),
        eyelashes=eyelashes,
        anims=anims
    )

