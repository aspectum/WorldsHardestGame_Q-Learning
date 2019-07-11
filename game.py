import pickle

from player import Player
from enemy import EnemyCircle
from qLearning import QLearning
from qLearning_offline import QLearning_offline
import temp
from map import Map
from watch import watcher


class Game:

    def __init__(self, level=0, watch=False, watch_periodic=False, replay=False):
        # To show the game
        self.watch = watch
        self.watch_periodic = watch_periodic
        self.replay = replay
        self.watcher_clock_flag = False
        self.watch_period = 50
        self.watch_duration = 10

        # game info
        self.gameContinues = True
        self.isWin = False
        self.level = level

        # Player attributes
        self.pl = None

        # map of the game
        self.map = Map(self, self.level)

        # attributes for enemies
        self.enemies = [None] * self.map.number_enemy

        self.iter_num = 0

        self.player_max_moves = 100
        self.player_max_max_moves = 300
        self.player_vel = 10
        self.player_moves_step = 5
        self.player_moves_interval = 5
        self.eps_decrease_interval = 40
        self.iteration_print_interval = 10
        self.max_iterations = 9999
        self.iter_state = []
        self.colision = False

        # attributes for Q-Learning with incremental learning
        self.learn = QLearning(self)
        self.learn_offline = QLearning_offline(self)
        

    # main game functions
    def start(self):
        if self.colision:
            temp.load_online(self)
        # draw player, enemies and map
        self.createEnv()
        if self.watch or self.watch_periodic:
            self.w = watcher(self, self.watcher_clock_flag)
        self.game_loop()

    def game_loop(self):
        n = 1
        k = 0
        watch_enable = False

        while not self.isWin:
            del self.iter_state[:]
            self.iter_state = []
            self.iter_state.append(self.iter_num)
            self.iter_state.append(self.player_max_moves)
            if self.watch:
                watch_enable = True
            elif self.watch_periodic:
                if self.iter_num // (n * self.watch_period) > 0:
                    watch_enable = True
                    k += 1
                    if k > self.watch_duration:
                        watch_enable = False
                        n += 1
                        k = 0
            else:
                watch_enable = False

            self.init_positions()
            self.pl.mov_num = 0

            while self.gameContinues:
                if watch_enable:
                    self.w.updateMap()
                # a = input()
                if self.colision:
                    self.learn.find_move()
                else:
                    self.learn_offline.find_move()
                self.updateMap(self.level)
                if self.replay:
                    self.save_state()

            # Probably can wrap this in a print state/status method
            if self.iter_num % self.iteration_print_interval == 0:
                self.print_status()
            self.endGame()

            if self.iter_num > self.max_iterations:
                print("Reached maximum of iterations and couldn't hit goal")
                return

    # functions used while game
    def createEnv(self):
        self.pl = Player(self, self.player_vel)

        for i in range(len(self.enemies)):
            self.enemies[i] = EnemyCircle(self, 2*self.player_vel, self.map.enemy_mov[i],
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

    def print_status(self):
        print('Iteration: ', self.iter_num)
        qsz = 0
        if self.colision:
            for i in self.learn.q_value_table:
                for j in self.learn.q_value_table[i]:
                    qsz += len(self.learn.q_value_table[i][j].t)
        #else:
        #    for i in self.learn_offline.q_value_table:
        #       for j in self.learn_offline.q_value_table[i]:
                  #qsz += len(self.learn_offline.q_value_table[i][j])

        print('Q-Table size: ', qsz)

    def save_state(self):
        player = self.pl.rec.getPos()

        enemies = []
        for e in self.enemies:
            enemies.append(e.rec.getPos())

        loop_state = []
        loop_state.append(player)
        loop_state.append(enemies)

        self.iter_state.append(loop_state)

    def endGame(self):

        if self.isWin:
            print("Hooorraaaay")
            print("Win after %d iterations" % self.iter_num)
            print("Max moves: ", self.player_max_moves)
            if not self.colision:
                temp.save_offline(self)
            if self.replay:
                with open('replay.p', 'wb') as f:
                    pickle.dump(self.iter_state, f)
                self.w = watcher(self, self.watcher_clock_flag)
                input('Press ENTER to start replay')
                self.w.replay(self.iter_state)
        else:
            # update Q-Learning variabless
            self.iter_num += 1

            if self.iter_num % self.player_moves_interval == 0:
                if self.player_max_moves < self.player_max_max_moves:
                    self.player_max_moves += self.player_moves_step

            if self.iter_num % self.eps_decrease_interval == 0:
                if self.learn.eps > 0.2:
                    self.learn.eps /= 2
                if self.learn_offline.eps>0.2:
                    self.learn.eps /= 2

            # restart the game

            self.gameContinues = True
