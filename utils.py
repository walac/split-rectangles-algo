import itertools
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
    return any(ra.intersects(rb) for (ra, rb) in
        itertools.combinations(rectangles, 2)
    )

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
    get_collision_boxes = lambda recs: [
        ra.collision_box(rb) for ra, rb in
            itertools.combinations(recs, 2) if ra.intersects(rb)
    ]
    collision_boxes = get_collision_boxes(rectangles)
    collision_area = sum(r.area for r in collision_boxes)
    while intersect(collision_boxes):
        collision_boxes = uniq(get_collision_boxes(collision_boxes))
        collision_area -= sum(r.area for r in collision_boxes)
    return sum(r.area for r in rectangles) - collision_area
