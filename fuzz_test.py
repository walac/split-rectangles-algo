from random import seed, randint
import time

from split import split_rectangles
from rect import Rect
import utils

def run():
    seed(time.time())
    g = lambda: randint(1, 100)
    while True:
        n = randint(2, 100)
        print(f'n = {n}')
        recs = [Rect(g(), g(), g(), g()) for _ in range(n)]
        result = split_rectangles(recs)
        assert not utils.intersect(result)
        assert utils.bounding_box(recs) == utils.bounding_box(result)
        assert utils.total_area(recs) == sum(r.area for r in result)

if __name__ == '__main__':
    run()
