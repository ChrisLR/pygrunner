from pygrunner.client.scenes.base import Scene
import pyglet


class GameScene(Scene):
    name = "game"

    def __init__(self, inputs, manager, game):
        super().__init__(inputs, manager, game)
        self.game._start_level()

        # TODO This scene is responsible for drawing the game
        # TODO Transmitting input to the Game
        # TODO And looping the game

    def on_draw(self):
        self.game.batch.draw()

    def update(self, dt):
        level = self.game.level
        for game_object in level.game_objects:
            game_object.update(dt)

        for static_object in level.statics:
            static_object.update(dt)

    def handle_keymap_input(self, keymap_input):
        pass


