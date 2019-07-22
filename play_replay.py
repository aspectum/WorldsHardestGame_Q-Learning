from game import Game
from watch import Watcher
import sys
import pickle
import os

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = "replay.p"

if not os.path.isfile(filename):
    print("ERROR: the file '", filename, "' doesn't exist")
    sys.exit()

with open(filename, "rb") as f:
    final_state = pickle.load(f)

w = Watcher(fps=int(sys.argv[1]), clock_flag=True)

game = Game(level=final_state[0], watcher=w)
game.watcher_clock_flag = True

w.replay(final_state)
