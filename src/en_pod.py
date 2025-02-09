import pyxel
import enemy
from gfx_data import ANIMS
import constants
import enemy_bullet
from en_swarmer import EnSwarmer

class EnPod(enemy.Enemy):
    def __init__(self, gameplay, x, y):
        super().__init__(gameplay, x, y, ANIMS["pod"][0], 
                         constants.ENEMY_TYPE_POD)

        self.angle_x = pyxel.rndi(0, 360)
        self.angle_y = pyxel.rndi(0, 360)

    def destroy(self):
        super().destroy()
        num = pyxel.rndi(3, 5)
        for _ in range(num):
            x = self.x + pyxel.rndi(-8, 16)
            y = self.y + pyxel.rndi(-8, 16)
            self.gameplay.enemies.append(EnSwarmer(self.gameplay, x, y))

    def update(self):
        self.total_frames += 1

        self.angle_x = (self.angle_x + 0.025) % 360
        self.vel_x = pyxel.sin(self.angle_x) * 0.5

        self.angle_y = (self.angle_y + 1) % 360
        self.vel_y = pyxel.cos(self.angle_y) * 0.1
        self._move()
        self._update_invincible_frames()
        self._got_hit_check()

        if self.total_frames % 320 == 0:
            self._shoot_at_player(enemy_bullet.SPEED_SLOW)