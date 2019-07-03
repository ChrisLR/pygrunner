from pygrunner.client.clientgame import ClientGame
from pygrunner.client.scenes.manager import SceneManager
import cProfile


if __name__ == '__main__':
    manager = SceneManager()
    game = ClientGame(manager)
    game.start()
    # cProfile.run('game.start()')
