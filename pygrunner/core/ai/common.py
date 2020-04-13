def find_closest_player(game, point):
    closest = min(game.players, key= lambda player: player.location.point.distance_to(point))
    return closest


def find_closest_in_objects(objects, point):
    closest = min(objects, key=lambda obj: obj.location.point.distance_to(point))
    return closest
