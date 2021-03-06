import itertools
import copy
from rect import Rect

def bounding_box(rectangles):
    """Return the bounding box enclosing all rectangles."""
    x1 = min(r.x for r in rectangles)
    y1 = min(r.y for r in rectangles)
    x2 = max(r.x2 for r in rectangles)
    y2 = max(r.y2 for r in rectangles)
    return Rect(x1, y1, x2 - x1, y2 - y1)

def intersect(rectangles):
    """Check if any rectangle in the list intersects with any other."""
    for a, b in itertools.combinations(rectangles, 2):
        if a.intersects(b):
            return True
    return False

def uniq(values):
    if len(values) == 0:
        return []
    output = [values[0]]
    prev = values[0]
    for item in values[1:]:
        if prev != item:
            output.append(item)
            prev = item
    return output

def total_area(rectangles):
    """Return the total area of the rectangles."""
    box = bounding_box(rectangles)
    m = [[0]*box.width for _ in range(box.height)]
    for r in rectangles:
        for y in range(r.height):
            for x in range(r.width):
                m[r.y+y-box.y][r.x+x-box.x] = 1

    return sum(sum(w) for w in m)
