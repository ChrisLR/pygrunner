import pyglet

from pygrunner.client.camera import Camera
from pygrunner.client.scenes.base import Scene
from pygrunner.core import components, physics


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.recycle_bin = set()
        self.game._start_level()
        level = self.game.level
        camera_location = components.Location(0, level.height, self.game.level)
        self.camera = Camera(camera_location, components.Size(self.window.height + 64, self.window.width + 64), game)
        self.camera.follow(self.game.level.game_objects[-1])
        self.physics_engine = physics.PhysicsEngine(0.01, 0.75, 0.9)

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

        # TODO This is supposed to prevent updating tiles that are not on screen
        camera_rectangle = self.camera.size.rectangle
        camera_left = int(camera_rectangle.left / 32)
        camera_right = int(camera_rectangle.right / 32)
        camera_top = int(camera_rectangle.top / 32)
        camera_bottom = int(camera_rectangle.bottom / 32)
        if camera_left < 0:
            camera_left = 0

        if camera_top < 0:
            camera_bottom = 0

        columns = level.static_collision_map._collision_map[camera_left:camera_right]
        statics = [static for column in columns for static in column[camera_top:camera_bottom]]
        #print(f"{len(statics)} statics updated")
        for static_object in statics:
            if static_object is None:
                continue

            static_object.update(dt)
            self.camera.update_for_object(static_object)
        self.camera.update()

        if self.recycle_bin:
            for game_object in self.recycle_bin:
                level.remove_game_object(game_object)
                self.game.factory.destroy(game_object)
            self.recycle_bin.clear()

    def handle_keymap_input(self, keymap_input):
        pass


