from rectangle import rect


class EnemyCircle:

    def __init__(self, game, image, speed, hor, border1, border2):

        self.hor = hor  # bool for moving horizontally or not (vertically)
        self.border1 = border1
        self.border2 = border2

        self.game = game
        self.speed = speed

        self.rec = rect((0, 0), (14, 14))

    def move(self):
        if self.rec.collidesWith(self.game.pl.rec):
            self.game.gameContinues = False
            self.game.learn.q_value_table[self.game.pl.x][self.game.pl.y].update_after_death()

        if self.hor:
            self.rec = self.rec.move((self.speed, 0))
        else:
            self.rec = self.rec.move((0, self.speed))

        if self.hor and self.rec.tl[0] >= self.border2 or self.rec.br[0] < self.border1:
            self.speed *= -1
        elif (not self.hor) and self.rec.br[1] > self.border2 or self.rec.tl[1] <= self.border1:
            self.speed *= -1
