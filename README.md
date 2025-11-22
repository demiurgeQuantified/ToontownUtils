> [!WARNING]
> This project has been archived and will not see any further development. I do still see a use for something like this, but with more experience I now see fundamental issues with the approach and style used in these projects.
# Toontown Utils
A package for Panda3D that streamlines the usage of Toontown Online assets, so that fan projects (games, videos, etc)
can easily use them.
## Features
### ToonActors and CogActors
ToonActors and CogActors give a simple syntax to creating and modifying Toontown's character models. Creating characters
now only takes a few lines of code, and manipulating them can be done with simple API calls.

---
## ToontownJSON
Though optional, Toontown Utils is primarily intended for use with
[ToontownJSON](https://github.com/demiurgeQuantified/ToontownJSON). ToontownJSON provides data on the vanilla cogs and
toon parts. Its schema can also be used to add custom cogs, species and body parts.

```python
from toontown_utils import TemplateManager
from toontown_utils.cog.CogActor import CogActor
from toontown_utils.toon.ToonActor import ToonActor

TemplateManager.readFile("cog.json")

cog = CogActor(cogType="ColdCaller")
cog.reparentTo(render)
cog.loop("neutral")

TemplateManager.readFile("toon.json")

toon = ToonActor(species="cat", head="ls", torso="m", legs="s", clothingType="skirt", eyelashes=True)
toon.reparentTo(render)
toon.setX(5)
toon.loop("neutral")
```
Without ToontownJSON, the syntax is much uglier, as models, animations, etc must all be defined in code before they are
used.
