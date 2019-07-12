from game import Game
from watch import watcher
import sys
import pickle
import os

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = 'replay.p'

if not os.path.isfile(filename):
    print("ERROR: the file '", filename, "' doesn't exist")
    sys.exit()

with open(filename, 'rb') as f:
    final_state = pickle.load(f)

game = Game(level=final_state[0], watch=True, watch_periodic=False, replay=False)
game.watcher_clock_flag = True

w = watcher(game, clock_flag=game.watcher_clock_flag, fps=int(sys.argv[1]))
w.replay(final_state)
