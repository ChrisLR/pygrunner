from pygrunner.client.graphics.spriteloader import SpriteLoader

class ClientGame(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.players = []
        self.joysticks = None
        self.batch = None
        self.clock = None
        self.window = None
        self.spriteloader = SpriteLoader()
        self.entities = {}

    def on_key_press(self, symbol, modifiers):
        self.scene_manager.on_key_press(symbol, modifiers)

    def update(self, dt):
        self.scene_manager.update(dt)

    def start(self):
        self.scene_manager.start()
