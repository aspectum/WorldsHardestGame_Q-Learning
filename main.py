from game import Game
import time

localtime = time.asctime( time.localtime(time.time()) )
print("Local current time :", localtime)
w, h = 1000, 1000

game = Game(w, h)
game.start()

localtime = time.asctime( time.localtime(time.time()) )
print("Local current time :", localtime)