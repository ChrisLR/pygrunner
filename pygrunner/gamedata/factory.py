


class Factory(object):
    """
    The factory spawns game objects in the game space.
    It also uses a pool to help with garbage collection
    """
    known_recipes = {}

    def __init__(self, sprite_loader, object_pool):
        self.sprite_loader = sprite_loader
        self.object_pool = object_pool

    def destroy(self, game_object):
        self.object_pool.add(game_object)

    def get_or_create(self, recipe, location):
        recipe = self._get_recipe(recipe)
        game_object = self.object_pool.get(recipe)
        if game_object:
            game_object.location = location
            return game_object
        else:
            game_object = recipe.create(location, self.sprite_loader)
            return game_object

    def _get_recipe(self, recipe):
        if isinstance(recipe, str):
            recipe = self.known_recipes.get(recipe)
            if recipe is None:
                raise Exception("Recipe '%s' not known." % recipe)
        else:
            if hasattr(recipe, 'create') and hasattr(recipe, 'reset'):
                return recipe

        raise Exception("Recipe '%s' is not valid.")


    @classmethod
    def register(cls, recipe):
        cls.known_recipes[recipe.name] = recipe
