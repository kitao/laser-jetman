import pyxel
import enemy
from gfx_data import ANIMS
# import enemy_bullet
import constants

class EnRedeye(enemy.Enemy):
    def __init__(self, gameplay, x, y):
        super().__init__(gameplay, x, y, ANIMS["redeye"][0], 
                         constants.ENEMY_TYPE_REDEYE)

        self.angle_x = pyxel.rndi(0, 360)
        self.angle_y = pyxel.rndi(0, 360)

    def update(self):
        self.total_frames += 1
        self.angle_x = (self.angle_x + 1) % 360
        self.vel_x = pyxel.sin(self.angle_x)# * 1
        self.angle_y = (self.angle_y + 6) % 360
        self.vel_y = pyxel.cos(self.angle_y) * 1
        self._move()
        self.flip_x = True if self.vel_x < 0 else False
        self._update_invincible_frames()
        self._got_hit_check()