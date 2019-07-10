from game import Game
import time

start = time.time()

game = Game(level=4, watch=False, watch_periodic=False, replay=True)
# watch overrides watch_periodic

# General parameters
game.player_max_moves = 100
game.player_max_max_moves = 300
game.player_vel = 10
game.player_moves_step = 5
game.player_moves_interval = 5
game.eps_decrease_interval = 40
game.iteration_print_interval = 50
game.max_iterations = 5000

# Q-Learning parameters
game.learn.eps = 0.8
game.learn.lr = 0.4
game.learn.gamma = 0.9

# Watcher parameters
game.watcher_clock_flag = True
game.watch_period = 50
game.watch_duration = 3

game.start()

finish = time.time()
print('Execution time ', time.strftime('%H:%M:%S', time.gmtime(finish-start)))
