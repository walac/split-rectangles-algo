from rect import Rect
import utils

intersection_pairs = [
    # rec a, rec b, a.collision_box(b)
    (Rect(0, 0, 2, 2), Rect(1, 1, 2, 2), Rect(1, 1, 1, 1)),
    (Rect(0, 1, 3, 1), Rect(1, 0, 1, 3), Rect(1, 1, 1, 1)),
    (Rect(0, 0, 4, 4), Rect(2, 3, 3, 4), Rect(2, 3, 2, 1)),
    (Rect(0, 1, 2, 2), Rect(1, 0, 2, 2), Rect(1, 1, 1, 1)),
    (Rect(0, 0, 4, 4), Rect(1, 1, 2, 2), Rect(1, 1, 2, 2)),
]

def test_area():
    assert Rect(0, 0, 1, 1).area == 1
    assert Rect(0, 0, 2, 2).area == 4
    assert Rect(0, 0, 3, 4).area == 12
    assert Rect(0, 0, 4, 3).area == 12
    assert Rect(1, 1, 4, 3).area == 12

def test_intersects():
    for a, b, _ in intersection_pairs:
        assert a.intersects(b), f'{a} {b}'
        assert b.intersects(a), f'{b} {a}'

    assert not Rect(1, 1, 1, 1).intersects(Rect(4, 4, 2, 2))

def test_collision_box():
    for a, b, c in intersection_pairs:
        assert a.collision_box(b) == c, f'{a}.collision_box({b} != {c}'
        assert b.collision_box(a) == c, f'{a}.collision_box({b} != {c}'

    r = Rect(0, 0, 2, 2)
    assert r.collision_box(r) == r

def test_subtraction():
    for a, b, _ in intersection_pairs:
        result = a - b
        result.extend(b - a)
        assert utils.bounding_box([a, b]) == utils.bounding_box(result), f'{a} {b} {result}'
        assert sum(
            r.area for r in result) + a.collision_box(b).area == utils.total_area([a, b]
        ), f'{a} {b} {result}'

    a = Rect(0, 0, 2, 2)
    assert len(a - a) == 0
