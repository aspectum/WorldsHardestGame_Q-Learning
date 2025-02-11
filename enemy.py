from rectangle import Rect


class EnemyCircle:
    def __init__(self, game, speed, hor, border1, border2):

        self.hor = hor  # bool for moving horizontally or not (vertically)
        self.border1 = border1
        self.border2 = border2

        self.game = game
        self.speed = speed

        self.rec = Rect((0, 0), (14, 14))

    def move(self):
        # Collision with player
        if self.rec.collides_with(self.game.player.rec) and self.game.colision:
            self.game.game_continues = False
            self.game.learn.q_value_table[self.game.player.rec.tl.x][
                self.game.player.rec.tl.y
            ].update_after_death()

        # Distiction between horizontal and vertical movement
        if self.hor:
            self.rec.move((self.speed, 0))
        else:
            self.rec.move((0, self.speed))

        # If passed limits (borders), change movement direction
        if self.hor and (self.rec.br.x > self.border2 or self.rec.tl.x < self.border1):
            self.speed *= -1
        elif not self.hor and (
            self.rec.br.y > self.border2 or self.rec.tl.y < self.border1
        ):
            self.speed *= -1
