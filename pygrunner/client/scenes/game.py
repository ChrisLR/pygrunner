import pyglet

from pygrunner.client.camera import Camera
from pygrunner.client.scenes.base import Scene
from pygrunner.core import components, geom, physics


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.recycle_bin = set()
        self.game._start_level()
        level = self.game.level
        camera_location = components.Location(0, level.height, self.game.level)
        self.camera = Camera(camera_location, components.Size(self.window.height + 64, self.window.width + 64), game)
        print((self.camera.size.height, self.camera.size.width))
        self.camera.follow(self.game.level.game_objects[-1])
        self.physics_engine = physics.PhysicsEngine(0.01, 0.75, 0.9)
        self._previous_statics = set()

    def on_draw(self):
        self.camera.draw()

    def update(self, dt):
        level = self.game.level
        self.physics_engine.update(self.game.level)
        for game_object in level.game_objects:
            game_object.update(dt)
            if game_object.recycle:
                self.recycle_bin.add(game_object)
            self.camera.update_for_object(game_object)
        self._update_static_all(dt, level)
        self.camera.update()

        if self.recycle_bin:
            for game_object in self.recycle_bin:
                level.remove_game_object(game_object)
                self.game.factory.destroy(game_object)
            self.recycle_bin.clear()

    def handle_keymap_input(self, keymap_input):
        pass

    def _update_static_all(self, dt, level):
        camera_rect = self.camera.size.rectangle
        camera_y_offset = level.height - camera_rect.y - camera_rect.height + 64
        camera_rect = geom.Rectangle(camera_rect.x, camera_y_offset, camera_rect.width, camera_rect.height)

        for static_object in level.statics:
            static_object_sprite = static_object.display.sprite
            if camera_rect.intersects(static_object.size.rectangle):
                static_object.update(dt)
                self.camera.update_for_object(static_object)
                if static_object_sprite is not None and static_object_sprite.visible is False:
                    static_object_sprite.visible = True
            else:
                if static_object_sprite is not None and static_object_sprite.visible is True:
                    static_object_sprite.visible = False

    def _update_static_chunk(self, dt, level):
        # TODO Currently statics being drawn from the map no longer allows drawing what is underneath
        # TODO We could store multiple statics in a single position but it would complicate physics.
        # TODO Alternatively we could store multiple arrays for each "tile layer"
        # TODO Finally we could instead divide the map into chunks and use each chunk of statics instead
        # TODO Means we can store all necessary statics and simply iterate through them no matter the location
        collision_map = level.static_collision_map._collision_map
        max_right = len(collision_map)
        max_bottom = len(collision_map[0])

        camera_rectangle = self.camera.size.rectangle
        camera_left = int(camera_rectangle.left / 32)
        camera_right = int(camera_rectangle.right / 32)
        if camera_left < 0:
            camera_left = 0
        if camera_right >= max_right:
            camera_right = max_right - 1

        # The Top and Bottom of the camera are reversed on purpose
        camera_top = int((level.height - camera_rectangle.bottom) / 32)
        camera_bottom = int((level.height - camera_rectangle.top) / 32) + 2
        if camera_top < 0:
            camera_top = 0
        if camera_bottom >= max_bottom:
            camera_bottom = max_bottom - 1

        # Used to debug
        # print(f'Showing from {camera_left} to {camera_right} and {camera_top} to {camera_bottom}')

        columns = collision_map[camera_left:camera_right]
        statics = [static for column in columns for static in column[camera_top:camera_bottom]]
        new_statics = set(statics)
        unclean_statics = self._previous_statics.difference(new_statics)
        for static_object in unclean_statics:
            if static_object is not None and static_object.display is not None and static_object.display.sprite is not None:
                static_object.display.sprite.visible = False

        self._previous_statics = new_statics
        for static_object in statics:
            if static_object is None:
                continue

            if static_object is not None and static_object.display is not None and static_object.display.sprite is not None:
                static_object.display.sprite.visible = True
            static_object.update(dt)
            self.camera.update_for_object(static_object)
