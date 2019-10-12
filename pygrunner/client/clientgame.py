import pyglet

from pygrunner.client import input
from pygrunner.client.graphics.spriteloader import SpriteLoader
from pygrunner.core import components
from pygrunner.core.layers import Layer
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.objectpool import ObjectPool
from pygrunner.gamedata.recipes import characters, enemies
from pygrunner.tmx import TmxLoader
from pygrunner.client.hud import HUD


class ClientGame(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.inputs = []
        self.window = None
        self.spriteloader = SpriteLoader()
        self.spriteloader.load_spritesheets(("packed.png",))
        self.factory = Factory(self.spriteloader, ObjectPool())
        self.hud = None
        # DEBUG
        # self.iteration = 0

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
        # For performance testing purposes
        # self.iteration += 1
        # if self.iteration == 100:
        #     pyglet.app.exit()

    def set_clear_color(self, rgb_color):
        r, g, b = rgb_color
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        pyglet.gl.glClearColor(r, g, b, 1)

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
        self.window = pyglet.window.Window(1024, 800)
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
        #self.level = TmxLoader(self.factory).load_map('simple')
        #self.level = TmxLoader(self.factory).load_map('quickmountain')
        self.level = TmxLoader(self.factory).load_map('ladderous')
        bg_color = self.level.background_color
        if bg_color:
            self.set_clear_color(bg_color)

        # TODO A better way to add actors to a game
        players = []
        actor = self.factory.get_or_create(enemies.BlackBat)
        players.append(actor)
        actor.location.set(96, 24)
        actor.replace_component(components.PlayerController(1, self.inputs[0]))
        self.level.add_game_object(actor)

        # actor = self.factory.get_or_create(characters.Turtle)
        # players.append(actor)
        # actor.location.set(96, 24)
        # actor.replace_component(components.PlayerController(2, self.inputs[2]))
        # self.level.add_game_object(actor)

        self.hud = HUD(self, players, self.spriteloader)




