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
        self.object_pool.refund(game_object)

    def get_or_create(self, recipe, custom_properties=None):
        recipe = self._get_recipe(recipe)
        game_object = self.object_pool.get(recipe)
        if not game_object:
            game_object = recipe.create(self.sprite_loader)

        if custom_properties is not None:
            recipe.modify(game_object, custom_properties)

        return game_object

    def _get_recipe(self, recipe_or_name):
        if isinstance(recipe_or_name, str):
            recipe = self.known_recipes.get(recipe_or_name)
            if recipe is None:
                raise Exception("Recipe '%s' not known." % recipe_or_name)
            return recipe
        else:
            if hasattr(recipe_or_name, 'create') and hasattr(recipe_or_name, 'reset'):
                return recipe_or_name

        raise Exception("Recipe '%s' is not valid." % recipe_or_name)

    def restock(self, recipe):
        initial_max = recipe.initial_stock
        if initial_max == 0:
            return

        used_count = self.object_pool.used_count.get(recipe, 0)
        current_max = self.object_pool.max_count.get(recipe, initial_max)
        available = current_max - used_count
        if available < initial_max:
            new_max = current_max * 2
            self.object_pool.max_count[recipe] = new_max
            for i in range(new_max):
                self.object_pool.add(recipe.create(self.sprite_loader))

    def restock_all(self):
        for recipe in self.known_recipes.values():
            self.restock(recipe)

    @classmethod
    def register(cls, recipe):
        cls.known_recipes[recipe.name] = recipe
        return recipe
