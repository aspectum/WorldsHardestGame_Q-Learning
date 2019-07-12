# TO-DO
# - Change data structure for q-table in order to be able to save it (pickle, dump)
# - Improve variable names for clarity
# - Remove unused variables
# - Of course, improve the q-learning algorithm and parameters as well
########################################################################

import random
from collections import defaultdict
import sys

dirs = ["right", "left", "up", "down", "stay"]


class QLearning:
    def __init__(self, game):
        self.pl = game.pl
        self.game = game

        self.eps = 0.2
        self.lr = 0.4
        self.gamma = 0.9

        self.q_value_table = self.mult_dim_dict(2, QValues, self)

    def mult_dim_dict(self, dim, dict_type, params):
        if dim == 1:
            return defaultdict(lambda: dict_type(params))
        else:
            return defaultdict(lambda: self.mult_dim_dict(dim - 1, dict_type, params))

    def dist2(self, obj1, obj2):
        return (obj1.tl.x - obj2.tl.x)**2 + (obj1.tl.y - obj2.tl.y)**2

    def find_move(self):
        r = random.random()

        if r < self.eps:
            self.move_randomly()
        else:
            self.move_optimally()

        x, y = self.game.pl.rec.tl.x, self.game.pl.rec.tl.y
        self.q_value_table[x][y].update_value()

    def move_randomly(self):
        i = random.randint(0, len(dirs) - 1)
        self.game.pl.move(dirs[i])

    def move_optimally(self):
        x, y = self.game.pl.rec.tl.x, self.game.pl.rec.tl.y

        self.game.pl.move(self.q_value_table[x][y].find_best_move())


class QValues:
    def __init__(self, QLearning):

        self.QL = QLearning
        self.table = self.QL.q_value_table
        self.pl = self.QL.game.pl
        self.val = []
        self.t = []  # time
        self.init_val = 0

    def update_value(self):

        if self.pl.mov_num not in self.t:
            self.t.append(self.pl.mov_num)
            self.val.append(self.init_val)

        # dist_finish = self.QL.dist2(self.QL.game.map.finish, self.pl.rec)

        reward = -1  # 10000000/(dist_finish + 1)

        best_reward, _ = self.find_max_reward()

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

    def find_max_reward(self):
        li = []

        for d in dirs:
            x, y = self.pl.move_simulation(d)
            li.append(self.table[x][y].get_val_at_t(self.pl.mov_num + 1))
        #     print()
        #     print(d)
        #     print(self.table[x][y].get_val_at_t(self.pl.mov_num + 1))

        # print(self.QL.game.pl.rec.getPos())
        # sys.exit()

        maxi = max(li)

        return maxi, li

    def find_best_move(self):
        maxi, li = self.find_max_reward()

        maxes = [i for i, x in enumerate(li) if x == maxi]

        if len(maxes) > 1:
            i = random.randint(0, len(maxes) - 1)
            best_move = dirs[i]
        else:
            best_move = dirs[li.index(maxi)]
    
        return best_move
