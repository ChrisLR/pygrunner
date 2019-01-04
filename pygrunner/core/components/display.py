import pyglet

from pygrunner.core.components.base import Component


class Display(Component):
    name = "display"

    def __init__(self, layer, animations):
        super().__init__()
        self.layer = layer
        self.animations = animations
        self.current = animations.get('idle')
        self.sprite = None
        self.batch = None
        self.group = None
        self._sprites = {}

    def assign(self, batch, group):
        self.batch = batch
        self.group = group

    def add(self, name, animation):
        self.animations[name] = animation

    def update(self):
        self.animations.current.position = self.host.location.tuple()

    def play(self, name):
        animation = self.animations.get(name)
        if animation is not None:
            if self.current is not None:
                self.current.visible = False

            self.current = self._sprites.get(name, pyglet.sprite.Sprite(animation, batch=self.batch, group=self.group))
            self.current.visible = True
            self.current.position = self.host.location.tuple()
            self.current.scale = 1.5

    def reset(self):
        self.current = self.animations.get('idle')
