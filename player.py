# Why self.opposite_dir?
from rectangle import Rect


class Player:
    def __init__(self, game, speed):
        # to calculate number of moves
        self.mov_num = 0

        self.speed = speed
        self.game = game

        self.rec = Rect((0, 0), (22, 22))

        self.move_dir = {
            "right": (self.speed, 0),
            "left": (-self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed),
            "stay": (0, 0),
        }

        # for returning
        self.opposite_dir = {
            "right": "left",
            "left": "right",
            "up": "down",
            "down": "up",
        }

    def move(self, d):

        # reaching max move limit
        if self.game.player_max_moves == self.mov_num:
            self.game.game_continues = False
            return

        # move player and update coordinates
        self.rec.move(self.move_dir[d])
        self.mov_num += 1

        # reaching finish
        if self.rec.collides_with(self.game.map.finish):
            self.game.game_continues = False
            self.game.is_win = True
            self.game.learn.q_value_table[self.rec.tl.x][
                self.rec.tl.y
            ].update_game_won()

        # collision logic with borders
        for line in self.game.map.lines:
            if self.rec.collides_with(line):
                # self.game.learn.q_value_table[self.rec.tl.x][self.rec.tl.y].update_wall_colision()
                self.rec.move(self.move_dir[self.opposite_dir[d]])
                self.game.learn.q_value_table[self.rec.tl.x][
                    self.rec.tl.y
                ].update_wall_colision()

        # collision with enemies
        for e in self.game.enemies:
            if self.rec.collides_with(e.rec) and self.game.colision:
                self.game.game_continues = False
                self.game.learn.q_value_table[self.rec.tl.x][
                    self.rec.tl.y
                ].update_after_death()

    def move_simulation(self, d):
        return (
            self.rec.tl.x + self.move_dir[d][0],
            self.rec.tl.y + self.move_dir[d][1],
        )
