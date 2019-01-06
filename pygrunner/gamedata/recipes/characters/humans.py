from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
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
            SpriteInfo('packed', 'human_male_1_climb_1', 30, 16, True),
        ],
        'punch': [
            SpriteInfo('packed', 'human_male_1_punch_0', 30, 15),
            SpriteInfo('packed', 'human_male_1_punch_1', 30, 17),
        ],
        'dead': [SpriteInfo('packed', 'human_male_1_dead_0', 30, 18)],
    }
