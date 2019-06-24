import pyglet

from pygrunner.core.spriteinfo import SpriteInfo


class HUD(object):
    """
    Object has to be drawn by the CAMERA in the front layer
    Object has to be composed of several elements
    Object needs information about the Game/Actors
    """

    def __init__(self, game, players, sprite_loader):
        super().__init__()
        self.game = game
        self.sprite_loader = sprite_loader
        self.elements = []
        self.players = players
        width, height = game.window.get_size()
        self._hud_positions = {
            0: (16, height - 16),
            1: (width - 48, height - 16),
            2: (16, 16),
            3: (width - 48, 16)
        }
        self._setup()

    def assign(self, batch, group):
        for element in self.elements:
            element.assign(batch, group)

    def _setup(self):
        for index, player in enumerate(self.players):
            rel_pos = self._hud_positions[index]
            element = HUDLifeBar(self, *rel_pos, player)
            self.elements.append(element)

    def update(self):
        for element in self.elements:
            element.update()


class HUDElement(object):
    def __init__(self, root, rel_x, rel_y):
        self.root = root
        self.rel_x = rel_x
        self.rel_y = rel_y

    def assign(self, batch, group):
        pass

    def update(self):
        pass

    def show(self):
        pass

    def hide(self):
        pass


class HUDLifeBar(HUDElement):
    _sprite_infos = {
            'empty_heart': [SpriteInfo('packed', 'empty_half_heart', 23, 24)],
            'half_heart': [SpriteInfo('packed', 'half_heart', 23, 27)],
            'full_heart': [SpriteInfo('packed', 'full_heart', 23, 25)],
    }

    def __init__(self, root, rel_x, rel_y, actor):
        super().__init__(root, rel_x, rel_y)
        self.actor = actor
        self._sprites = []
        self.animations = {}
        self._initialize()

    def _initialize(self):
        for animation_name, sprite_infos in self._sprite_infos.items():
            frames = []
            for sprite_info in sprite_infos:
                sheet = self.root.sprite_loader.get_by_name(sprite_info.spritesheet_name)
                sheet.set_region_name(sprite_info.sprite_name, sprite_info.row,
                                      sprite_info.column)
                frame = pyglet.image.AnimationFrame(
                    sheet.get_region_by_name(sprite_info.sprite_name), 0.1)
                frames.append(frame)
            self.animations[animation_name] = pyglet.image.Animation(frames)
        self._sprites = [
            pyglet.sprite.Sprite(self.animations["empty_heart"])
            for _ in range(self.actor.health.max)]

    def assign(self, batch, group):
        for i, sprite in enumerate(self._sprites):
            sprite.batch = batch
            sprite.group = group
            sprite.x = self.rel_x + (i * 16)
            sprite.y = self.rel_y

    def update(self):
        for i in range(self.actor.health.max):
            if i >= len(self._sprites):
                # TODO Support adding them
                break

            sprite = self._sprites[i]
            if i <= self.actor.health.current - 1:
                sprite.image = self.animations['full_heart']
            else:
                sprite.image = self.animations['empty_heart']
