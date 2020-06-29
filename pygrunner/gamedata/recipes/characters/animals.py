from pyg2d.core.ai.follower import DumbFollowerAI
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pyg2d.gamedata.recipes.characters.base import Character


@Factory.register
class Turtle(Character):
    name = "Turtle"
    animations = {
        'idle': [SpriteInfo('packed', 'turtle_idle', 0, 16)],
        'run': [
            SpriteInfo('packed', 'turtle_idle_run_0', 0, 16),
            SpriteInfo('packed', 'turtle_idle_run_1', 0, 17),
            SpriteInfo('packed', 'turtle_idle_run_1', 0, 18),
            SpriteInfo('packed', 'turtle_idle_run_1', 0, 19),
        ],
    }

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        actor = super().create(sprite_loader)
        actor.remove_component(actor.health)
        actor.controller.ai = DumbFollowerAI(actor)

        return actor
