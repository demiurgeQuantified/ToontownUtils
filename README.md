# Toontown Utils
A package for Panda3D that aims to streamline the usage of Toontown Online's assets, so that fan projects
(games, videos, etc) can focus on implementing functionality and not putting models together correctly.
## CogActors
CogActors are a layer placed on top of regular Panda3D Actors to make creating and modifying Cog models simple calls.
To create a CogActor from scratch, a Body tuple must first be created that, at minimum, points to the model of the body
and the matching heads model.

```python
from toontown_utils.cog.CogActor import CogActor
from toontown_utils.cog.CogBody import CogBody

bodyA = CogBody(model="phase_3.5/models/char/suitA-mod.bam", headsModel="phase_4/models/char/suitA-heads.bam")

cog = CogActor(bodyType=bodyA, head="bigcheese")
```
Animations need to be loaded as usual.
```python
cog.loadAnims({"neutral": "phase_4/models/char/suitA-neutral.bam"})
cog.reparentTo(render)
cog.loop("neutral")
```
In most cases, manipulating aspects of the cog is as simple as setting attributes:
```python
cog.gloveColor = Vec4(1, 0, 0, 1)  # make sure to import Vec4 first!
cog.sleeveTexture = "phase_3.5/maps/l_sleeve.jpg"
```
Defining bodies, loading animations, setting textures etc is still very tedious, which is why loading from JSON is the
primary method of setting up cogs:
### CogJSON
Better syntax for manipulating cog models is one thing, but in most cases we only want preset cog designs. Additionally,
things like animations are rarely project specific.
[CogJSON](https://github.com/demiurgeQuantified/CogJSON) is a schema that allows easy configuration of cog templates.
It provides a dataset based on the original cogs as these are most often all that is needed.

Using CogJSON in your project is much simpler, as every detail of the cog is already defined for you.

```python
from toontown_utils import TemplateManager
from toontown_utils.cog.CogActor import CogActor

TemplateManager.loadFile("path/to/my.json")

cog = CogActor(cogType="ColdCaller")
cog.reparentTo(render)
cog.loop("neutral")
```
## ToonActors
ToonActors are not implemented yet :(