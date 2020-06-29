from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory

from pygrunner.gamedata.recipes.characters.base import Character


@Factory.register
class HumanMale1(Character):
    name = "Human Male 1"
    animations = {
        'idle': [SpriteInfo('packed', 'human_male_1_idle_0', 30, 12)],
        'run': [
            SpriteInfo('packed', 'human_male_1_run_0', 30, 13),
            SpriteInfo('packed', 'human_male_1_run_1', 30, 14),
        ],
        'climb':[
            SpriteInfo('packed', 'human_male_1_climb_0', 30, 15),
            SpriteInfo('packed', 'human_male_1_climb_1', 30, 15, True),
        ],
        'punch': [
            SpriteInfo('packed', 'human_male_1_punch_0', 30, 14),
            SpriteInfo('packed', 'human_male_1_punch_1', 30, 16),
        ],
        'dead': [SpriteInfo('packed', 'human_male_1_dead_0', 30, 17)],
    }


@Factory.register
class HumanFemale1(Character):
    name = "Human Female 1"
    animations = {
        'idle': [SpriteInfo('packed', 'human_female_1_idle_0', 29, 12)],
        'run': [
            SpriteInfo('packed', 'human_female_1_run_0', 29, 13),
            SpriteInfo('packed', 'human_female_1_run_1', 29, 14),
        ],
        'climb':[
            SpriteInfo('packed', 'human_female_1_climb_0', 29, 15),
            SpriteInfo('packed', 'human_female_1_climb_1', 29, 15, True),
        ],
        'punch': [
            SpriteInfo('packed', 'human_female_1_punch_0', 29, 14),
            SpriteInfo('packed', 'human_female_1_punch_1', 29, 16),
        ],
        'dead': [SpriteInfo('packed', 'human_female_1_dead_0', 29, 17)],
    }


@Factory.register
class HumanTurtle(Character):
    name = "Turtle"
    animations = {
        'idle': [SpriteInfo('packed', 'human_turtle_1_idle_0', 0, 20)],
        'run': [
            SpriteInfo('packed', 'human_turtle_1_run_0', 0, 21),
            SpriteInfo('packed', 'human_turtle_1_run_1', 0, 22),
        ],
        'climb': [
            SpriteInfo('packed', 'human_turtle_1_climb_0', 0, 23),
            SpriteInfo('packed', 'human_turtle_1_climb_1', 0, 24, True),
        ],
        'punch': [
            SpriteInfo('packed', 'human_turtle_1_punch_0', 0, 22),
            SpriteInfo('packed', 'human_turtle_1_punch_1', 0, 24),
        ],
        'dead': [SpriteInfo('packed', 'human_turtle_1_dead_0', 0, 27)],
        'transform_to_turtle': [
            SpriteInfo('packed', 'human_turtle_1_trt_0', 0, 28),
            SpriteInfo('packed', 'human_turtle_1_trt_1', 0, 29),
            SpriteInfo('packed', 'human_turtle_1_trt_2', 0, 30),
            SpriteInfo('packed', 'turtle_idle', 0, 16),
        ],
        'transform_from_turtle': [
            SpriteInfo('packed', 'turtle_idle', 0, 16),
            SpriteInfo('packed', 'human_turtle_1_trt_2', 0, 30),
            SpriteInfo('packed', 'human_turtle_1_trt_1', 0, 29),
            SpriteInfo('packed', 'human_turtle_1_trt_0', 0, 28),
        ],
    }

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        actor = super().create(sprite_loader)

        return actor
