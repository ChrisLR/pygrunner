import abc

import pyglet


class Recipe(metaclass=abc.ABCMeta):
    """
    An object detailing how to create or reset game objects
    """
    name = ""
    animations = {}

    @abc.abstractmethod
    def create(self, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pass

    @abc.abstractmethod
    def reset(self, game_object):
        """
        Reinitialize components for re-use
        """
        pass

    def _set_animations(self, sprite_loader):
        animations = {}
        for animation_name, sprite_infos in self.animations.items():
            frames = []
            for sprite_info in sprite_infos:
                sheet = sprite_loader.get_by_name(sprite_info.spritesheet_name)
                sheet.set_region_name(sprite_info.sprite_name, sprite_info.row, sprite_info.column)
                frame = pyglet.image.AnimationFrame(sheet.get_region_by_name(sprite_info.sprite_name), 0.1)
                frames.append(frame)
            animations[animation_name] = pyglet.image.Animation(frames)

        return animations