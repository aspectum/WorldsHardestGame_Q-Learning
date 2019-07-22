import pickle

from player import Player
from enemy import EnemyCircle
from qLearning import QLearning
import qLearning
from map import Map


class Game:
    def __init__(self, level=0, watcher=None, colision=True):
        # watcher settings (to show game)
        self.watcher = watcher
        self.watch = None
        self.show_replay = None
        if self.watcher is not None:
            self.watcher.linkToGame(self)
            self.watch = self.watcher.watch_all or self.watcher.watch_periodic
            self.show_replay = self.watcher.show_replay

        # game info
        self.game_continues = True
        self.is_win = False
        self.level = level

        # Player attributes
        self.player = None

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
        self.colision = colision
        self.checkpoints = False
        self.constant_eps = False
        self.replay_file_only = False

        self.epochs = 0
        self.qsz = 0

        # draw player, enemies and map
        self.create_env()

        # attributes for Q-Learning with incremental learning
        self.learn = QLearning(self, online=colision)

    # Starting game
    def start(self):
        if self.colision:
            qLearning.load_online(self)
        self.game_loop()
        if not self.colision:
            qLearning.save_offline(self, False)
        if self.watcher is not None:
            self.watcher.quit()

    def game_loop(self):

        while not self.is_win:
            self.restart_state()
            self.init_positions()
            self.player.mov_num = 0

            while self.game_continues:
                if self.should_i_watch():
                    self.watcher.update_map()
                self.learn.find_move()
                self.update_map(self.level)
                self.save_state()

            self.print_status()
            self.end_game()

            if self.iter_num > self.max_iterations:
                print("Reached maximum of iterations and couldn't hit goal")
                return

    # functions used while game
    def create_env(self):
        self.player = Player(self, self.player_vel)

        for i in range(len(self.enemies)):
            self.enemies[i] = EnemyCircle(
                self,
                2 * self.player_vel,
                self.map.enemy_mov[i],
                self.map.border1[i],
                self.map.border2[i],
            )

    def init_positions(self):
        self.player.rec.move_to((self.map.start_x, self.map.start_y))

        for i in range(len(self.enemies)):
            self.enemies[i].rec.move_to((self.map.posx[i], self.map.posy[i]))

    def update_map(self, level):
        for e in self.enemies:
            e.move()

    def should_i_watch(self):
        if self.watch:
            if self.watcher.watch_all:
                return True
            elif self.watcher.watch_periodic:
                if self.iter_num % self.watcher.period < self.watcher.duration:
                    return True

        return False

    def print_status(self):
        qsz = 0
        if self.colision:
            for i in self.learn.q_value_table:
                for j in self.learn.q_value_table[i]:
                    qsz += len(self.learn.q_value_table[i][j].t)
        self.qsz = qsz
        if self.iter_num % self.iteration_print_interval == 0:
            print("Iteration: ", self.iter_num)
            print("Q-Table size: ", qsz)

    def restart_state(self):
        del self.iter_state[:]
        self.iter_state = []
        self.iter_state.append(self.level)
        if self.colision:
            self.iter_state.append(1)
        else:
            self.iter_state.append(0)
        self.iter_state.append(self.iter_num)
        self.iter_state.append(self.player_max_moves)

    def save_state(self):
        player = self.player.rec.get_pos()

        enemies = []
        for e in self.enemies:
            enemies.append(e.rec.get_pos())

        loop_state = []
        loop_state.append(player)
        loop_state.append(enemies)

        self.iter_state.append(loop_state)

    def end_game(self):
        self.iter_num += 1
        if self.is_win:
            print("Hooorraaaay")
            print("Win after %d iterations" % self.iter_num)
            print("Max moves: ", self.player_max_moves)
            print("Moves used: ", self.player.mov_num)
            self.epochs = self.iter_num
            if self.colision:
                qLearning.save_online(self)
                replay_fname = "result/replay.p"
            else:
                replay_fname = "result/replay_offline.p"
                qLearning.save_offline(self, True)
                self.is_win = False
                self.game_continues = True
            with open(replay_fname, "wb") as f:
                pickle.dump(self.iter_state, f)
            if self.watcher is not None:
                if self.watcher.show_replay:
                    input("Press ENTER to start replay")
                    self.watcher.replay(self.iter_state)
        else:
            if self.iter_num % self.player_moves_interval == 0:
                if self.player_max_moves < self.player_max_max_moves:
                    self.player_max_moves += self.player_moves_step

            if (not self.constant_eps) and (
                self.iter_num % self.eps_decrease_interval == 0
            ):
                if self.learn.eps > 0.2:
                    self.learn.eps /= 2

            # restart the game

            self.game_continues = True
