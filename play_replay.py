from game import Game
from watch import watcher
import sys
import pickle
import os

game = Game(level=0, watch=True, watch_periodic=False, replay=False)
game.watcher_clock_flag = True

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'replay.p'

if not os.path.isfile(filename):
    print("ERROR: the file '", filename, "' doesn't exist")
    sys.exit()


with open(filename, 'rb') as f:
    final_state = pickle.load(f)
    w = watcher(game, game.watcher_clock_flag)
    w.replay(final_state)
