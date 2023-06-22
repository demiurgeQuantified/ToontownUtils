from panda3d.core import NodePath, Vec4, Texture

from direct.actor.Actor import Actor

from toontown_utils import TemplateManager

from toontown_utils.toon.ToonSpecies import ToonSpecies
from toontown_utils.toon.ToonPart import ToonPart
from toontown_utils.toon.ToonHead import ToonHead


class ToonActor(Actor):
    def __init__(self, species: ToonSpecies | str = None,
                 head: str | ToonHead = None, torso: str | ToonPart = None, legs: ToonPart | str = None,
                 clothingType: str = "skirt", eyelashes: bool = False) -> None:
        Actor.__init__(self)
        self.species: ToonSpecies = species
        self.clothingType = clothingType
        self.headType = head
        self.torsoType = torso
        self.legsType = legs

        self.head: NodePath = None
        self.muzzles: dict[str, NodePath] = {}
        self.torso: NodePath = None
        self.legs: NodePath = None

        self._headColor = Vec4(1, 1, 1, 1)
        self._torsoColor = Vec4(1, 1, 1, 1)
        self._legsColor = Vec4(1, 0, 0, 1)
        self._glovesColor = Vec4(1, 1, 1, 1)

        self._topTexture: Texture = None
        self._sleeveTexture: Texture = None
        self._bottomTexture: Texture = None
        self._topColor = Vec4(1, 1, 1, 1)
        self._bottomColor = Vec4(1, 1, 1, 1)

        self.createModel(self.species, self.headType, self.torsoType, self.legsType)

    def createModel(self, species: ToonSpecies, head: str, torso: ToonPart, legs: ToonPart) -> None:
        self.createHead(species.heads[head])
        self.muzzles["neutral"].unstash()
        self.createTorso(torso)
        self.createLegs(legs)
        
        self.reapplyColors()

    def createLegs(self, legsPart: ToonPart) -> None:
        if self.legs is not None:
            self.legs.removeNode()

        self.loadModel(legsPart.model, "legs")
        self.loadAnims(legsPart.anims, "legs")
        self.legs = self.getPart("legs")

        self.legs.find("**/shoes").stash()
        self.legs.find("**/boots_short").stash()
        self.legs.find("**/boots_long").stash()

        if self.torso is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))

    def createTorso(self, torsoPart: ToonPart) -> None:
        if self.torso is not None:
            self.torso.removeNode()

        self.loadModel(torsoPart.model, "torso")
        self.loadAnims(torsoPart.anims, "torso")
        self.torso = self.getPart("torso")

        if self.legs is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))
        if self.head is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def createHead(self, head: ToonHead) -> None:
        if self.head is not None:
            self.head.removeNode()

        self.loadModel(head.model, "head")
        if head.anims is not None:
            self.loadAnims(head.anims, "head")
        self.head: NodePath = self.getPart("head")

        if head.parts is not None:
            self.head.getChildren()[0].getChildren().stash()
            for part in head.parts:
                self.head.find(f"**/{part};+s").unstash()

        if head.muzzles is not None:
            self.muzzles = {}
            for muzzle, part in head.muzzles.items():
                self.muzzles[muzzle] = self.head.find(f"**/{part};+s")

        if self.torso is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def reapplyColors(self) -> None:
        for pieceName in ("legs", "feet"):
            piece = self.legs.find(f"**/{pieceName}")
            piece.setColor(self.legsColor)

        for pieceName in ("arms", "neck"):
            piece = self.torso.find(f"**/{pieceName}")
            piece.setColor(self.torsoColor)

        parts = self.head.findAllMatches("**/head*")
        parts.setColor(self.headColor)

    def reapplyClothing(self) -> None:
        top: NodePath = self.torso.find("**/torso-top")
        top.setTexture(self.topTexture, 1)
        top.setColor(self.topColor)

        sleeves: NodePath = self.torso.find("**/sleeves")
        sleeves.setTexture(self.sleeveTexture, 1)
        sleeves.setColor(self.topColor)

        bottom: NodePath = self.torso.find("**/torso-bot")
        bottom.setTexture(self.bottomTexture, 1)
        bottom.setColor(self.bottomColor)

    @property
    def species(self) -> ToonSpecies:
        return self._species

    @species.setter
    def species(self, species: str | ToonSpecies):
        if isinstance(species, str):
            species = TemplateManager.Species[species]
        self._species = species

    @property
    def legsColor(self) -> Vec4:
        return self._legsColor

    @legsColor.setter
    def legsColor(self, color: Vec4) -> None:
        self._legsColor = color
        if self.legs is None:
            return
        for pieceName in ("legs", "feet"):
            piece = self.legs.find(f"**/{pieceName}")
            piece.setColor(color)

    @property
    def torsoColor(self) -> Vec4:
        return self._torsoColor

    @torsoColor.setter
    def torsoColor(self, color: Vec4) -> None:
        self._torsoColor = color
        if self.torso is None:
            return
        for pieceName in ("arms", "neck"):
            piece = self.torso.find(f"**/{pieceName}")
            piece.setColor(color)

    @property
    def headColor(self) -> Vec4:
        return self._headColor

    @headColor.setter
    def headColor(self, color: Vec4) -> None:
        self._headColor = color
        if self.head is None:
            return
        self.head.findAllMatches("**/head*").setColor(color)

    @property
    def headType(self) -> str:
        return self._headType

    @headType.setter
    def headType(self, head: str) -> None:
        self._headType = head

    @property
    def torsoType(self) -> ToonPart:
        return self._torsoType

    @torsoType.setter
    def torsoType(self, torso: str | ToonPart) -> None:
        if isinstance(torso, str):
            try:
                torso = TemplateManager.Torsos[self.clothingType][torso]
            except KeyError:
                torso = TemplateManager.Torsos["all"][torso]
        self._torsoType = torso

    @property
    def legsType(self) -> ToonPart:
        return self._legsType

    @legsType.setter
    def legsType(self, legs: str | ToonPart) -> None:
        if isinstance(legs, str):
            try:
                legs = TemplateManager.Legs[self.clothingType][legs]
            except KeyError:
                legs = TemplateManager.Legs["all"][legs]
        self._legsType = legs

    @property
    def topColor(self) -> Vec4:
        return self._topColor

    @topColor.setter
    def topColor(self, color: Vec4) -> None:
        self._topColor = color
        for pieceName in ("torso-top", "sleeves"):
            piece = self.legs.find(f"**/{pieceName}")
            piece.setColor(color)

    @property
    def bottomColor(self) -> Vec4:
        return self._topColor

    @bottomColor.setter
    def bottomColor(self, color: Vec4) -> None:
        self._topColor = color
        piece = self.legs.find("**/torso-bot")
        piece.setColor(color)

    @property
    def bottomTexture(self) -> Texture:
        return self._bottomTexture

    @bottomTexture.setter
    def bottomTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._bottomTexture = tex
        self.torso.find("**/torso-bot").setTexture(tex, 1)

    @property
    def topTexture(self) -> Texture:
        return self._topTexture

    @topTexture.setter
    def topTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._topTexture = tex
        self.torso.find("**/torso-top").setTexture(tex, 1)

    @property
    def sleeveTexture(self) -> Texture:
        return self._sleeveTexture

    @sleeveTexture.setter
    def sleeveTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._sleeveTexture = tex
        self.torso.find("**/sleeves").setTexture(tex, 1)

