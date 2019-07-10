import sys

from rectangle import rect


class Map:
    def __init__(self, game, level):
        self.level = level
        self.game = game

        self.coor = []
        self.lines = []
        self.finish = None

        self.number_enemy = 0
        self.enemy_mov = []
        self.border1 = []
        self.border2 = []
        self.posx = []
        self.posy = []

        self.readFile(level)
        self.drawMap(level)

    def readFile(self, lvl):

        name = ""
        name += "./levels/" + "level" + str(lvl) + ".txt"
        f = open(name)
        self.readInfo(f)
        f = open(name)
        self.parseInput(f)

    def readInfo(self, f):
        for line in f:
            if 'Init' in line:
                break
        self.game.start_x, self.game.start_y = map(int, f.readline().split(","))
        for line in f:
            if 'Enemies' in line:
                break
        self.number_enemy = int(f.readline())
        for i in range(self.number_enemy):
            linha = f.readline().split(",")
            self.posx.append(int(linha[0]))
            self.posy.append(int(linha[1]))
            self.enemy_mov.append((linha[2]))
            self.border1.append(int(linha[3]))
            self.border2.append(int(linha[4]))

    def parseInput(self, f):
        for line in f:
            if 'Map' in line:
                break
        for line in f:
            if 'End' in line:
                break
            temp = line.split(' ')
            self.coor.append((tuple(map(int, temp[0].split(","))),
                             tuple(map(int, temp[1].split(",")))))

    def drawMap(self, level):
        for c in self.coor:
            self.lines.append(self._drawLine(c[0], c[1], 3))

        self.drawFinish(level)

    def drawFinish(self, level):
        name = ""
        name += "./levels/" + "level" + str(level) + ".txt"
        f = open(name)

        for line in f:
            if 'End' in line:
                break
        linha = f.readline().split(",")
        for x in range(0, 4):
            linha[x] = int(linha[x])
        self.finish = self._drawRect((linha[0], linha[1]), linha[2], linha[3])

    def _drawLine(self, start, finish, thickness):
        if start[0] == finish[0]:   # Vertical
            tl_x = start[0] - 1
            tl_y = start[1]
            tl = (tl_x, tl_y)

            br_x = finish[0] - 1
            br_y = finish[1]
            br = (br_x, br_y)

            line = rect(tl, br)
        elif start[1] == finish[1]:   # Horizontal
            tl_x = start[0]
            tl_y = start[1] - 1
            tl = (tl_x, tl_y)

            br_x = finish[0]
            br_y = finish[1] + 1
            br = (br_x, br_y)

            line = rect(tl, br)
        else:   # Diagonal, shouldn't happen
            print("ERROR: Level shouldn't have diagonal lines!")
            sys.exit()

        return line

    def _drawRect(self, tl, w, h):
        br_x = tl[0] + w
        br_y = tl[1] + h
        br = (br_x, br_y)

        rec = rect(tl, br)

        return rec
