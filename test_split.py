import utils
from split import split_rectangles
from rect import Rect

test_cases = [
    (
        Rect(0, 0, 2, 2),
        Rect(1, 1, 2, 2)
    ),
    (
        Rect(1, 1, 2, 2),
        Rect(9, 1, 2, 2),
        Rect(1, 7, 2, 2),
        Rect(9, 7, 2, 2),
        Rect(0, 4, 4, 2),
        Rect(8, 4, 4, 2),
        Rect(2, 2, 8, 6),
        Rect(5, 0, 2, 10),
    ),
    (
        Rect(1, 1, 3, 3),
        Rect(2, 2, 3, 3),
        Rect(3, 0, 3, 3),
    ),
    (
        Rect(0, 0, 4, 4),
        Rect(1, 1, 2, 2),
    ),
]

def test_split_rectangles():
    for tc in test_cases:
        result = split_rectangles(tc)
        info = f'{tc} {result}'
        assert not utils.intersect(result), info
        assert utils.total_area(tc) == sum(r.area for r in result), info
        assert utils.bounding_box(tc) == utils.bounding_box(result), info

def test_no_intersection():
    recs = [
        Rect(0, 0, 1, 1),
        Rect(2, 2, 1, 1),
        Rect(3, 3, 1, 1),
    ]

    recs.sort()
    result = split_rectangles(recs)
    result.sort()

    assert not any(a != b for a, b in zip(recs, result))

def test_adjacent():
    recs = [
            Rect(0, 0, 1, 1),
            Rect(0, 1, 1, 1),
            Rect(1, 0, 1, 1),
    ]

    recs.sort()
    result = split_rectangles(recs)
    result.sort()
