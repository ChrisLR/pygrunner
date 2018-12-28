class Factory(object):
    """
    The factory spawns game objects in the game space.
    It also uses a pool to help with garbage collection
    """
    def __init__(self, sprite_loader):
        self.sprite_loader = sprite_loader


    def _set_animations(self, spriteloader):
        frames = []
        for sheet_name, name, row, col in (self.frame_0_opts, self.frame_1_opts):
            sheet = spriteloader.get_by_name(sheet_name)
            sheet.set_region_name(name, row, col)
            frame = pyglet.image.AnimationFrame(sheet.get_region_by_name(name), 0.1)
            frames.append(frame)

        return pyglet.image.Animation(frames)
