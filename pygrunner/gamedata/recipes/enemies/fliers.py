from pygrunner.core import stances
from pygrunner.core.ai.flying import FlyingAI
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
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
