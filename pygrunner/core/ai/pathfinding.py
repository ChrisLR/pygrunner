import math

from pygrunner.core.keymap import Keymap


def get_dumb_keymaps_to(actor, target_point, can_climb=False, can_fly=False, can_jump=False, stop_at_edge=True):
    static_map_array = actor.location.level.static_collision_map.get_array()

    tile_dist_y = target_point.y - actor.location.y
    tile_dist_x = snap_grid(target_point.x - actor.location.x)

    keymaps = []
    if can_climb or can_fly:
        if tile_dist_y <= -1:
            keymaps.append(Keymap.Up)
            return keymaps
        elif tile_dist_y >= 1:
            keymaps.append(Keymap.Down)
            return keymaps

    if tile_dist_x > 0:
        rect = actor.size.bottom_rectangle
        by = snap_grid(rect.bottom) + 1
        bx = snap_grid(rect.right)
        edge = static_map_array[by][bx]
        if edge:
            if can_jump:
                keymaps.append(Keymap.Jump)
            elif stop_at_edge:
                keymaps.append(Keymap.Right)
        else:
            keymaps.append(Keymap.Right)
    elif tile_dist_x < 0:
        rect = actor.size.bottom_rectangle
        by = snap_grid(rect.bottom) + 1
        bx = snap_grid(rect.left)
        edge = static_map_array[by][bx]
        if edge:
            if can_jump:
                keymaps.append(Keymap.Jump)
            elif stop_at_edge:
                keymaps.append(Keymap.Left)
        else:
            keymaps.append(Keymap.Left)

    return keymaps


def get_keymaps_to(actor, target_point, can_climb=False, can_fly=False, can_jump=False):
    """
    This function returns keymaps to direct a character in the general direction
    of a point. This function gives no guarantee but will be easier on performance
    """
    static_map_array = actor.level.static_collision_map.get_array()

    ghost_point = actor.location.point
    jump_blocks_vertical_max = int(actor.recipe.jump_height / 3)
    jump_blocks_horizontal_max = actor.recipe.move_speed + int(math.ceil(actor.recipe.jump_height / 4))

    closed_nodes = []
    # Horizontal direction
    dir_point = ghost_point.direction_to(target_point)
    step_x = dir_point.x * actor.recipe.move_speed
    step_y = dir_point.y
    temp_target_x = None
    temp_target_y = None

    found = False
    current_path = []
    while found:
        if step_y <= -1:
            # We need to go higher
            if can_fly:
                current_path.append(Keymap.Up)
            elif can_climb:
                # Can we climb straight up?
                if actor.physics.center_climbables:
                    current_path.append(Keymap.Up)
                else:
                    # Is there a point where we CAN climb up?
                    pass
        if step_y == 0:
            # We do not need to go higher.
            pass


def find_horizontal_climbable_point(start_x, start_y, static_map, direction):
    """
    This scans a line, starting at a point and keeping close to the ground
    Trying to get a climbable tile
    """
    left_x = None
    lx = start_x
    floor_y = int(start_y / 32) + 32
    while not left_x:
        if not static_map[lx][floor_y]:
            left_x = lx
        else:
            lx -= 1


def snap_grid(num):
    return int(num / 32)


class Node(object):
    __slots__ = ('x', 'y', 'needs_climb', 'needs_flight', 'needs_jump')

    def __init__(self, x, y, needs_climb, needs_flight, needs_jump):
        self.x = x
        self.y = y
        self.needs_climb = needs_climb
        self.needs_flight = needs_flight
        self.needs_jump = needs_jump
