import random
from collections import defaultdict
import time
import os
# from shutil import copyfile

MOVES = ["right", "left", "up", "down", "stay"]  # Possible moves


# Q-table and helper methods
class QLearning:
    def __init__(self, game, online=True):
        self.pl = game.pl
        self.game = game

        self.eps = 0.2      # Random action chance
        self.lr = 0.4       # Learning rate
        self.gamma = 0.9    # Future rewards multiplicator (discount)

        if online:
            self.q_value_table = self.mult_dim_dict(2, QValues, self)
        else:
            self.q_value_table = self.mult_dim_dict(2, QValues_offline, self)

    def mult_dim_dict(self, dim, dict_type, params):
        if dim == 1:
            return defaultdict(lambda: dict_type(params))
        else:
            return defaultdict(lambda: self.mult_dim_dict(dim - 1, dict_type, params))

    def find_move(self):
        r = random.random()
        if r < self.eps:
            self.move_randomly()
        else:
            self.move_optimally()
        x, y = self.game.pl.rec.tl.x, self.game.pl.rec.tl.y
        self.q_value_table[x][y].update_value()

    def move_randomly(self):
        i = random.randint(0, len(MOVES) - 1)
        self.game.pl.move(MOVES[i])

    def move_optimally(self):
        self.game.pl.move(self.find_best_move())

    def find_max_reward(self):
        li = []
        for m in MOVES:
            x, y = self.pl.move_simulation(m)
            li.append(self.q_value_table[x][y].get_val_at_t(self.pl.mov_num + 1))
        maxi = max(li)

        return maxi, li

    def find_best_move(self):
        maxi, li = self.find_max_reward()
        maxes = [i for i, x in enumerate(li) if x == maxi]
        if len(maxes) > 1:  # Between equally good moves, choose randomly
            i = random.randint(0, len(maxes) - 1)
            best_move = MOVES[i]
        else:
            best_move = MOVES[li.index(maxi)]

        return best_move


class QValues:
    def __init__(self, QLearning):

        self.QL = QLearning
        self.table = self.QL.q_value_table

        self.pl = self.QL.game.pl
        self.val = []       # values in each 'time' (self.t)
        self.t = []         # 'time' (more like tick number or iteration) - representing 'board state' (i.e. enemy positions) with a single value
        self.init_val = 0   # initial value

    def update_value(self):

        if self.pl.mov_num not in self.t:
            self.t.append(self.pl.mov_num)
            self.val.append(self.init_val)

        # reward = -1  #  Not using this reward in online mode

        best_reward, _ = self.QL.find_max_reward()

        # Classic Q-Learning learning formula
        self.val[self.t.index(self.pl.mov_num)] += self.QL.lr * (self.QL.gamma * best_reward - self.val[self.t.index(self.pl.mov_num)])

    def update_after_death(self):
        if self.pl.mov_num not in self.t:
            self.t.append(self.pl.mov_num)
            self.val.append(-3000)
        else:
            self.val[self.t.index(self.pl.mov_num)] -= 3000

    def update_wall_colision(self):
        if self.pl.mov_num not in self.t:
            self.t.append(self.pl.mov_num)
            self.val.append(-500)
        else:
            self.val[self.t.index(self.pl.mov_num)] -= 500

    def update_game_won(self):
        if self.pl.mov_num not in self.t:
            self.t.append(self.pl.mov_num)
            self.val.append(100000 / self.QL.game.pl.mov_num)
        else:
            self.val[self.t.index(self.pl.mov_num)] += 100000 / self.QL.game.pl.mov_num

    def get_val_at_t(self, mov):
        if mov in self.t:
            return self.val[self.t.index(mov)]
        else:
            return self.init_val


class QValues_offline:
    def __init__(self, QLearning):

        self.QL = QLearning
        self.table = self.QL.q_value_table

        self.val = 0  # single value (no enemies -> no different board states for same position)

    def update_value(self):
        reward = -1  # If player keeps going to same places, this starts to add up, so motivates it to explore
        best_reward, _ = self.QL.find_max_reward()

        self.val += self.QL.lr * (reward + self.QL.gamma * best_reward - self.val)

    def update_after_death(self):
        self.val -= 3000

    def update_wall_colision(self):
        self.val -= 1000

    def update_game_won(self):
        self.val += 100000 / self.QL.game.pl.mov_num

    def get_val_at_t(self, mov):
        return self.val


def save_offline(obj, intermediate):
    if intermediate:
        if not os.path.isdir('qtables'):
            os.makedirs('qtables')
        filename = os.path.join('qtables', 'offline_learn_{}.txt'.format(int(time.time())))
    else:
        filename = 'offline_learn.txt'
    with open(filename, 'w') as f:
        f.write(str(obj.player_vel) + '\n')
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                value = obj.learn.q_value_table[i][j].get_val_at_t(0)
                line = str(i) + ',' + str(j) + ',' + str(value) + ',\n'
                f.write(line)
    # copyfile('offline_learn.txt', 'result/offline_learn.txt')


# To load to train online (use this values as ininial)
def load_online(obj):
    if os.path.isfile('offline_learn.txt'):
        obj.learn_offline_initial_conditions = QLearning(obj, online=False)
        with open('offline_learn.txt', 'r') as f:
            f.readline()
            for line in f:
                words = line.split(',')
                x = int(words[0])
                y = int(words[1])
                value = float(words[2])
                obj.learn_offline_initial_conditions.q_value_table[x][y].val = value
                obj.learn.q_value_table[x][y].init_val = value


def save_online(obj):
    filename = 'result/online_learn.txt'
    with open(filename, 'w') as f:
        f.write(str(obj.player_vel) + '\n')
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                f.write(str(i) + ',' + str(j) + ',')
                if len(obj.learn.q_value_table[i][j].t) > 0:
                    for k in range(len(obj.learn.q_value_table[i][j].t)):
                        t = obj.learn.q_value_table[i][j].t[k]
                        v = obj.learn.q_value_table[i][j].val[k]
                        f.write(str(t) + ',' + str(v) + ',')
                f.write('\n')
