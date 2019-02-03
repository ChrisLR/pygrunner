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
        game_object.add_component(components.Bouncer(cls.vertical_force, cls.horizontal_force))

        return game_object


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
    vertical_force = -48
