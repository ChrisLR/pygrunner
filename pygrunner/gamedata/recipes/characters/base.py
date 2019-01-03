from pygrunner.gamedata.recipes.base import Recipe
from pygrunner.core.objecttypes import Actor
from pygrunner.core import components, Layer, stances



class Character(Recipe):
    name = ""
    animations = {}
    move_speed = 1
    jump_height = 1

    def create(self, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = self._set_animations(sprite_loader)
        controller = components.AIController(None)
        display = components.Display(Layer.middle, pyglet_animations)
        location = components.Location(0, 0)
        physics = components.Physics()
        size = components.Size()
        stance = components.Stance(stances.Walking, (stances.Idle, stances.Walking))
        actor = Actor(self.name, controller, display, location, physics, size, stance)

        return actor

    def reset(self, game_object):
        """
        Reinitialize components for re-use
        """
        game_object.controller.reset()
        game_object.display.reset()
        game_object.location.reset()
        game_object.physics.reset()
        game_object.size.reset()
        game_object.stance.reset()
