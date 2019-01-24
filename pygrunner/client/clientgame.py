import pyglet

from pygrunner.client import input
from pygrunner.client.graphics.spriteloader import SpriteLoader
from pygrunner.core import components
from pygrunner.core.layers import Layer
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.objectpool import ObjectPool
from pygrunner.gamedata.recipes import characters
from pygrunner.tmx import TmxLoader


class ClientGame(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.inputs = []
        self.window = None
        self.spriteloader = SpriteLoader()
        self.spriteloader.load_spritesheets(("packed.png",))
        self.factory = Factory(self.spriteloader, ObjectPool())


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
        self.factory.restock_all()
        self.level = TmxLoader(self.factory).load_map('simple')

        # TODO This is just for development
        actor = self.factory.get_or_create(characters.HumanMale1)
        actor.location.set(32, 16)
        actor.controller = components.PlayerController(1, self.inputs[0])
        # TODO Not the way it should be done
        actor.controller.register(actor)
        self.level.add_game_object(actor)
