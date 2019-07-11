from game import Game
import time

start = time.time()

game = Game(level=1, watch=True, watch_periodic=False, replay=True)
# watch overrides watch_periodic

# General parameters
game.player_max_moves = 100
game.player_max_max_moves = 1000
game.player_vel = 5
game.player_moves_step = 5
game.player_moves_interval = 10
game.eps_decrease_interval = 100
game.iteration_print_interval = 100
game.max_iterations = 10000

# Q-Learning parameters
game.learn.eps = 0.8
game.learn.lr = 0.3
game.learn.gamma = 0.9

# Watcher parameters
game.watcher_clock_flag = True
game.watch_period = 1000
game.watch_duration = 1

# Colision On/Off
game.colision = False

game.start()

finish = time.time()
print('Execution time ', time.strftime('%H:%M:%S', time.gmtime(finish-start)))
