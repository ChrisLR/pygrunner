from pygrunner.core import components, Layer
from pygrunner.core.objecttypes import GameObject
from pygrunner.gamedata.recipes.base import Recipe


class Collectible(Recipe):
    name = ""
    animations = {}
    move_speed = 1
    jump_height = 1
    initial_stock = 10

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = cls._set_animations(sprite_loader)
        display = components.Display(Layer.middle, pyglet_animations)
        location = components.Location(0, 0)
        physics = components.Physics()
        size = components.Size()
        actor = GameObject(cls.name, display, location, physics, size, cls)

        return actor

    @classmethod
    def reset(cls, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()