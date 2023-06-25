from panda3d.core import NodePath, Texture
from direct.actor.Actor import Actor

from toontown_utils.cog.TemplateCog import *
from toontown_utils.cog import CogGlobals
from toontown_utils.TemplateManager import Cogs


class CogActor(Actor):
    def __init__(self, cogType: TemplateCog | str = None,
                 bodyType: CogBody = None, dept: Department = None, head: str = None,
                 skelecog=False, waiter=False, lose=False) -> None:
        """
        CogActor constructor.
        If cogType is specified, bodyType, dept and head are ignored.
        No arguments are mandatory: you can call the functions to create the model later.
        :param cogType: A cog template to copy.
        :param bodyType: The Body to read models from
        :param dept: The cog's department, used to set their body textures.
        :param head: The name of the head part in the Body's head mesh to show.
        :param skelecog: Should this cog be a skelecog?
        :param waiter: Should this cog be a waiter?
        :param lose: Should the lose model be used?
        """
        Actor.__init__(self)
        # TODO: ToonActor cleaned up all these stupid properties, CogActor should be updated to match
        self._isLose = lose
        self._isSkelecog = skelecog

        self._template: TemplateCog = cogType
        self._bodyType: CogBody = bodyType
        self.department: Department = dept

        self.head: NodePath = None
        self.medallion: NodePath = None
        self.healthMeter: NodePath = None
        self.healthMeterGlow: NodePath = None
        self.showingHeads: list[str] = []

        self._legTexture = None
        self._blazerTexture = None
        self._sleeveTexture = None
        self._tieTexture = None
        self._headTexture = None
        self._gloveColor = Vec4(1, 1, 1, 1)
        self._headColor = Vec4(1, 1, 1, 1)

        if cogType is not None:
            self.loadTemplate(cogType)
            if waiter:
                self.makeWaiter()
        elif bodyType is not None:
            self.createModel(bodyType, skelecog, lose)
            if dept is not None:
                self.setDepartmentTextures(dept)
            if head is not None:
                self.showHeadModel(head)
            else:
                self.hideHeadModels()
            if waiter:
                self.makeWaiter()

    def loadTemplate(self, template: TemplateCog | str) -> None:
        """
        Applies all the data from a template onto the actor.
        :param template: Either the template, or the string name of the template
        :return:
        """
        if isinstance(template, str):
            try:
                template = Cogs[template]
            except KeyError:
                print(f"CogActor: No such cog template {template}")
                return
        self._template = template
        self.department = template.department

        self.createModel(template.body, skelecog=self._isSkelecog, lose=self._isLose)
        self.setScale(template.size / template.body.sizeFactor)

        self.setDepartmentTextures(template.department)

        self.gloveColor = template.gloveColor

        if template.headColor is not None:
            self.headColor = template.headColor
        else:
            self.headColor = Vec4(1, 1, 1, 1)

        self.showHeadModel(template.head)

        if template.head2 is not None:
            self.showHeadModel(template.head2, False)

        self.headTexture = template.headTexture

    def createHead(self, bodyType: CogBody):
        """
        Creates the head model for the bodyType and attaches it. Cleans up an existing head if necessary.
        :param bodyType:
        :return:
        """
        if self.head is not None:
            self.head.removeNode()
        self.head = loader.loadModel(bodyType.headsModel).getChild(0)
        self.head.reparentTo(self.find("**/joint_head"))

    def createModel(self, bodyType: CogBody, skelecog=False, lose=False) -> None:
        """
        Creates the appropriate model and all subparts for the given Body. Also cleans up the previous model if necessary.
        :param bodyType: The Body that stores the wanted models
        :param skelecog: Should the skelecog model be used?
        :param lose: Should the lose model be used? (respects skelecog)
        :return:
        """
        currModel = self.getPart("modelRoot")
        if currModel is not None:
            currModel.removeNode()
            if self.head is not None:
                self.head.removeNode()
                self.head = None

        self._bodyType = bodyType
        if not lose:
            if not skelecog:
                self.loadModel(bodyType.model)
                if self.head is None:
                    self.createHead(bodyType)
            else:
                self.loadModel(bodyType.skelecog.model)

            self.createHealthMeter()
            if self.department is not None:
                self.createMedallion(self.department)

            if bodyType.animations is not None:
                self.loadAnims(bodyType.animations)
        else:
            if not skelecog:
                self.loadModel(bodyType.loseModel)
                if self.head is None:
                    self.createHead(bodyType)
            else:
                self.loadModel(bodyType.skelecog.loseModel)

            if bodyType.animations is not None and bodyType.loseAnim is not None:
                self.loadAnims({bodyType.loseAnim: bodyType.animations[bodyType.loseAnim]})

    def createMedallion(self, dept: Department) -> None:
        """
        Creates the medallion (department icon) for the given department and attaches it to the cog.
        Cleans up an existing medallion if necessary.
        :param dept:
        :return:
        """
        if self._isLose:
            return
        if self.medallion is not None:
            self.medallion.removeNode()
        medallion = dept.medallion
        attachment = self.find("**/joint_attachMeter")

        medallionModel = loader.loadModel(medallion.model)
        if medallion.part is not None:
            self.medallion = medallionModel.find(f"**/{medallion.part}").copyTo(attachment)
        else:
            self.medallion = medallionModel.copyTo(attachment)

        self.medallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        if medallion.color is not None:
            self.medallion.setColor(medallion.color)
        medallionModel.removeNode()

    def createHealthMeter(self) -> None:
        """
        Creates the health meter and attaches it. Cleans up an existing health meter if necessary.
        :return:
        """
        if self._isLose:
            return
        if self.healthMeter is not None:
            self.healthMeter.removeNode()
            self.healthMeterGlow.removeNode()
        model = loader.loadModel(CogGlobals.healthMeterModel)
        button = model.find("**/minnieCircle").copyTo(self.find("**/joint_attachMeter"))
        button.setScale(3)
        button.setH(180)
        button.setColor(CogGlobals.HealthColor["off"])
        button.hide()
        self.healthMeter = button

        glow = loader.loadModel(CogGlobals.healthMeterGlowModel)
        glow.reparentTo(button)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(0.25, 1, 0.25, 0.5)
        self.healthMeterGlow = glow

        model.removeNode()

    def becomeLoseActor(self) -> None:
        """
        Switches the cog to its lose model, which is a special model used for the defeated explosion animation.
        :return:
        """
        if self._isLose:
            print("CogActor: becomeLoseActor() called, but already in the lose state")
            return
        self._isLose = True
        self.medallion = None
        self.healthMeter = None
        self.healthMeterGlow = None

        self.createModel(self._bodyType, self._isSkelecog, True)
        self.reapplyTextures()
        self.reapplyShowingHeads()

    def becomeNormalActor(self) -> None:
        """
        Switches the cog back to its normal model from its lose model.
        :return:
        """
        if not self._isLose:
            print("CogActor: becomeNormal() called but already normal")
            return
        self._isLose = False

        self.createModel(self._bodyType, self._isSkelecog, False)
        self.reapplyTextures()
        self.reapplyShowingHeads()

        if self.department is not None:
            self.createMedallion(self.department)
        self.createHealthMeter()

    def setSkelecog(self, skelecog: bool) -> None:
        """
        Sets whether the cog is a skelecog. This will regenerate the model.
        :param skelecog:
        :return:
        """
        if self._isSkelecog == skelecog:
            return
        self._isSkelecog = skelecog

        self.createModel(self._bodyType, skelecog, self._isLose)
        self.reapplyTextures()
        if not skelecog:
            self.reapplyShowingHeads()
        if not self._isLose:
            attachment = self.find("**/joint_attachMeter")
            self.medallion.reparentTo(attachment)
            self.healthMeter.reparentTo(attachment)

    def setHealthMeterColor(self, color: Vec4, glowColor: Vec4 = None) -> None:
        """
        Sets the color of the cog's health meter to the given color.
        :param color: The color to set the meter to
        :param glowColor: The color to set the meter's glow to. If not specified, it will be calculated in a way that
        will match the original appearance, but might look strange on non-standard colors.
        :return:
        """
        if self._isLose:
            return
        self.healthMeter.setColor(color)
        if glowColor is None:
            glowColor = Vec4(max(color.x, 0.25), max(color.y, 0.25), max(color.z, 0.25), color.w * 0.5)
        self.healthMeterGlow.setColor(glowColor)

    def reapplyTextures(self) -> None:
        """
        Reapplies the body textures to the body. You don't usually need to call this unless you swap the model manually.
        :return:
        """
        if not self._isSkelecog:
            self.find("**/legs").setTexture(self.legTexture, 1)
            self.find("**/torso").setTexture(self.blazerTexture, 1)
            self.find("**/arms").setTexture(self.sleeveTexture, 1)
            if self.headTexture is not None:
                self.head.setTexture(self.headTexture, 1)
            self.find("**/hands").setColor(self.gloveColor)
            self.head.setColor(self.headColor)
        else:
            self.find("**/tie").setTexture(self.tieTexture, 1)

    def reapplyShowingHeads(self) -> None:
        """
        Reapplies the showing heads to the body. You don't usually need to call this unless you swap the model manually.
        :return:
        """
        if self._isSkelecog:
            return
        headModels = self.showingHeads.copy()
        self.hideHeadModels()
        for head in headModels:
            self.showHeadModel(head, False)

    def hideHeadModels(self) -> None:
        """
        Hides all the parts of the head model.
        :return:
        """
        self.showingHeads.clear()
        if self._isSkelecog:
            return
        self.head.getChildren().stash()

    def showHeadModel(self, wantedHead: str, hideOthers: bool = True) -> None:
        """
        Shows a specific head part.
        :param wantedHead: The name of the part to show
        :param hideOthers: Hide all other head parts?
        :return:
        """
        if hideOthers:
            self.hideHeadModels()
        self.showingHeads.append(wantedHead)
        if self._isSkelecog:
            return
        head = self.head.find(f"@@{wantedHead}")
        if not head.isEmpty():
            head.unstash()

    def setBodyTextures(self, legTex: Texture | str, blazerTex: Texture | str, sleeveTex: Texture | str,
                        tieTex: Texture | str = None):
        """
        Shorthand for changing all of the body's textures at once.
        :param legTex:
        :param blazerTex:
        :param sleeveTex:
        :param tieTex:
        :return:
        """
        self.legTexture = legTex
        self.blazerTexture = blazerTex
        self.sleeveTexture = sleeveTex
        if tieTex is not None:
            self.tieTexture = tieTex

    def setDepartmentTextures(self, dept: Department) -> None:
        """
        Sets the body textures to those of the given department. Does not update the medallion.
        :param dept:
        :return:
        """
        self.setBodyTextures(dept.leg, dept.blazer, dept.sleeve, dept.tie)

    def makeWaiter(self) -> None:
        """
        Sets the body textures to the waiter textures (configured in CogGlobals)
        :return:
        """
        self.setBodyTextures(CogGlobals.waiterLeg, CogGlobals.waiterBlazer, CogGlobals.waiterSleeve)

    @property
    def legTexture(self) -> Texture:
        return self._legTexture

    @legTexture.setter
    def legTexture(self, tex: str | Texture) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._legTexture = tex
        if not self._isSkelecog:
            self.find("**/legs").setTexture(tex, 1)

    @property
    def blazerTexture(self) -> Texture:
        return self._blazerTexture

    @blazerTexture.setter
    def blazerTexture(self, tex: str | Texture) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._blazerTexture = tex
        if not self._isSkelecog:
            self.find("**/torso").setTexture(tex, 1)

    @property
    def sleeveTexture(self) -> Texture:
        return self._sleeveTexture

    @sleeveTexture.setter
    def sleeveTexture(self, tex: str | Texture) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._sleeveTexture = tex
        if not self._isSkelecog:
            self.find("**/arms").setTexture(tex, 1)

    @property
    def tieTexture(self) -> Texture:
        return self._tieTexture

    @tieTexture.setter
    def tieTexture(self, tex: str | Texture) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._tieTexture = tex
        if self._isSkelecog:
            self.find("**/tie").setTexture(tex, 1)

    @property
    def headTexture(self) -> Texture | None:
        return self._headTexture

    @headTexture.setter
    def headTexture(self, tex: str | Texture | None) -> None:
        if tex is None:
            self._headTexture = None
            if not self._isSkelecog:
                self.head.clearTexture()
            return
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self._headTexture = tex
        if not self._isSkelecog:
            self.head.setTexture(tex, 1)

    @property
    def gloveColor(self) -> Vec4:
        return self._gloveColor

    @gloveColor.setter
    def gloveColor(self, color: Vec4) -> None:
        self._gloveColor = color
        if not self._isSkelecog:
            self.find("**/hands").setColor(color)

    @property
    def headColor(self) -> Vec4:
        return self._headColor

    @headColor.setter
    def headColor(self, color: Vec4) -> None:
        self._headColor = color
        if self.head is not None:
            self.head.setColor(color)
