import pyglet

from pygrunner.client import input
from pygrunner.client.graphics.spriteloader import SpriteLoader
from pygrunner.core.layers import Layer
from pygrunner.core.level import Level
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.objectpool import ObjectPool
from pygrunner.gamedata.recipes import tiles


class ClientGame(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.inputs = []
        self.window = None
        self.spriteloader = SpriteLoader()
        self.spriteloader.load_spritesheets(("packed.png",))
        self.factory = Factory(self.spriteloader, ObjectPool())
        self.batch = pyglet.graphics.Batch()
        self.groups = {
            Layer.background: pyglet.graphics.OrderedGroup(Layer.background),
            Layer.middle: pyglet.graphics.OrderedGroup(Layer.middle),
            Layer.foreground: pyglet.graphics.OrderedGroup(Layer.foreground),
        }

    def on_draw(self):
        self.window.clear()
        self.scene_manager.on_draw()

    def on_key_press(self, symbol, modifiers):
        for input_ in self.inputs:
            input_.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for input_ in self.inputs:
            input_.on_key_release(symbol, modifiers)

    def update(self, dt):
        self.scene_manager.update(dt)

    def start(self):
        self.initialize_keyboard_players()
        self.initialize_joystick_players()
        self.initialize_ui()
        pyglet.clock.schedule_interval(self.update, 1 / 1000)
        self.scene_manager.start(self.inputs, self.window, self)
        pyglet.app.run()

    def initialize_keyboard_players(self):
        # TODO Handle customized Mapping
        keyboard_1 = input.Keyboard(input.KeyboardMapping.default())
        keyboard_2 = input.Keyboard(input.KeyboardMapping.alternate())
        self.inputs.append(keyboard_1)
        self.inputs.append(keyboard_2)

    def initialize_ui(self):
        self.window = pyglet.window.Window()
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)

    def initialize_joystick_players(self):
        joysticks = pyglet.input.get_joysticks()
        for joystick in joysticks:
            joystick.open()
            # TODO Handle customized Mapping
            joystick_mapping = input.JoystickMapping.default()
            joystick_input = input.Joystick(joystick, joystick_mapping)
            self.inputs.append(joystick_input)

    def _start_level(self):
        # TODO This is only in the meantime so we can develop further.
        self.level = Level("basic", 100, 100)
        self.factory.restock_all()

        y = 2
        top_recipe = tiles.RedBlockTop
        middle_recipe = tiles.RedBlockMiddle
        for x in range(100):
            top = self.factory.get_or_create(top_recipe)
            middle = self.factory.get_or_create(middle_recipe)
            # TODO These multipliers aren't explicit, will need an explicit way to convert from
            # TODO World to Screen using a camera
            top.location.x = x
            top.location.y = y
            middle.location.x = x
            middle.location.y = y + 1
            # TODO Not yet very clear when we must assign batches/groups
            top.display.assign(self.batch, self.groups[top_recipe.layer])
            middle.display.assign(self.batch, self.groups[top_recipe.layer])
            self.level.add_static(top)
            self.level.add_static(middle)
