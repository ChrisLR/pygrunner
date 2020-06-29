from pyg2d.core.geom import Rectangle, Point


def test_intersects_horizontally():
    rect_1 = Rectangle(1, 0, 10, 1)
    rect_2 = Rectangle(5, 0, 10, 1)

    assert rect_1.intersects(rect_2)
    assert rect_2.intersects(rect_1)


def test_intersects_vertically():
    rect_1 = Rectangle(0, 1, 1, 10)
    rect_2 = Rectangle(0, 5, 1, 10)

    assert rect_1.intersects(rect_2)
    assert rect_2.intersects(rect_1)


def test_does_not_intersect_horizontally():
    rect_1 = Rectangle(1, 1, 10, 1)
    rect_2 = Rectangle(12, 1, 10, 1)

    assert not rect_1.intersects(rect_2)
    assert not rect_2.intersects(rect_1)


def test_does_not_intersect_vertically():
    rect_1 = Rectangle(1, 1, 1, 10)
    rect_2 = Rectangle(1, 12, 1, 10)

    assert not rect_1.intersects(rect_2)
    assert not rect_2.intersects(rect_1)


def test_point_calculates_distance_correctly():
    point_1 = Point(1, 1)
    point_2 = Point(2, 2)
    point_3 = Point(5, 6)

    assert point_1.distance_to(point_2) == 1
    assert point_2.distance_to(point_1) == 1
    assert point_1.distance_to(point_3) == 6
