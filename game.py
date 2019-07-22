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

        # initializing player
        self.player = None

        # map of the game
        self.map = Map(self, self.level)

        # initializing enemies
        self.enemies = [None] * self.map.number_enemy

        self.iter_num = 0  # number of current iteration
        self.player_max_moves = (
            100
        )  # max player moves at current iteration (kills player after max_moves)
        self.player_max_max_moves = (
            300
        )  # max_moves grows over iterations until max_max_moves
        self.player_vel = (
            10
        )  # "velocity", but it's more like a step size (used to discretize map, hard to solve with vel below 5)
        self.player_moves_step = (
            5
        )  # every player_moves_interval iterations, player_max_moves increases by player_modes_step
        self.player_moves_interval = 5
        self.eps_decrease_interval = (
            40
        )  # if constant_eps is false, every eps_decrease_interval iterations epsilon is halved
        self.iteration_print_interval = 10  # print info periodically
        self.max_iterations = 9999  # max iterations before giving up
        self.iter_state = []  # "state" of current iteration (player movement history)
        self.colision = colision
        self.checkpoints = False  # not implemented correctly, leave False
        self.constant_eps = False  # ignore eps_decrease_interval

        self.qtable_size = 0  # size of qtable at current iteration

        # create player and enemies
        self.create_env()

        # create qlearning object
        self.learn = QLearning(self, online=colision)

    # starting game
    def start(self):
        if self.colision:
            qLearning.load_offline_qtable(self)

        self.game_loop()

        if not self.colision:
            qLearning.save_offline_qtable(self, False)

        if self.watcher is not None:
            self.watcher.quit()

    def game_loop(self):
        while not self.is_win:  # learning loop
            self.restart_state()
            self.init_positions()
            self.player.mov_num = 0

            while self.game_continues:  # game loop on single learning iteration
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

    # create player and enemies
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

    # put player and enemies on starting positions
    def init_positions(self):
        self.player.rec.move_to((self.map.start_x, self.map.start_y))

        for i in range(len(self.enemies)):
            self.enemies[i].rec.move_to((self.map.posx[i], self.map.posy[i]))

    # move enemies to next position
    def update_map(self, level):
        for e in self.enemies:
            e.move()

    # checks if should display this iteration
    def should_i_watch(self):
        if self.watch:
            if self.watcher.watch_all:
                return True
            elif self.watcher.watch_periodic:
                if self.iter_num % self.watcher.period < self.watcher.duration:
                    return True

        return False

    # prints learning progress info
    def print_status(self):
        qtable_size = 0
        if self.colision:
            for i in self.learn.q_value_table:
                for j in self.learn.q_value_table[i]:
                    qtable_size += len(self.learn.q_value_table[i][j].t)
        self.qtable_size = qtable_size
        if self.iter_num % self.iteration_print_interval == 0:
            print("Iteration: ", self.iter_num)
            print("Q-Table size: ", qtable_size)

    # restarts state variable with new iteration
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

    # saves player and enemies positions
    def save_state(self):
        player = self.player.rec.get_pos()

        enemies = []
        for e in self.enemies:
            enemies.append(e.rec.get_pos())

        loop_state = []
        loop_state.append(player)
        loop_state.append(enemies)

        self.iter_state.append(loop_state)

    # end of iteration procedures
    def end_game(self):
        self.iter_num += 1
        if self.is_win:
            print("Hooorraaaay")
            print("Win after %d iterations" % self.iter_num)
            print("Max moves: ", self.player_max_moves)
            print("Moves used: ", self.player.mov_num)
            if self.colision:
                qLearning.save_online(self)
                replay_fname = "result/replay.p"
            else:
                replay_fname = "result/replay_offline.p"
                qLearning.save_offline_qtable(self, True)
                self.is_win = False  # keeps going on to learn better path
                self.game_continues = True
            with open(replay_fname, "wb") as f:
                pickle.dump(self.iter_state, f)
            if self.watcher is not None:
                if self.watcher.show_replay:
                    input("Press ENTER to start replay")
                    self.watcher.replay(self.iter_state)
        else:
            if (
                self.iter_num % self.player_moves_interval == 0
            ):  # increasing player_max_moves
                if self.player_max_moves < self.player_max_max_moves:
                    self.player_max_moves += self.player_moves_step

            if (not self.constant_eps) and (  # halving epsilon
                self.iter_num % self.eps_decrease_interval == 0
            ):
                if self.learn.eps > 0.2:  # "minimum" epsilon
                    self.learn.eps /= 2

            self.game_continues = True
