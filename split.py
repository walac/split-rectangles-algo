import heapq
import itertools
import intervaltree

from rect import Rect

class Event:
    """
    Represents a sweep line event.

    The event ENTER is for when we are starting to scan a rectangle.
    The event LEAVE is for when we are done with the rectangle.
    """
    ENTER = 1
    LEAVE = 2

    def __init__(self, r, event_type):
        self.rect = r
        self.event = event_type

    def __lt__(self, rhs):
        my_x = self.rect.x if self.event == Event.ENTER else self.rect.x2
        rhs_x = rhs.rect.x if rhs.event == Event.ENTER else rhs.rect.x2
        # the IntervalTree we are using compare intervals in closed sets,
        # but we need open set comparison, because two adjacent rectangles
        # are not intersected. To get the intended behavior, if two rectangles
        # match their x coordinate, we process first the LEAVE event.
        # Example:
        #
        # ----------------
        # |       |      |
        # |   A   |   B  |
        # |       |      |
        # ----------------
        #
        # The x2 coordinate of A is equal to the x coordinate of B,
        # but they don't overlap each other.
        if my_x == rhs_x:
            return self.event == Event.LEAVE
        return my_x < rhs_x

    def __repr__(self):
        return f'Event({"ENTER" if self.event == Event.ENTER else "LEAVE"}, {self.rect})'

def generate_events(rectangles):
    """For each rectangle, generate ENTER and LEAVE event objects."""
    evs = lambda r: [Event(r, Event.ENTER), Event(r, Event.LEAVE)]
    events = [evs(r) for r in rectangles]
    return list(itertools.chain(*events))

def split_rectangles(rectangles):
    """
    Given a set of possibly intersecting rectangles, return another
    set of non-intersecting retangles the ocuppies the same area

    If uses the sweep interval algorithm to detect the intersections
    in linearithimic time.
    """
    events = generate_events(rectangles)
    heapq.heapify(events)
    intervals = intervaltree.IntervalTree()
    result = []
    removed = set()

    while True:
        try:
            ev = heapq.heappop(events)
        except IndexError:
            return result

        if ev.rect in removed:
            continue

        if ev.event == Event.ENTER:
            for intersection in intervals.overlap(ev.rect.y, ev.rect.y2):
                rinter = intersection.data

                # compute the set of split rectangles
                split = [ev.rect.collision_box(rinter)]
                split.extend(rinter - ev.rect)
                split.extend(ev.rect - rinter)

                intervals.remove(intersection)

                # Unfortunately we can't make a random remove from the
                # priority queue, so we mark the old rectangles as removed
                removed.add(ev.rect)
                removed.add(rinter)

                for event in generate_events(split):
                    heapq.heappush(events, event)

                break
            else:
                intervals.addi(ev.rect.y, ev.rect.y2, ev.rect)
        else:
            result.append(ev.rect)
            intervals.removei(ev.rect.y, ev.rect.y2, ev.rect)

if __name__ == '__main__':
    recs = [Rect(0, 0, 2, 2), Rect(1, 1, 2, 2)]
    # print(f'{recs} = {split_rectangles(recs)}')
    recs = [
        Rect(1, 1, 2, 2),
        Rect(9, 1, 2, 2),
        Rect(1, 7, 2, 2),
        Rect(9, 7, 2, 2),
        Rect(0, 4, 4, 2),
        Rect(8, 4, 4, 2),
        Rect(2, 2, 8, 6),
        Rect(5, 0, 2, 10),
    ]
    #print(split_rectangles(recs))
    recs = [
        Rect(1, 1, 3, 3),
        Rect(2, 2, 3, 3),
        Rect(3, 0, 3, 3),
    ]
    print(split_rectangles(recs))
