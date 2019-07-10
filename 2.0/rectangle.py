class rect:
    def __init__(self, tl, br):
        self.tl = point(tl[0], tl[1])
        self.br = point(br[0], br[1])

    def getPos(self):
        return (self.tl, self.br)

    def move(self, direction):
        x = direction[0]
        y = direction[1]
        self.tl.x += x
        self.tl.y += y
        self.br.x += x
        self.br.y += y

    def moveTo(self, tl):
        dx = tl[0] - self.tl.x
        dy = tl[1] - self.tl.y
        self.tl.x += dx
        self.tl.y += dy
        self.br.x += dx
        self.br.x += dy

    def collidesWith(self, rec):
        if (self.tl.x > rec.br.x) or (rec.tl.x > self.br.x):
            return False

        if (self.tl.y > rec.br.y) or (rec.tl.y > self.br.y):
            return False

        return True


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
