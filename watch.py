import pygame
import sys


class Watcher:

    black = 0, 0, 0
    white = 255, 255, 255

    def __init__(
        self,
        show="all",
        replay=False,
        period=None,
        duration=None,
        fps=60,
        clock_flag=True,
    ):
        self.game = None
        self.sc = None
        pygame.init()

        self.myfont = pygame.font.SysFont("monospace", 24)
        self.lbl_iter_num = None
        self.lbl_max_moves = None

        self.clock_flag = clock_flag
        self.tick_freq = fps
        self.clock = pygame.time.Clock()

        self.watch_all = False
        self.watch_periodic = False
        if show == "all":
            self.watch_all = True
        elif show == "periodic":
            self.watch_periodic = True
        elif show == "nothing":
            pass
        else:
            print("ERROR: invalid option: show=", show)
        self.period = period
        self.duration = duration

        self.show_replay = replay

        self.first_update = True

    def linkToGame(self, game):
        self.game = game

    # Only creating window on first update
    def createScreen(self, w, h):
        self.sc = pygame.display.set_mode([w, h])
        self.sc.fill(Watcher.white)
        pygame.display.flip()

        self.player_im = pygame.image.load("./img/player.jpg").convert()
        self.enemy_im = pygame.image.load("./img/enemy.jpg").convert()

    def update_map(self):
        if self.first_update:
            self.createScreen(1000, 1000)
            self.first_update = False
        self.check_input()
        self.sc.fill(Watcher.white)

        tl = self.game.pl.rec.get_pos()
        self.sc.blit(self.player_im, tl)
        for e in self.game.enemies:
            tl = e.rec.get_pos()
            self.sc.blit(self.enemy_im, tl)

        self.draw_map()

        self.lbl_iter_num = self.myfont.render(
            "Iter number: " + str(self.game.iter_num), 1, Watcher.black
        )
        self.lbl_max_moves = self.myfont.render(
            "Max moves: " + str(self.game.player_max_moves), 1, Watcher.black
        )

        self.sc.blit(self.lbl_iter_num, (20, 100))
        self.sc.blit(self.lbl_max_moves, (20, 130))

        pygame.display.update()

        if self.clock_flag:
            self.clock.tick(self.tick_freq)

    def draw_map(self):
        for line in self.game.map.lines:
            w = line.br.x - line.tl.x
            h = line.br.y - line.tl.y
            pygame.draw.rect(self.sc, Watcher.black, [line.tl.x, line.tl.y, w, h])

        self.draw_finish()

    def draw_finish(self,):
        w = self.game.map.finish.br.x - self.game.map.finish.tl.x
        h = self.game.map.finish.br.y - self.game.map.finish.tl.y
        pygame.draw.rect(
            self.sc,
            (0, 255, 0),
            [self.game.map.finish.tl.x, self.game.map.finish.tl.y, w, h],
        )

    # Checks if window is open
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def replay(self, state):
        if self.first_update:
            self.createScreen(1000, 1000)
            self.first_update = False
            waitForWindowOnFocus()
        iter_num = state[2]
        max_moves = state[3]

        self.lbl_iter_num = self.myfont.render(
            "Iter number: " + str(iter_num), 1, Watcher.black
        )
        self.lbl_max_moves = self.myfont.render(
            "Max moves: " + str(max_moves), 1, Watcher.black
        )

        for i in range(4, len(state)):
            self.check_input()
            self.sc.fill(Watcher.white)

            tl = state[i][0]
            self.sc.blit(self.player_im, tl)

            if state[1] == 1:
                for e in state[i][1]:
                    self.sc.blit(self.enemy_im, e)

            self.draw_map()

            self.sc.blit(self.lbl_iter_num, (20, 100))
            self.sc.blit(self.lbl_max_moves, (20, 130))

            pygame.display.update()

            if self.clock_flag:
                self.clock.tick(self.tick_freq)

    def quit(self):
        pygame.display.quit()
        pygame.quit()


# On focus and mouse hover
def waitForWindowOnFocus():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 1 and event.gain == 1:
                    return
