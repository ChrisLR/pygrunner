from pyg2d.core import Layer, objecttypes
from pyg2d.core import components
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pyg2d.gamedata.recipes.base import Recipe


class LiquidBlock(Recipe):
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

        return game_object

    @classmethod
    def modify(cls, game_object, custom_properties):
        super().modify(game_object, custom_properties)

    @classmethod
    def reset(cls, game_object):
        super().reset(game_object)


@Factory.register
class LavaTop(LiquidBlock):
    name = "Lava Top"
    animations = {
        'idle': [SpriteInfo('packed', 'lava_top', 21, 25)],
    }

    @classmethod
    def create(cls, sprite_loader):
        game_object = super().create(sprite_loader)
        game_object.add_component(components.StaticTriggers())
        game_object.add_component(components.KillTouch(damage=1, knockback=True))
        return game_object


@Factory.register
class LavaMiddle(LiquidBlock):
    name = "Lava Middle"
    animations = {
        'idle': [SpriteInfo('packed', 'lava_middle', 20, 25)]
    }

    @classmethod
    def create(cls, sprite_loader):
        game_object = super().create(sprite_loader)
        game_object.add_component(components.StaticTriggers())
        game_object.add_component(components.KillTouch(damage=1))

        return game_object
