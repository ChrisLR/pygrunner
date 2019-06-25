from pygrunner.core.ai.basic import ZombieAI
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.enemies.base import Enemy


@Factory.register
class GreenZombie(Enemy):
    name = "Green Zombie"
    move_speed = 1
    jump_height = 8
    animations = {
        'idle': [SpriteInfo('packed', 'green_zombie_idle_0', 28, 0)],
        'run': [
            SpriteInfo('packed', 'green_zombie_run_0', 28, 0),
            SpriteInfo('packed', 'green_zombie_run_1', 28, 1),
        ],
        'climb':[
            SpriteInfo('packed', 'green_zombie_climb_0', 28, 3),
            SpriteInfo('packed', 'green_zombie_climb_1', 28, 3, True),
        ],
        'punch': [
            SpriteInfo('packed', 'green_zombie_punch_0', 28, 2),
            SpriteInfo('packed', 'green_zombie_punch_1', 28, 4),
            SpriteInfo('packed', 'green_zombie_punch_1', 28, 4),
        ],
        'dead': [SpriteInfo('packed', 'green_zombie_dead_0', 28, 5)],
    }

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        actor = super().create(sprite_loader)
        actor.controller.ai = ZombieAI(actor)

        return actor
