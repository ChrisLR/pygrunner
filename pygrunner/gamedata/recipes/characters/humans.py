from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.characters.base import Character


@Factory.register
class HumanMale1(Character):
    name = "Human Male 1"
    animations = {
        'idle': [SpriteInfo('packed.png', 'human_male_1_idle_0', 0, 13)],
        'run': [
            SpriteInfo('packed.png', 'human_male_1_run_0', 0, 14),
            SpriteInfo('packed.png', 'human_male_1_run_1', 0, 15),
        ],
        'climb':[
            SpriteInfo('packed.png', 'human_male_1_climb_0', 0, 16),
            SpriteInfo('packed.png', 'human_male_1_climb_1', 0, 16, True),
        ],
        'punch': [
            SpriteInfo('packed.png', 'human_male_1_punch_0', 0, 15),
            SpriteInfo('packed.png', 'human_male_1_punch_1', 0, 17),
        ],
        'dead': [SpriteInfo('packed.png', 'human_male_1_dead_0', 0, 18)],
    }
