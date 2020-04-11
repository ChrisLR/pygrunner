import abc

import pyglet


class Recipe(metaclass=abc.ABCMeta):
    """
    An object detailing how to create or reset game objects
    """
    name = ""
    animations = {}
    initial_stock = 0

    @classmethod
    @abc.abstractmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        pass

    @classmethod
    def modify(cls, game_object, custom_properties):
        flipped_horizontal = custom_properties.get('flipped_horizontal')
        if flipped_horizontal is not None:
            game_object.flipped = flipped_horizontal
        # TODO Support vertical flip

    @classmethod
    @abc.abstractmethod
    def reset(cls, game_object):
        """
        Reinitialize components for re-use
        """
        pass

    @classmethod
    def _set_animations(cls, sprite_loader):
        animations = {}
        for animation_name, sprite_infos in cls.animations.items():
            images = []
            for sprite_info in sprite_infos:
                sheet = sprite_loader.get_by_name(sprite_info.spritesheet_name)
                sheet.set_region_name(sprite_info.sprite_name, sprite_info.row, sprite_info.column)
                image = sheet.get_region_by_name(sprite_info.sprite_name)
                images.append(image)

            if len(images) > 1:
                frames = [pyglet.image.AnimationFrame(image, 0.1) for image in images]
                animations[animation_name] = pyglet.image.Animation(frames)
            else:
                animations[animation_name] = images[0]

        return animations
