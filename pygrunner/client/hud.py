from pygrunner.core.componentholder import ComponentHolder
from pygrunner.core.spriteinfo import SpriteInfo


class HUD(ComponentHolder):
    """
    Object has to be drawn by the CAMERA in the front layer
    Object has to be composed of several elements
    Object needs information about the Game/Actors
    """
    def __init__(self, game, sprite_loader):
        super().__init__()
        self.game = game
        self.sprite_loader = sprite_loader



class HUDElement(object):
    def __init__(self, root, rel_x, rel_y):
        self.root = root
        self.rel_x = rel_x
        self.rel_y = rel_y

    def update(self):
        pass

    def show(self):
        pass

    def hide(self):
        pass


class HUDLifeBar(HUDElement):
    _sprite_infos = {
            'empty_heart': [SpriteInfo('packed', 'empty_half_heart', 26, 15)],
            'half_heart': [SpriteInfo('packed', 'half_heart', 29, 15)],
            'full_heart': [SpriteInfo('packed', 'full_heart', 27, 15)],
        }

    def __init__(self, root, rel_x, rel_y, actor):
        super().__init__(root, rel_x, rel_y)
        self.actor = actor
        self._sprites = []

    def _initialize(self):
        self.root.spriteloader.get_by_name("")
        # This needs to use the sprite loader to load the sprites

    def update(self):
        # We draw grey hearts up to the Max Health
        # Then we Draw max / 2 full health and a half heart for the left over
        for _ in range(self.actor.health.max):
            pass
