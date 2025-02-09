import pyxel
import utils

SIZE = 2
RADIUS = SIZE / 2

MINE_SIZE = 4
MINE_RADIUS = MINE_SIZE // 2

MAX_LIFE = 120

SPEED_NONE = 0
SPEED_SLOW = 1
SPEED_MEDIUM = 2
SPEED_FAST = 3

def set_velocity_to_player(gameplay, bullet, speed):
    a = utils.get_angle_wrap_x(bullet.x + RADIUS, bullet.y + RADIUS,
                               gameplay.player.x + 4, gameplay.player.y + 4,
                               gameplay.ground.width)
    
    bullet.vel_x = pyxel.cos(a) * speed
    bullet.vel_y = pyxel.sin(a) * speed

class EnemyBullet:
    def __init__(self, gameplay, x, y, speed):
        self.gameplay = gameplay
        self.total_frames = 0
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.col = pyxel.COLOR_WHITE
        self.life = MAX_LIFE
        self.remove = False
        self.is_mine = True
        if speed != SPEED_NONE:
            set_velocity_to_player(gameplay, self, speed)
            self.is_mine = False
        self.gameplay.enemy_bullets.append(self)

    def _move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def update(self):
        self.total_frames += 1

        self.life = max(0, self.life - 1)
        if self.life == 0:
            self.remove = True
            return

        if not self.is_mine:
            self._move()

        if self.total_frames % 5 == 0:
            self.col = pyxel.COLOR_RED if self.col == pyxel.COLOR_WHITE else pyxel.COLOR_WHITE

    def draw(self, scroll_x, ground_w):
        # Fix to ensure sprites within -8 pixels left of scroll_x get partially drawn.
        draw_x = self.x - (scroll_x % ground_w)
        if draw_x <= -SIZE or draw_x > 0:
            draw_x = (self.x - scroll_x) % ground_w

        if draw_x <= -SIZE or draw_x >= pyxel.width:
          return

        if self.is_mine:
            pyxel.circ(draw_x + MINE_RADIUS, self.y + MINE_RADIUS, MINE_RADIUS, self.col)
        else:
            pyxel.circ(draw_x + RADIUS, self.y + RADIUS, RADIUS, self.col)