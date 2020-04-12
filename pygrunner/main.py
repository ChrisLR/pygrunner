from pygrunner.client.clientgame import ClientGame
from pygrunner.client.scenes.manager import SceneManager
#import cProfile
#from pyinstrument import Profiler


if __name__ == '__main__':
    manager = SceneManager()
    game = ClientGame(manager)
    #profiler = Profiler()
    #profiler.start()
    game.start()
    #profiler.stop()
    # print(profiler.output_text(unicode=True, color=True))
    #cProfile.run('game.start()', sort='cumulative')
