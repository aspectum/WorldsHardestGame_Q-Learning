from game import Game
from watch import watcher
import pickle

game = Game(level=0, watch=True, watch_periodic=False, replay=False)
game.watcher_clock_flag = True

with open('replay.p', 'rb') as f:
    final_state = pickle.load(f)
w = watcher(game, game.watcher_clock_flag)
w.replay(final_state)
