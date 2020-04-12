from pygrunner.core import components, Layer
from pygrunner.core.objecttypes import GameObject
from pygrunner.gamedata.recipes.base import Recipe


class Container(Recipe):
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
        physics.affected_by_gravity = False
        physics.affected_by_velocity = False
        size = components.Size()
        game_object = GameObject(cls.name, display, location, physics, size, cls)

        return game_object

    @classmethod
    def reset(cls, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()
        game_object.collectible.reset()
