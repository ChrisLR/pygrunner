class Camera(object):
    def __init__(self, location, size, game):
        self.location = location
        self.size = size
        self.game = game

    def adjust_game_object_sprite(self, game_object):
        """
        Will adjust a game object's sprite based on
        :param game_object: The game object to adjust
        """
        if self.is_visible(game_object):
            game_object.display.current.visible = True
            pixel_coordinate = self.coord_to_pixel(game_object.location.x, game_object.location.y)
            game_object.display.current.set_position(*pixel_coordinate)
        else:
            game_object.display.current.visible = False

    def pixel_to_coord(self, pixel_x, pixel_y):
        return self.location.x + pixel_x, self.location.y + pixel_y

    def coord_to_pixel(self, coord_x, coord_y):
        return (coord_x - self.location.x) * 16, (coord_y - self.location.y) * 16

    def is_visible(self, game_object):
        if self.size.rectangle.intersects(game_object.size.rectangle):
            return True
        return False
