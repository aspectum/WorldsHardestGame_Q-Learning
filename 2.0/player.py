# Why self.opposite_dir?
from rectangle import rect


class Player:

    def __init__(self, game, speed):
        # to calculate number of moves
        self.mov_num = 0

        self.speed = speed
        self.game = game

        self.rec = rect((0, 0), (22, 22))

        self.move_dir = {"right": (self.speed, 0), "left": (-self.speed, 0),
                         "up": (0, -self.speed), "down": (0, self.speed), "stay": (0, 0)}

        # for returning
        self.opposite_dir = {"right": "left", "left": "right", "up": "down", "down": "up"}

    def move(self, d):

        # reaching max move limit
        if self.game.player_max_moves == self.mov_num:
            self.game.gameContinues = False
            return

        # move player and update coordinates
        self.rec = self.rec.move(self.move_dir[d])
        self.mov_num += 1

        # reaching finish
        if self.rec.collidesWith(self.game.map.finish):
            self.game.gameContinues = False
            self.game.isWin = True

        # intersection logic with borders
        for line in self.game.map.lines:
            if self.rec.collidesWith(line):
                self.rec = self.rec.move(self.move_dir[self.opposite_dir[d]])
                # This was the bottleneck previously
                # Maybe optimize
                # Add logic to punish if colliding with wall (in q-table)

    def move_simulation(self, d):
        return (self.rec.tl[0] + self.move_dir[d][0], self.rec.tl[1] + self.move_dir[d][1])

    # What is your purpose?
    def mov_back_simulation(self, d):
        return self.move_simulation(self.opposite_dir(d))
