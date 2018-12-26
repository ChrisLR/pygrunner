import pyglet


class SceneManager(object):
    def __init__(self):
        self.scenes = []
        self.scene_stack = []

    @property
    def active_scene(self):
        return self.scene_stack[-1]

    def start(self):
        self.initialize_ui()
        pyglet.clock.schedule_interval(self.update, 1 / 1000)
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.active_scene.on_draw()

    def on_key_press(self, symbol, modifiers):
        self.active_scene.on_key_press(symbol, modifiers)

    def initialize_ui(self):
        self.window = pyglet.window.Window()
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)

    def update(self, dt):
        self.active_scene.update(dt)
