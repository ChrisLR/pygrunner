from pygrunner.client.scenes.base import Scene
from pygrunner.client.camera import Camera
from pygrunner.core import components, physics


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.game._start_level()
        self.camera = Camera(components.Location(0, 0), components.Size(self.window.height, self.window.width), game)
        self.camera.follow(self.game.level.game_objects[1])
        self.physics_engine = physics.PhysicsEngine(0.01, 0.5, 0.9)

    def on_draw(self):
        self.camera.draw()

    def update(self, dt):
        level = self.game.level
        self.physics_engine.update(self.game.level)
        for game_object in level.game_objects:
            game_object.update(dt)
            self.camera.update_for_object(game_object)

        for static_object in level.statics:
            static_object.update(dt)
            self.camera.update_for_object(static_object)
        self.camera.update()


    def handle_keymap_input(self, keymap_input):
        pass


