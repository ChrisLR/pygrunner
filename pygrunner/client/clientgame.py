import pyglet

from pygrunner.client.graphics.spriteloader import SpriteLoader
from pygrunner.core import controllers
from pygrunner.client import input


class ClientGame(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.inputs = []
        self.window = None
        self.spriteloader = SpriteLoader()

    def on_draw(self):
        self.window.clear()
        self.scene_manager.on_draw()

    def on_key_press(self, symbol, modifiers):
        for controller in self.inputs:
            controller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for controller in self.inputs:
            controller.on_key_release(symbol, modifiers)

    def update(self, dt):
        self.scene_manager.update(dt)

    def start(self):
        self.initialize_keyboard_players()
        self.initialize_joystick_players()
        self.initialize_ui()
        pyglet.clock.schedule_interval(self.update, 1 / 1000)
        pyglet.app.run()
        self.scene_manager.start(self.inputs)

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

    def initialize_joystick_players(self):
        joysticks = pyglet.input.get_joysticks()
        for joystick in joysticks:
            joystick.open()
            # TODO Handle customized Mapping
            joystick_mapping = input.JoystickMapping.default()
            joystick_input = input.Joystick(joystick, joystick_mapping)
            self.inputs.append(joystick_input)
