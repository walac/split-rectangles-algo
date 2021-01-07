class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    @property
    def area(self):
        return self.width * self.height

    def intersects(self, rhs):
        return not (rhs.x2 <= self.x
            or rhs.y2 <= self.y
            or rhs.x >= self.x2
            or rhs.y >= self.y2)

    def collision_box(self, rhs):
        """Return the collision box of two intersecting rectangles."""
        x = max(self.x, rhs.x)
        y = max(self.y, rhs.y)
        x2 = min(self.x2, rhs.x2)
        y2 = min(self.y2, rhs.y2)
        return Rect(x, y, x2 - x, y2 - y)

    def __contains__(self, r):
        """Check if r is contained in us."""
        return r.x >= self.x    \
            and r.y >= self.y   \
            and r.x2 <= self.x2 \
            and r.y2 <= self.y2

    def __hash__(self):
        return id(self)

    def __sub__(self, rhs):
        """Implements the 4-zone Rectangle Difference Algorithm."""
        result = []

        if self in rhs:
            return result

        # compute the top rectangle
        ra_height = rhs.y - self.y
        if ra_height > 0:
            result.append(Rect(self.x, self.y, self.width, ra_height))

        # compute the bottom rectangle
        rb_height = self.height - (rhs.y2 - self.y)
        if rb_height > 0 and rhs.y2 < self.y2:
            result.append(Rect(self.x, rhs.y2, self.width, rb_height))

        y1 = rhs.y if rhs.y > self.y else self.y
        y2 = rhs.y2 if rhs.y2 < self.y2 else self.y2
        rc_height = y2 - y1

        # compute the left triangle
        rc_width = rhs.x - self.x
        if rc_width > 0 and rc_height > 0:
            result.append(Rect(self.x, y1, rc_width, rc_height))

        # compute the right rectangle
        rd_width = self.width - (rhs.x2 - self.x)
        if rd_width > 0:
            result.append(Rect(rhs.x2, y1, rd_width, rc_height))

        return result

    def __lt__(self, rhs):
        if self.x < rhs.x:
            return True
        if self.x == rhs.x and self.y < rhs.y:
            return True
        return False

    def __eq__(self, rhs):
        return self.x == rhs.x              \
            and self.width == rhs.width     \
            and self.y == rhs.y             \
            and self.height == rhs.height

    def __ne__(self, rhs):
        return not self == rhs

    def __repr__(self):
        return f'Rect({self.x}, {self.y}, {self.width}, {self.height})'

if __name__ == '__main__':
    ra = Rect(0, 0, 2, 2)
    rb = Rect(1, 1, 2, 2)
    print(f'{ra} - {rb} = {ra - rb}')
    print(f'{rb} - {ra} = {rb - ra}')
    ra = Rect(0, 1, 3, 2)
    rb = Rect(1, 0, 1, 4)
    print(f'{ra} - {rb} = {ra - rb}')
    print(f'{rb} - {ra} = {rb - ra}')
