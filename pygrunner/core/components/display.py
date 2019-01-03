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

    def add(self, name, animation):
        self.animations[name] = animation

    def update(self):
        self.animations.current.position = self.host.location.tuple()

    def play(self, name, batch, group):
        animation = self.animations.get(name)
        if animation is not None:
            self.current = pyglet.sprite.Sprite(animation, batch=batch, group=group)
            self.current.position = self.host.location.tuple()
            self.current.scale = 1.5

    def reset(self):
        self.current = self.animations.get('idle')

