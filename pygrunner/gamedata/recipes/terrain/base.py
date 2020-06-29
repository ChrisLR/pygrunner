from pyg2d.core import components, Layer
from pyg2d.core.objecttypes import StaticObject
from pygrunner.gamedata.recipes.base import Recipe


class Terrain(Recipe):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.middle

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = cls._set_animations(sprite_loader)
        display = components.Display(cls.layer, pyglet_animations)
        location = components.Location(0, 0)
        physics = components.Physics(solid=False)
        size = components.Size()
        tile = StaticObject(cls.name, display, location, physics, size, cls)

        return tile

    @classmethod
    def reset(cls, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()
