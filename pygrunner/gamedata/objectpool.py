class ObjectPool(object):
    """
    This pool stores created objects and retrieves them
    """
    def __init__(self):
        self._pool = {}
        self.used_count = {}
        self.max_count = {}


    def add(self, recipe, game_object):
        """
        Adds a game object to the pool
        :param recipe:
        :param game_object:
        :return:
        """
        if recipe in self._pool:
            self._pool[recipe].append(game_object)
        else:
            self._pool[recipe] = [game_object]


    def get(self, recipe):
        """
        Get a game object from the pool.
        :param recipe: The recipe associated to the game object
        :return: An initialized game object
        """
        if recipe not in self._pool:
            return None

        game_object_list = self._pool[recipe]
        if not game_object_list:
            return None

        used_count = self.used_count.get(recipe, 0)
        game_object = game_object_list.pop(0)
        self.used_count[recipe] = used_count + 1

        return game_object

    def refund(self, recipe, game_object):
        """
        Returns a game object to the pool and reinitialize it
        :param recipe:
        :param game_object:
        :return:
        """
        recipe.reset(game_object)
        used_count = self.used_count.get(recipe, 1)
        if recipe in self._pool:
            self._pool[recipe].append(game_object)
        else:
            self._pool[recipe] = [game_object]
        self.used_count[recipe] = used_count - 1
