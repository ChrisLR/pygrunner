from pyg2d.core import stances
from pyg2d.core.ai.flying import FlyingAI
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pygrunner.gamedata.recipes.enemies.base import Enemy


@Factory.register
class BlackBat(Enemy):
    name = "Black Bat"
    move_speed = 4
    jump_height = 20
    start_stance = stances.Flying
    stances = [stances.Flying, stances.Punching, stances.Dead]
    animations = {
        'idle': [
            SpriteInfo('packed', 'black_bat_idle_0', 26, 0),
            SpriteInfo('packed', 'black_bat_idle_1', 26, 1)
        ],
        'fly': [
            SpriteInfo('packed', 'black_bat_idle_0', 26, 0),
            SpriteInfo('packed', 'black_bat_idle_1', 26, 1),
        ],
        'dead': [SpriteInfo('packed', 'black_bat_dead_0', 26, 2)],
    }

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        actor = super().create(sprite_loader)
        actor.controller.ai = FlyingAI(actor)

        return actor


@Factory.register
class BlueGhost(Enemy):
    name = "Blue Ghost"
    move_speed = 4
    jump_height = 20
    start_stance = stances.Flying
    stances = [stances.Flying, stances.Punching, stances.Dead]
    animations = {
        'idle': [
            SpriteInfo('packed', 'blue_ghost_idle_0', 27, 6),
        ],
        'fly': [
            SpriteInfo('packed', 'blue_ghost_idle_0', 27, 7),
            SpriteInfo('packed', 'blue_ghost_idle_1', 27, 8),
        ],
        'dead': [SpriteInfo('packed', 'blue_ghost_dead_0', 27, 11)],
    }

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        actor = super().create(sprite_loader)
        actor.controller.ai = FlyingAI(actor)

        return actor
