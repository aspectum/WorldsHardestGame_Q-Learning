import pygame

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
            self.coor.append((tuple(map(int, temp[0].split(","))), tuple(map(int, temp[1].split(",")))))


    def drawMap(self, level):
        for c in self.coor:
            self.lines.append(pygame.draw.line(self.game.sc, self.game.black, c[0], c[1], 3))
        
        self.drawFinish(level)
    
    def drawFinish(self, level):
        name = ""
        name += "./levels/" + "level" + str(level) + ".txt"
        f = open(name)

        for line in f:
            if 'End' in line:
                break
        linha = f.readline().split(",")
        for x in range(0,4):
            linha[x] = int(linha[x])
        self.finish = pygame.draw.rect(self.game.sc, (0, 255, 0), [linha[0], linha[1], linha[2], linha[3]])


    