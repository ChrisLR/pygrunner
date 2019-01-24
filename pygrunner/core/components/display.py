from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Display(Component):
    name = "display"

    def __init__(self, layer, animations):
        super().__init__()
        self.layer = layer
        self.animations = animations
        self.current = None
        self.current_name = ""
        # TODO Flipped images shouldn't be kept here
        # TODO We should store and access flipped images from the spritesheet
        self._flipped_images = {}
        self.flipped = False
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
            self.current = animation

            if self.flipped:
                self.current = self._get_or_create_flipped(self.current_name, animation)
            else:
                self.current = animation

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
            self.current = self.animations.get(self.current_name)
            self.flipped = False
        else:
            self.current = self._get_or_create_flipped(self.current_name, self.current)
            self.flipped = True