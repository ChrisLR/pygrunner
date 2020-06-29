from pyg2d.client import GameManager, GameOptions
from pyg2d.core.game import GameContext

from pygrunner.gamedata.recipes.characters import humans

if __name__ == '__main__':
    options = GameOptions("sprites", "tmx", [humans.HumanMale1])
    game_context = GameContext(options)
    game_context.sprite_loader.load_grid_sheet("sidescroller/packed.png", grid_size=32, name="packed")
    game = GameManager(game_context)
    game_context.level_manager.add_level("simple")
    game.start()
