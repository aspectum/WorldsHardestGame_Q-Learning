from game import Game
import time

start = time.time()

game = Game(level=5, watch=False, watch_periodic=True, replay=True)
# watch overrides watch_periodic

# General parameters
game.player_max_moves = 100
game.player_max_max_moves = 300
game.player_vel = 10
game.player_moves_step = 5
game.player_moves_interval = 10
game.eps_decrease_interval = 25
game.iteration_print_interval = 50
game.max_iterations = 500

# Q-Learning parameters
game.learn_offline.eps = 0.9
game.learn_offline.lr = 0.3
game.learn_offline.gamma = 0.8

# game.learn.eps = 0.2
# game.learn.lr = 0.4
# game.learn.gamma = 0.8

# Watcher parameters
game.watcher_clock_flag = True
game.watch_period = 100
game.watch_duration = 1

# Colision On/Off
game.colision = False
game.checkpoints = False
game.constant_eps = False

game.replay_file_only = True

game.start()

finish = time.time()
print('Execution time ', time.strftime('%H:%M:%S', time.gmtime(finish-start)))
