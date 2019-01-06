from pygrunner.client.scenes.base import Scene
from pygrunner.client.camera import Camera
from pygrunner.core import components, physics


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.game._start_level()
        self.camera = Camera(components.Location(0, 0), components.Size(self.window.height, self.window.width), game)
        self.physics_engine = physics.PhysicsEngine(0.01, 0.5, 0.9)

        # TODO This scene is responsible for drawing the game
        # TODO Transmitting input to the Game
        # TODO And looping the game

    def on_draw(self):
        self.game.batch.draw()

    def update(self, dt):
        level = self.game.level
        for game_object in level.game_objects:
            game_object.update(dt)
            self.camera.adjust_game_object_sprite(game_object)

        for static_object in level.statics:
            static_object.update(dt)
            self.camera.adjust_game_object_sprite(static_object)

        self.physics_engine.update(self.game.level)


    def handle_keymap_input(self, keymap_input):
        pass


