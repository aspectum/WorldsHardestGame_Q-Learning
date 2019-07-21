from game import Game
from watch import Watcher

import time
import os

if not os.path.isdir('resultado'):
    os.makedirs('resultado')

start = time.time()

col = True

watcher = None
watcher = Watcher(show='nothing', period=5, duration=2, replay=col, fps=30, clock_flag=True)

game = Game(level=0, watcher=watcher, colision=col)
# watch overrides watch_periodic

# General parameters
game.player_max_moves = 200
game.player_max_max_moves = 600
game.player_vel = 10
game.player_moves_step = 5
game.player_moves_interval = 5
game.eps_decrease_interval = 200
game.iteration_print_interval = 50
game.max_iterations = 700

# Q-Learning parameters
if col:
    game.learn.eps = 0.15
    game.learn.lr = 0.3
    game.learn.gamma = 0.9
else:
    game.learn.eps = 0.9
    game.learn.lr = 0.6
    game.learn.gamma = 0.99

# Watcher parameters
# game.watcher_clock_flag = True
# game.watch_period = 300
# game.watch_duration = 1

# Colision On/Off
# game.colision = True
game.checkpoints = False
game.constant_eps = False

# game.replay_file_only = not col

game.start()

finish = time.time()
print('Execution time ', time.strftime('%H:%M:%S', time.gmtime(finish - start)))

if game.colision:
    filename = "resultado/params_online.txt"
else:
    filename = "resultado/params_offline.txt"

with open(filename, 'w') as f:
    f.write('game.player_max_moves = ' + str(game.player_max_moves) + '\n')
    f.write('game.player_max_max_moves = ' + str(game.player_max_max_moves) + '\n')
    f.write('game.player_vel = ' + str(game.player_vel) + '\n')
    f.write('game.player_moves_step = ' + str(game.player_moves_step) + '\n')
    f.write('game.player_moves_interval = ' + str(game.player_moves_interval) + '\n')
    f.write('game.eps_decrease_interval = ' + str(game.eps_decrease_interval) + '\n')
    f.write('game.iteration_print_interval = ' + str(game.iteration_print_interval) + '\n')
    f.write('game.max_iterations = ' + str(game.max_iterations) + '\n')
    f.write('game.learn.eps = ' + str(game.learn.eps) + '\n')
    f.write('game.learn.lr = ' + str(game.learn.lr) + '\n')
    f.write('game.learn.gamma = ' + str(game.learn.gamma) + '\n')
    # f.write('game.watcher_clock_flag = ' + str(game.watcher_clock_flag) + '\n')
    # f.write('game.watch_period = ' + str(game.watch_period) + '\n')
    # f.write('game.watch_duration = ' + str(game.watch_duration) + '\n')
    f.write('game.colision = ' + str(game.colision) + '\n')
    f.write('game.checkpoints = ' + str(game.checkpoints) + '\n')
    f.write('game.constant_eps = ' + str(game.constant_eps) + '\n')
    f.write('game.epochs = ' + str(game.epochs) + '\n')
    f.write('game.pl.mov_num = ' + str(game.pl.mov_num) + '\n')
    f.write('game.qsz = ' + str(game.qsz) + '\n')
