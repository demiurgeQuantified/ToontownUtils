from panda3d.core import NodePath, Vec4

from direct.actor.Actor import Actor

from toontown_utils.toon.ToonSpecies import ToonSpecies
from toontown_utils.toon.ToonPart import ToonPart


class ToonActor(Actor):
    def __init__(self, species: ToonSpecies = None, head: str = None, torso: str = None, legs: str = None) -> None:
        Actor.__init__(self)
        self.species: ToonSpecies = species
        self.headType: str = head
        self.torsoType: str = torso
        self.legsType: str = legs

        self.head: NodePath = None
        self.torso: NodePath = None
        self.legs: NodePath = None

        self.headColor = Vec4(1, 1, 1, 1)
        self.torsoColor = Vec4(1, 1, 1, 1)
        self.legsColor = Vec4(1, 0, 0, 1)
        self.glovesColor = Vec4(1, 1, 1, 1)

    def createModel(self, species: ToonSpecies, head: str, torso: ToonPart, legs: ToonPart) -> None:
        self.createHead(species.heads[head])
        self.createTorso(torso)
        self.createLegs(legs)
        self.reapplyColors()

    def createLegs(self, model: str) -> None:
        if self.legs is not None:
            self.legs.removeNode()
        self.loadModel(model, "legs")
        self.legs = self.getPart("legs")
        if self.torso is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))

        self.legs.find("**/shoes").stash()
        self.legs.find("**/boots_short").stash()
        self.legs.find("**/boots_long").stash()

    def createTorso(self, model: str) -> None:
        if self.torso is not None:
            self.torso.removeNode()
        self.loadModel(model, "torso")
        self.torso = self.getPart("torso")
        if self.legs is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))
        if self.head is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def createHead(self, model: str) -> None:
        if self.head is not None:
            self.head.removeNode()
        self.loadModel(model, "head")
        self.head = self.getPart("head")
        if self.torso is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def reapplyColors(self) -> None:
        for pieceName in ('legs', 'feet'):
            piece = self.legs.find('**/%s;+s' % pieceName)
            piece.setColor(self.legsColor)

        for pieceName in ('arms', 'neck'):
            piece = self.torso.find('**/' + pieceName)
            piece.setColor(self.torsoColor)

        parts = self.head.findAllMatches('**/head*')
        parts.setColor(self.headColor)

    @property
    def legsColor(self) -> Vec4:
        return self._legsColor

    @legsColor.setter
    def legsColor(self, color: Vec4) -> None:
        self._legsColor = color
        if self.legs is None:
            return
        for pieceName in ('legs', 'feet'):
            piece = self.legs.find('**/%s;+s' % pieceName)
            piece.setColor(color)

    @property
    def torsoColor(self) -> Vec4:
        return self._torsoColor

    @torsoColor.setter
    def torsoColor(self, color: Vec4) -> None:
        self._torsoColor = color
        if self.torso is None:
            return
        for pieceName in ('arms', 'neck'):
            piece = self.torso.find('**/' + pieceName)
            piece.setColor(color)

    @property
    def headColor(self) -> Vec4:
        return self._headColor

    @headColor.setter
    def headColor(self, color: Vec4) -> None:
        self._headColor = color
        if self.head is None:
            return
        self.head.findAllMatches('**/head*').setColor(color)

    @property
    def headType(self) -> str:
        return self._headType

    @headType.setter
    def headType(self, head: str) -> None:
        self._headType = head

    @property
    def torsoType(self) -> str:
        return self._torsoType

    @torsoType.setter
    def torsoType(self, torso: str) -> None:
        self._torsoType = torso

    @property
    def legsType(self) -> str:
        return self._legsType

    @legsType.setter
    def legsType(self, legs: str) -> None:
        self._legsType = legs
