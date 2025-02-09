import pyxel
import utils
from audio import play_sound

SPEED = 4
LIFE = 30
START_LENGTH = 7
END_LENGTH = 30

COLORS = [8, 9, 10, 11, 3, 2, 5, 12, 14]
MAX_TRAILS = 4

class Laser:
    def __init__(self, gameplay, x, y, x_dir):
        self.gameplay = gameplay
        self.total_frames = 0
        self.x = x
        self.y = y
        self.dir_x = x_dir
        self.vel_x = SPEED * x_dir
        self.life = LIFE
        self.length = START_LENGTH
        self.trails = 0
        gameplay.lasers.append(self)
        self.remove = False
        play_sound("LASER")

    def hit_rect_check(self, x, y, w, h):
        laser_x = self.x - (self.length) if self.dir_x < 0 else self.x
        return utils.rect_collision_check_wrap_x(
            laser_x, self.y, self.length, 1,
            x, y, w, h, self.gameplay.ground.width)

    def update(self):
        self.total_frames += 1
        self.life -= 1
        self.x += self.vel_x
        self.length = START_LENGTH + (END_LENGTH - START_LENGTH) * (1-(self.life / LIFE))
        self.trails = 1 + MAX_TRAILS - (pyxel.floor((self.life / LIFE) * MAX_TRAILS))

        if self.dir_x < 0:
            if self.x <= self.gameplay.scroll_x:
                self.remove = True
        else:
            if self.x >= self.gameplay.scroll_x + pyxel.width:
                self.remove = True

    def draw(self):
        col = COLORS[(pyxel.floor(self.total_frames * 0.2)) % len(COLORS)]
        pyxel.line(self.x, self.y, self.x + (self.length * self.dir_x), self.y, col)
        for i in range(self.trails):
            pyxel.pset((self.x + (i * 3) * -self.dir_x), self.y, col)

        # laser_x = self.x - (self.length) if self.dir_x < 0 else self.x
        #pyxel.text(self.x, self.y - 8, f"x: {pyxel.floor(self.x)}", 7)