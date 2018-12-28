from pygrunner.client.scenes.base import Scene


class GameScene(Scene):
    def __init__(self, inputs, window, game):
        super().__init__(inputs, window, game)
        # TODO This scene is responsible for drawing the game
        # TODO Transmitting input to the Game
        # TODO And looping the game