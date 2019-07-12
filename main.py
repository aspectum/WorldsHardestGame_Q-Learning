from game import Game
import time

start = time.time()

game = Game(level=5, watch=False, watch_periodic=False, replay=True)
# watch overrides watch_periodic

# General parameters
game.player_max_moves = 200
game.player_max_max_moves = 3000
game.player_vel = 1
game.player_moves_step = 10
game.player_moves_interval = 20
game.eps_decrease_interval = 500
game.iteration_print_interval = 100
game.max_iterations = 10000

# Q-Learning parameters
game.learn_offline.eps = 0.81
game.learn_offline.lr = 0.3
game.learn_offline.gamma = 0.8

# game.learn.eps = 0.2
# game.learn.lr = 0.4
# game.learn.gamma = 0.8

# Watcher parameters
game.watcher_clock_flag = False
game.watch_period = 1000
game.watch_duration = 1

# Colision On/Off
game.colision = False
game.checkpoints = False
game.constant_eps = False

game.replay_file_only = True

game.start()

finish = time.time()
print('Execution time ', time.strftime('%H:%M:%S', time.gmtime(finish-start)))
