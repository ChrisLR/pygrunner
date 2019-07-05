from pygrunner.core import Layer, objecttypes
from pygrunner.core import components
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.base import Recipe


class KillBlock(Recipe):
    # TODO Decide if we want a special tile, or we keep as a game object
    name = ""
    animations = {}
    initial_stock = 100
    layer = Layer.middle
    vertical_force = 0
    horizontal_force = 0

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
        physics.platform = False
        physics.solid = False
        size = components.Size()
        game_object = objecttypes.GameObject(cls.name, display, location, physics, size, cls)
        game_object.add_component(components.StaticTriggers())
        game_object.add_component(components.KillTouch(only_on_fall=True))

        return game_object

    @classmethod
    def modify(cls, game_object, custom_properties):
        super().modify(game_object, custom_properties)

    @classmethod
    def reset(cls, game_object):
        super().reset(game_object)


@Factory.register
class BrownSpikesBottom(KillBlock):
    name = "Brown Spikes Bottom"
    animations = {
        'idle': [SpriteInfo('packed', 'brown_spikes_bottom', 8, 30)],
    }
