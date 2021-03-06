from pygrunner.core import components, Layer, stances
from pygrunner.core.objecttypes import Actor
from pygrunner.gamedata.recipes.base import Recipe


class Character(Recipe):
    name = ""
    animations = {}
    move_speed = 4
    jump_height = 20
    initial_stock = 10
    max_health = 4

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = cls._set_animations(sprite_loader)
        controller = components.AIController(None)
        display = components.Display(Layer.middle, pyglet_animations)
        location = components.Location(0, 0)
        physics = components.Physics()
        size = components.Size()
        stance = components.Stance(stances.Idle, [stances.Idle, stances.Running, stances.Jumping, stances.Climbing, stances.Dead])
        actor = Actor(cls.name, controller, display, location, physics, size, stance, cls)
        actor.add_component(components.Collector())
        actor.add_component(components.Health(cls.max_health))

        return actor

    @classmethod
    def reset(cls, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.controller.reset()
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()
        game_object.stance.reset()
