from pygrunner.core import components, Layer, stances
from pygrunner.core.objecttypes import Actor
from pygrunner.gamedata.recipes.base import Recipe


class Enemy(Recipe):
    name = ""
    animations = {}
    move_speed = 2
    jump_height = 1
    initial_stock = 10
    max_health = 1

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
        stance = components.Stance(stances.Idle, [stances.Idle, stances.Running, stances.Jumping, stances.Climbing, stances.Punching, stances.Dead])
        actor = Actor(cls.name, controller, display, location, physics, size, stance, cls)
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
