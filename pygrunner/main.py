from pygrunner.client.clientgame import ClientGame
from pygrunner.client.scenes.manager import SceneManager


if __name__ == '__main__':
    manager = SceneManager()
    game = ClientGame(manager)
    game.start()
