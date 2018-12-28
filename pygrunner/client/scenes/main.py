import pyglet

from pygrunner.client.scenes.base import Scene
from pygrunner.core.keymap import Keymap


class MainMenu(Scene):
    def __init__(self, inputs, window, game):
        super().__init__(inputs, window, game)
        self.labels = [
            pyglet.text.Label(
                'Start',
                font_name='Times New Roman',
                font_size=36,
                x=window.width // 2,
                y=window.height // 2,
                anchor_x='center',
                anchor_y='center'),
            pyglet.text.Label(
                'Exit',
                font_name='Times New Roman',
                font_size=36,
                x=window.width // 2,
                y=window.height // 2 - 36,
                anchor_x='center',
                anchor_y='center')
        ]
        self.focused_label_index = 0

    def on_draw(self):
        # TODO UI Controls should be batched
        for label in self.labels:
            label.draw()

    def update(self, dt):
        new_input = self.get_all_input()
        if new_input:
            self.handle_keymap_input(new_input)

    def handle_keymap_input(self, keymap_input):
        if Keymap.Up in keymap_input:
            self.cycle_focus_previous()
        elif Keymap.Down in keymap_input:
            self.cycle_focus_next()

    def cycle_focus_next(self):
        # TODO This will be necessary in many scenes, need composition
        old_label = self.labels[self.focused_label_index]
        self.focused_label_index += 1
        if self.focused_label_index >= len(self.labels):
            self.focused_label_index = 0
        new_label = self.labels[self.focused_label_index]
        old_label.color = (255, 255, 255, 255)
        new_label.color = (0, 255, 255, 255)

    def cycle_focus_previous(self):
        # TODO This will be necessary in many scenes, need composition
        old_label = self.labels[self.focused_label_index]
        self.focused_label_index -= 1
        if self.focused_label_index < 0:
            self.focused_label_index = len(self.labels) - 1
        new_label = self.labels[self.focused_label_index]
        old_label.color = (255, 255, 255, 255)
        new_label.color = (0, 255, 255, 255)
