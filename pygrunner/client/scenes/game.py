from pygrunner.client.scenes.base import Scene
from pygrunner.client.camera import Camera
from pygrunner.core import components, physics


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.recycle_bin = set()
        self.game._start_level()
        camera_location = components.Location(0, 0, self.game.level)
        self.camera = Camera(camera_location, components.Size(self.window.height + 64, self.window.width + 64), game)
        self.camera.follow(self.game.level.game_objects[-1])
        self.physics_engine = physics.PhysicsEngine(0.01, 0.5, 0.9)

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

        for static_object in level.statics:
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


