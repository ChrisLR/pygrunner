def complex_pathfinding(actor, target_coordinate, can_climb=False, can_fly=False):
    static_map_array = actor.level.static_collision_map.get_array()
    closed_nodes = []
    open_nodes = []
    ghost_x, ghost_y = actor.location.tuple
    target_x, target_y = target_coordinate
    tries = 10
    while tries:
        columns = static_map_array[ghost_x - 1: ghost_x + 1:]
        top_row = columns[ghost_y - 1]
        middle_row = columns[ghost_y]
        bottom_row = columns[ghost_y + 1]

        for x in range(3):
            # TODO While we detect all 9 squares, we need to only move left, right, up, down
            # TODO The squares will help us determine if we have to jump or not to get there.
            top = top_row[x]
            mid = middle_row[x]
            low = bottom_row[x]
            if mid is None:
                pass
        tries -= 1


class Node(object):
    __slots__ = ('x', 'y', 'needs_climb', 'needs_flight', 'needs_jump')

    def __init__(self, x, y, needs_climb, needs_flight, needs_jump):
        self.x = x
        self.y = y
        self.needs_climb = needs_climb
        self.needs_flight = needs_flight
        self.needs_jump = needs_jump
