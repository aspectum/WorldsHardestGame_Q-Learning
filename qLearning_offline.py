import random
from collections import defaultdict

dirs = ["right", "left", "up", "down", "stay"]


class QLearning_offline:
    def __init__(self, game):
        self.pl = game.pl
        self.game = game

        self.eps = 0.8
        self.lr = 0.4
        self.gamma = 0.9

        self.q_value_table = self.mult_dim_dict(2, QValues_offline, self)

        self.active_checkpoint = 0

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


class QValues_offline:
    def __init__(self, QLearning):

        self.QL = QLearning
        self.table = self.QL.q_value_table
        self.pl = self.QL.game.pl

        self.val = 0

    def update_value(self):

        dist = self.QL.dist2(self.QL.game.map.checkpoints[self.QL.active_checkpoint], self.pl.rec)

        reward = 10000 / (dist + 1)
        best_reward, _ = self.find_max_reward()

        self.val += self.QL.lr * (reward + self.QL.gamma * best_reward - self.val)

    def update_after_death(self):
        self.val -= 3000

    def update_wall_colision(self):
        self.val -= 1000

    def update_game_won(self):
        # self.val += 100000 / self.QL.game.pl.mov_num
        self.val += 10000

    def update_checkpoint(self):
        self.val = 250
        if self.QL.active_checkpoint + 1 < len(self.QL.game.map.checkpoints):
            self.QL.eps = 0.3
            self.QL.active_checkpoint += 1

    def get_val_at_t(self, mov):
        return self.val

    def find_max_reward(self):
        li = []

        for d in dirs:
            x, y = self.pl.move_simulation(d)
            li.append(self.table[x][y].get_val_at_t(self.pl.mov_num + 1))

        maxi = max(li)

        return maxi, li

    def find_best_move(self):
        maxi, li = self.find_max_reward()

        return dirs[li.index(maxi)]
