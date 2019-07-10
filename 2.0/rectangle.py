class rect:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br

    def getPos(self):
        return (self.tl, self.br)

    def move(self, x, y):
        self.tl[0] += x
        self.tl[1] += y
        self.br[0] += x
        self.br[1] += y

    def collidesWith(self, rec):
        if (self.tl[0] > rec.br[0]) or (rec.tl[0] > self.br[0]):
            return False

        if (self.tl[1] > rec.br[1]) or (rec.tl[1] > self.br[1]):
            return False

        return True
