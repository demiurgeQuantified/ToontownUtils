from panda3d.core import NodePath, Vec4

from direct.actor.Actor import Actor

from toontown_utils.toon.ToonSpecies import ToonSpecies
from toontown_utils.toon.ToonPart import ToonPart


class ToonActor(Actor):
    def __init__(self, species: ToonSpecies = None, head: str = None, body: str = None, legs: str = None) -> None:
        Actor.__init__(self)
        self.species: ToonSpecies = species
        self.headType: str = head
        self.bodyType: str = body
        self.legsType: str = legs

        self.headColor = Vec4(0, 0, 0, 1)
        self.bodyColor = Vec4(0, 0, 0, 1)
        self.legsColor = Vec4(0, 0, 0, 1)
        self.glovesColor = Vec4(0, 0, 0, 1)

        self.head: NodePath = None
        self.body: NodePath = None
        self.legs: NodePath = None

    def createModel(self, species: ToonSpecies, head: str, body: ToonPart, legs: ToonPart) -> None:
        self.createHead(species.heads[head])
        self.createBody(body)
        self.createLegs(legs)

    def createLegs(self, model: str):
        if self.legs is not None:
            self.legs.removeNode()
        self.loadModel(model, "legs")
        self.legs = self.getPart("legs")
        if self.body is not None:
            self.body.reparentTo(self.legs.find("**/joint_hips"))

        self.legs.find("**/shoes").stash()
        self.legs.find("**/boots_short").stash()
        self.legs.find("**/boots_long").stash()

    def createBody(self, model: str):
        if self.body is not None:
            self.body.removeNode()
        self.loadModel(model, "body")
        self.body = self.getPart("body")
        if self.legs is not None:
            self.body.reparentTo(self.legs.find("**/joint_hips"))
        if self.head is not None:
            self.head.reparentTo(self.body.find("**/def_head"))

    def createHead(self, model: str):
        if self.head is not None:
            self.head.removeNode()
        self.loadModel(model, "head")
        self.head = self.getPart("head")
        if self.body is not None:
            self.head.reparentTo(self.body.find("**/def_head"))

    @property
    def headType(self) -> str:
        return self._headType

    @headType.setter
    def headType(self, new) -> None:
        self._headType = new

    @property
    def bodyType(self) -> str:
        return self._headType

    @bodyType.setter
    def bodyType(self, new) -> None:
        self._headType = new

    @property
    def legsType(self) -> str:
        return self._headType

    @legsType.setter
    def legsType(self, new) -> None:
        self._headType = new
