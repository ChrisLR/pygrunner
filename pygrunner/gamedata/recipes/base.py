class Recipe(object):
    """
    An object detailing how to create or reset game objects
    """
    name = ""

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
