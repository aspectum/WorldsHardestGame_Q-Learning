import pygame
import sys


class watcher:

    black = 0, 0, 0
    white = 255, 255, 255

    def __init__(self, game, clock_flag=False):
        self.game = game
        self.sc = None
        self.createScreen(1000, 1000)
        # self.drawMap(self.game.level)
        self.myfont = pygame.font.SysFont("monospace", 24)
        # render text
        self.lbl_iter_num = None
        self.lbl_max_moves = None
        self.player_im = pygame.image.load("./img/player.jpg").convert()
        self.enemy_im = pygame.image.load("./img/enemy.jpg").convert()

        self.clock_flag = clock_flag

        self.tick_freq = 60
        self.clock = pygame.time.Clock()

        self.updateMap()

    def createScreen(self, w, h):
        pygame.init()
        self.sc = pygame.display.set_mode([w, h])
        self.sc.fill(watcher.white)
        pygame.display.flip()

    def updateMap(self):
        self.check_input()
        self.sc.fill(watcher.white)

        tl = self.game.pl.rec.getPos()
        self.sc.blit(self.player_im, tl)
        for e in self.game.enemies:
            tl = e.rec.getPos()
            self.sc.blit(self.enemy_im, tl)

        self.drawMap()

        self.lbl_iter_num = self.myfont.render("Iter number: " + str(self.game.iter_num), 1, watcher.black)
        self.lbl_max_moves = self.myfont.render("Max moves: " + str(self.game.player_max_moves),
                                                1, watcher.black)

        self.sc.blit(self.lbl_iter_num, (20, 100))
        self.sc.blit(self.lbl_max_moves, (20, 130))

        pygame.display.update()

        if self.clock_flag:
            self.clock.tick(self.tick_freq)

    def drawMap(self):
        # for c in self.game.map.coor:
        #     pygame.draw.line(self.sc, watcher.black, c[0], c[1], 3)
        for line in self.game.map.lines:
            w = line.br.x - line.tl.x
            h = line.br.y - line.tl.y
            # rec = pygame.rect(self.game.map.finish.tl.x, self.game.map.finish.tl.y, w, h)
            pygame.draw.rect(self.sc, watcher.black,
                             [line.tl.x, line.tl.y, w, h])

        self.drawFinish()

    def drawFinish(self, ):
        w = self.game.map.finish.br.x - self.game.map.finish.tl.x
        h = self.game.map.finish.br.y - self.game.map.finish.tl.y
        # rec = pygame.rect(self.game.map.finish.tl.x, self.game.map.finish.tl.y, w, h)
        pygame.draw.rect(self.sc, (0, 255, 0),
                         [self.game.map.finish.tl.x, self.game.map.finish.tl.y, w, h])

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def replay(self, state):
        iter_num = state[0]
        max_moves = state[1]

        self.lbl_iter_num = self.myfont.render("Iter number: " + str(iter_num), 1, watcher.black)
        self.lbl_max_moves = self.myfont.render("Max moves: " + str(max_moves),
                                                1, watcher.black)

        for i in range(2, len(state)):
            self.check_input()
            self.sc.fill(watcher.white)

            tl = state[i][0]
            self.sc.blit(self.player_im, tl)
            for e in state[i][1]:
                self.sc.blit(self.enemy_im, e)

            self.drawMap()

            self.sc.blit(self.lbl_iter_num, (20, 100))
            self.sc.blit(self.lbl_max_moves, (20, 130))

            pygame.display.update()

            if self.clock_flag:
                self.clock.tick(self.tick_freq)
