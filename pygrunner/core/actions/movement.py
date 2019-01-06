from pygrunner.core.actions.base import Action


class WalkRight(Action):
    @classmethod
    def can_execute(cls, game_object):
        return True

    @classmethod
    def execute(cls, game_object):
        if game_object.physics.velocity_x <= 0:
            game_object.physics.velocity_x += 1
        else:
            game_object.physics.velocity_x = 1
        game_object.flipped = False
        game_object.display.play('run')

class WalkLeft(Action):
    @classmethod
    def execute(cls, game_object):
        if game_object.physics.velocity_x >= 0:
            game_object.physics.velocity_x -= 1
        else:
            game_object.physics.velocity_x = -1
        game_object.flipped = True
        game_object.display.play('run')

    @classmethod
    def can_execute(cls, game_object):
        return True


class Jump(Action):
    @classmethod
    def execute(cls, game_object):
        if game_object.physics.velocity_y == 0:
            game_object.physics.velocity_y -= 16

    @classmethod
    def can_execute(cls, game_object):
        return game_object.physics.bottom_collisions