class Rect:
    def __init__(self, tl, br):
        self.tl = Point(tl[0], tl[1])
        self.br = Point(br[0], br[1])

    def get_pos(self):
        return [self.tl.x, self.tl.y], [self.br.x, self.br.y]

    def move(self, direction):
        x = direction[0]
        y = direction[1]
        self.tl.x += x
        self.tl.y += y
        self.br.x += x
        self.br.y += y

    def move_to(self, tl):
        dx = tl[0] - self.tl.x
        dy = tl[1] - self.tl.y
        self.tl.x += dx
        self.tl.y += dy
        self.br.x += dx
        self.br.y += dy

    def collides_with(self, rec):
        if (self.tl.x > rec.br.x) or (rec.tl.x > self.br.x):
            return False

        if (self.tl.y > rec.br.y) or (rec.tl.y > self.br.y):
            return False

        return True


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
