from pygrunner.client.scenes.main import MainMenu
from pygrunner.client.scenes.game import GameScene


class SceneManager(object):
    def __init__(self):
        self.scenes = [MainMenu, GameScene]
        self.scene_stack = []
        self.inputs = None
        self.game = None
        self.window = None

    @property
    def active_scene(self):
        return self.scene_stack[-1]

    def on_draw(self):
        self.active_scene.on_draw()

    def start(self, inputs, window, game):
        self.inputs = inputs
        self.window = window
        self.game = game
        self.scene_stack.append(self.scenes[0](inputs, self, game))

    def update(self, dt):
        self.active_scene.update(dt)

    def change_to(self, scene_name):
        scene = next(scene for scene in self.scenes if scene.name == scene_name)
        self.scene_stack.append(scene(self.inputs, self, self.game))
