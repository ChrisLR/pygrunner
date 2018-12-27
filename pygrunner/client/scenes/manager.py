class SceneManager(object):
    def __init__(self):
        self.scenes = []
        self.scene_stack = []
        self.inputs = None

    @property
    def active_scene(self):
        return self.scene_stack[-1]

    def on_draw(self):
        self.active_scene.on_draw()

    def start(self, inputs):
        self.inputs = inputs
        self.scene_stack.append(self.scenes[0])

    def update(self, dt):
        self.active_scene.update(dt)
