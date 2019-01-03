from pygrunner.gamedata.recipes.base import Recipe
from pygrunner.core.objecttypes import Actor
from pygrunner.core import components, Layer



class Character(Recipe):
    name = ""
    animations = {}
    move_speed = 1
    jump_height = 1

    def create(self, location, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pyglet_animations = self._set_animations(sprite_loader)
        display = components.Display(Layer.middle, pyglet_animations)
        actor = Actor(self.name, )

    def reset(self, game_object):
        """
        Reinitialize components for re-use
        """
        pass

