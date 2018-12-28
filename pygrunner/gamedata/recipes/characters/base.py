from pygrunner.gamedata.recipes.base import Recipe


class Character(Recipe):
    name = ""
    animations = {}
    move_speed = 1
    jump_height = 1

    def create(self, location):
        """
        Creates a game object and assigns proper components
        """
        pass

    def reset(self, game_object):
        """
        Reinitialize components for re-use
        """
        pass
