from pygrunner.core import Layer, objecttypes
from pygrunner.core import components
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.base import Recipe


class JumpPad(Recipe):
    # TODO Decide if we want a special tile, or we keep as a game object
    name = ""
    animations = {}
    initial_stock = 200
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
        physics.platform = True
        physics.solid = False
        size = components.Size()
        game_object = objecttypes.GameObject(cls.name, display, location, physics, size, cls)
        bouncer = components.Bouncer(cls.vertical_force, cls.horizontal_force)
        game_object.add_component(bouncer)

        return game_object

    @classmethod
    def modify(cls, game_object, custom_properties):
        super().modify(game_object, custom_properties)
        vertical_force = custom_properties.get('vertical_force')
        if vertical_force is not None:
            game_object.bouncer.vertical_force = vertical_force

        horizontal_force = custom_properties.get('horizontal_force')
        if horizontal_force is not None:
            game_object.bouncer.horizontal_force = horizontal_force

    @classmethod
    def reset(cls, game_object):
        pass


@Factory.register
class YellowJumpPad(JumpPad):
    name = "Yellow Jump Pad"
    animations = {
        'idle': [SpriteInfo('packed', 'yellow_jump_pad', 26, 31)],
        'bounce': [SpriteInfo('packed', 'yellow_jump_pad_bounce', 27, 31)]
    }
    vertical_force = -24


@Factory.register
class HorizontalYellowJumpPad(JumpPad):
    name = "Horizontal Yellow Jump Pad"
    animations = {
        'idle': [SpriteInfo('packed', 'yellow_jump_pad', 26, 32)],
        'bounce': [SpriteInfo('packed', 'yellow_jump_pad_bounce', 27, 32)]
    }
    horizontal_force = 24
