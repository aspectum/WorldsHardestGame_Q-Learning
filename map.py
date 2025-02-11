# Code is a bit hacky and confusing
# Implemented levels 0 to 5
# Ignoring checkpoints (didn't work as expected)

import sys

from rectangle import Rect


class Map:
    def __init__(self, game, level):
        self.level = level

        self.coor = []
        self.lines = []
        self.finish = None

        self.number_enemy = 0
        self.enemy_mov = []
        self.border1 = []
        self.border2 = []
        self.posx = []
        self.posy = []
        self.start_x = []
        self.start_y = []
        self.number_checks = 0
        self.checkpointx = []
        self.checkpointy = []
        self.checkpoints = []

        self.read_file(level)
        self.draw_map(level)
        self.make_checkpoints()
        self.checkpoints.append(self.finish)

    def read_file(self, lvl):

        name = ""
        name += "./levels/" + "level" + str(lvl) + ".txt"
        f = open(name)
        self.read_info(f)
        f = open(name)
        self.parse_input(f)

    def read_info(self, f):
        for line in f:
            if "Init" in line:
                break
        self.start_x, self.start_y = map(int, f.readline().split(","))
        for line in f:
            if "Enemies" in line:
                break
        self.number_enemy = int(f.readline())
        for i in range(self.number_enemy):
            linha = f.readline().split(",")
            self.posx.append(int(linha[0]))
            self.posy.append(int(linha[1]))
            if linha[2] == "True":
                self.enemy_mov.append(True)
            else:
                self.enemy_mov.append(False)
            self.border1.append(int(linha[3]))
            self.border2.append(int(linha[4]))
        f.readline()
        number_checkpoints = int(f.readline())
        for i in range(number_checkpoints):
            linha = f.readline().split(",")
            self.checkpointx.append(int(linha[0]))
            self.checkpointy.append(int(linha[1]))

    def parse_input(self, f):
        for line in f:
            if "Map" in line:
                break
        for line in f:
            if "End" in line:
                break
            temp = line.split(" ")
            self.coor.append(
                (
                    tuple(map(int, temp[0].split(","))),
                    tuple(map(int, temp[1].split(","))),
                )
            )

    def draw_map(self, level):
        for c in self.coor:
            self.lines.append(self.draw_line(c[0], c[1], 3))

        self.draw_finish(level)

    def draw_finish(self, level):
        name = ""
        name += "./levels/" + "level" + str(level) + ".txt"
        f = open(name)

        for line in f:
            if "End" in line:
                break
        linha = f.readline().split(",")
        for x in range(0, 4):
            linha[x] = int(linha[x])
        self.finish = self.draw_rect((linha[0], linha[1]), linha[2], linha[3])

    def draw_line(self, start, finish, thickness):
        if start[0] == finish[0]:  # Vertical
            if start[1] > finish[1]:
                temp = start
                start = finish
                finish = temp
            tl_x = start[0] - 1
            tl_y = start[1]
            tl = (tl_x, tl_y)

            br_x = finish[0] - 1
            br_y = finish[1]
            br = (br_x, br_y)

            line = Rect(tl, br)
        elif start[1] == finish[1]:  # Horizontal
            if start[0] > finish[0]:
                temp = start
                start = finish
                finish = temp
            tl_x = start[0]
            tl_y = start[1] - 1
            tl = (tl_x, tl_y)

            br_x = finish[0]
            br_y = finish[1] + 1
            br = (br_x, br_y)

            line = Rect(tl, br)
        else:  # Diagonal, shouldn't happen
            print("ERROR: Level shouldn't have diagonal lines!")
            print(start)
            print(finish)
            sys.exit()

        return line

    def draw_rect(self, tl, w, h):
        br_x = tl[0] + w
        br_y = tl[1] + h
        br = (br_x, br_y)

        rec = Rect(tl, br)

        return rec

    def make_checkpoints(self):
        for i in range(len(self.checkpointx)):
            c = Rect(
                (self.checkpointx[i] - 5, self.checkpointy[i] - 5),
                (self.checkpointx[i] + 5, self.checkpointy[i] + 5),
            )
            self.checkpoints.append(c)
