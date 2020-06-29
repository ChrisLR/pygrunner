from pyg2d.core.ai.basic import ZombieAI
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pyg2d.gamedata.recipes.enemies.base import Enemy


@Factory.register
class GreenZombie(Enemy):
    name = "Green Zombie"
    move_speed = 1
    jump_height = 16
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


@Factory.register
class GreenOrc(Enemy):
    name = "Green Orc"
    move_speed = 4
    jump_height = 20
    animations = {
        'idle': [SpriteInfo('packed', 'green_orc_idle_0', 30, 0)],
        'run': [
            SpriteInfo('packed', 'green_orc_run_0', 30, 0),
            SpriteInfo('packed', 'green_orc_run_1', 30, 1),
        ],
        'climb':[
            SpriteInfo('packed', 'green_orc_climb_0', 30, 3),
            SpriteInfo('packed', 'green_orc_climb_1', 30, 3, True),
        ],
        'punch': [
            SpriteInfo('packed', 'green_orc_punch_0', 30, 2),
            SpriteInfo('packed', 'green_orc_punch_1', 30, 4),
            SpriteInfo('packed', 'green_orc_punch_1', 30, 4),
        ],
        'dead': [SpriteInfo('packed', 'green_orc_dead_0', 30, 5)],
    }


@Factory.register
class BlueOrc(Enemy):
    name = "Blue Orc"
    move_speed = 4
    jump_height = 20
    animations = {
        'idle': [SpriteInfo('packed', 'blue_orc_idle_0', 20, 11)],
        'run': [
            SpriteInfo('packed', 'blue_orc_run_0', 20, 11),
            SpriteInfo('packed', 'blue_orc_run_1', 20, 12),
        ],
        'climb':[
            SpriteInfo('packed', 'blue_orc_climb_0', 20, 14),
            SpriteInfo('packed', 'blue_orc_climb_1', 20, 14, True),
        ],
        'punch': [
            SpriteInfo('packed', 'blue_orc_punch_0', 20, 13),
            SpriteInfo('packed', 'blue_orc_punch_1', 20, 15),
            SpriteInfo('packed', 'blue_orc_punch_1', 20, 15),
        ],
        'dead': [SpriteInfo('packed', 'blue_orc_dead_0', 20, 16)],
    }


@Factory.register
class BlueDemon(Enemy):
    name = "Blue Demon"
    move_speed = 4
    jump_height = 20
    animations = {
        'idle': [SpriteInfo('packed', 'blue_demon_idle_0', 23, 11)],
        'run': [
            SpriteInfo('packed', 'blue_demon_run_0', 23, 11),
            SpriteInfo('packed', 'blue_demon_run_1', 23, 12),
        ],
        'climb':[
            SpriteInfo('packed', 'blue_demon_climb_0', 23, 14),
            SpriteInfo('packed', 'blue_demon_climb_1', 23, 14, True),
        ],
        'punch': [
            SpriteInfo('packed', 'blue_demon_punch_0', 23, 13),
            SpriteInfo('packed', 'blue_demon_punch_1', 23, 15),
            SpriteInfo('packed', 'blue_demon_punch_1', 23, 15),
        ],
        'dead': [SpriteInfo('packed', 'blue_demon_dead_0', 23, 16)],
    }
