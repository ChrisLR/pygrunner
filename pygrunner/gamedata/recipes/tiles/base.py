from pygrunner.core import components, Layer
from pygrunner.core.objecttypes import StaticObject
from pygrunner.gamedata.recipes.base import Recipe


class Tile(Recipe):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.background

    def create(self, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = self._set_animations(sprite_loader)
        display = components.Display(self.layer, pyglet_animations)
        location = components.Location(0, 0)
        physics = components.Physics()
        size = components.Size()
        tile = StaticObject(self.name, display, location, physics, size)

        return tile

    def reset(self, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()
