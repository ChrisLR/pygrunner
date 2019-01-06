import pyglet

from pygrunner.core.components.base import Component


class Display(Component):
    name = "display"

    def __init__(self, layer, animations):
        super().__init__()
        self.layer = layer
        self.animations = animations
        self.current = None
        self.current_name = ""
        self.batch = None
        self.group = None
        # TODO Flipped images shouldn't be kept here
        # TODO We should store and access flipped images from the spritesheet
        self._flipped_images = {}
        self.flipped = False

    def assign(self, batch, group):
        self.batch = batch
        self.group = group
        self.play('idle')

    def add(self, name, animation):
        self.animations[name] = animation

    def update(self):
        if self.flipped != self.host.flipped:
            self.flip()

    def play(self, name):
        if self.current and name == self.current_name:
            return

        self.current_name = name
        animation = self.animations.get(name)
        if animation is not None:
            if self.current is not None:
                self.current.visible = False
            else:
                self.current = pyglet.sprite.Sprite(animation, batch=self.batch, group=self.group)

            if self.flipped:
                self.current.image = self._get_or_create_flipped(self.current_name, animation)
            else:
                self.current.image = animation

            self.current.scale = 1

    def reset(self):
        self.current = self.animations.get('idle')


    def _get_or_create_flipped(self, name, animation):
        flipped_image = self._flipped_images.get(name)
        if flipped_image is None:
            flipped_image = animation.get_transform(flip_x=True)
            self._flipped_images[name] = flipped_image

        return flipped_image

    def flip(self):
        if self.flipped:
            self.current.image = self.animations.get(self.current_name)
            self.flipped = False
        else:
            self.current.image = self._get_or_create_flipped(self.current_name, self.current.image)
            self.flipped = True