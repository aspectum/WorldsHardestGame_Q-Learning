from player import Player
from enemy import EnemyCircle
from qLearning import QLearning
from map import Map


class Game:

    black = 0, 0, 0
    white = 255, 255, 255

    def __init__(self, w, h):

        # screen sizes
        self.width = w
        self.height = h

        # game info
        self.gameContinues = True
        self.isWin = False
        self.level = 1

        # Player attributes
        self.pl = None

        # map of the game
        self.map = Map(self, 1)

        # attributes for enemies
        self.enemies = [None] * self.map.number_enemy

        # attributes for Q-Learning with incremental learning
        self.learn = QLearning(self)

        self.iter_num = 0
        self.player_max_moves = 100

        # render text
        self.lbl_iter_num = None
        self.lbl_max_moves = None

    def createScreen(self, w, h):
        # pygame.init()
        # self.sc = pygame.display.set_mode([w, h])
        # self.sc.fill(Game.white)
        # pygame.display.flip()
        return

    # main game functions
    def start(self):

        # draw player, enemies and map
        self.createEnv()
        self.game_loop()

    def game_loop(self):

        while not self.isWin:
            self.init_positions()
            self.pl.mov_num = 0

            while self.gameContinues:
                self.learn.find_move()
                self.updateMap(self.level)

            # Probably can wrap this in a print state/status method
            print('Iteration: ', self.iter_num)
            qsz = 0
            for i in self.learn.q_value_table:
                for j in self.learn.q_value_table[i]:
                    qsz += len(self.learn.q_value_table[i][j].t)
            print('Q-Table size: ', qsz)
            self.endGame()

    # functions used while game
    def createEnv(self):
        self.pl = Player(self, 10)

        for i in range(len(self.enemies)):
            self.enemies[i] = EnemyCircle(self, 20, self.map.enemy_mov[i],
                                          self.map.border1[i], self.map.border2[i])

    def init_positions(self):

        # self.pl.set_pos(self.map.start_x, self.map.start_y)
        self.pl.rec.moveTo((self.map.start_x, self.map.start_y))

        for i in range(len(self.enemies)):
            # self.enemies[i].set_pos(self.map.posx[i], self.map.posy[i])
            self.enemies[i].rec.moveTo((self.map.posx[i], self.map.posy[i]))

    def updateMap(self, level):
        for e in self.enemies:
            e.move()

        # self.map.drawMap(level)

    def endGame(self):

        if self.isWin:
            print("Hooorraaaay")
            print("Win after %d iterations" % self.iter_num)
            print("Max moves: ", self.player_max_moves)
        else:
            # update Q-Learning variabless
            self.iter_num += 1

            if self.iter_num % 5 == 0:
                self.player_max_moves += 5

            if self.iter_num % 40 == 0:
                if self.learn.eps > 0.2:
                    self.learn.eps /= 2

            # restart the game

            self.gameContinues = True
