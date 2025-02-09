import pyxel
import enemy
from gfx_data import ANIMS
import constants
from utils import get_angle_wrap_x
import enemy_bullet

MIN_NEXT_MOVE_FRAMES = 15
ADD_NEXT_MOVE_FRAMES = 45

SPEED = 0.35

class EnMutant(enemy.Enemy):
    def __init__(self, gameplay, x, y):
        super().__init__(gameplay, x, y, ANIMS["mutant"][0], 
                         constants.ENEMY_TYPE_MUTANT)
        
        # Reduced to 0 as spawned from landers.
        self.invincible_frames = 0

        self.target_x = 0
        self.target_y = 0
        self.next_move_frames = self._get_next_move_frames()

    def _get_next_move_frames(self):
        return MIN_NEXT_MOVE_FRAMES + pyxel.rndi(0, ADD_NEXT_MOVE_FRAMES)

    def _set_new_target(self):
        a = get_angle_wrap_x(self.x + 4, self.y + 4,
                             self.gameplay.player.x + 4, 
                             self.gameplay.player.y + 4,
                             self.gameplay.ground.width)
        self.vel_x = pyxel.cos(a) * SPEED
        self.vel_y = pyxel.sin(a) * SPEED
        self.next_move_frames = self._get_next_move_frames()

    def update(self):
        self.total_frames += 1

        if self.next_move_frames == 0:
            self._set_new_target()
        self.next_move_frames = max(0, self.next_move_frames - 1)
        self._move()
        self._got_hit_check()

        if self.total_frames % 360 == 0:
            self._shoot_at_player(enemy_bullet.SPEED_SLOW)