import pyxel
from laser import Laser

SHOT_DELAY = 12
MUZZLE_FLASH_FRAMES = 3

class LaserGun:
    def __init__(self):
        self.shot_delay = 0
        self.muzzle_flash_frames = 0

    def reset(self):
        self.shot_delay = 0
        self.muzzle_flash_frames = 0

    def update(self):
        self.shot_delay = max(0, self.shot_delay - 1)
        self.muzzle_flash_frames = max(0, self.muzzle_flash_frames - 1)

    def shoot(self, gameplay, x, y, x_dir):
        if self.shot_delay > 0:
            return
        self.shot_delay = SHOT_DELAY
        self.muzzle_flash_frames = MUZZLE_FLASH_FRAMES
        Laser(gameplay, x, y, x_dir)

    def draw(self, x, y):
        if self.muzzle_flash_frames <= 0:
            return
        pyxel.circ(x, y, self.muzzle_flash_frames, pyxel.COLOR_WHITE)