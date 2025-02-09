import pyxel
import particle
import sprite
from audio import play_sound

class Jetpack(particle.Emitter):
    def __init__(self, jetman):
        super().__init__(jetman.x, jetman.y + 4, 50, 20)
        self.jetman = jetman
        self.firing = False

        # Jetpack specific variables and ranges
        self.particles_per_frame = 3
        self.particle_life_min = 5
        self.particle_life_max = 12
        self.particle_vx_min = -0.25
        self.particle_vx_max = 0.25
        self.particle_vy_min = 0.25
        self.particle_vy_max = 1.5
        self.particle_color_order = (10, 9, 8, 2, 1)
        self.particle_size_order = (1, 2)

    def reset(self):
        self.particles = []

    def _update_position(self):
        if self.jetman.flip_x:
            self.x = self.jetman.x + sprite.SIZE - 2
        else:
            self.x = self.jetman.x + 1
        self.y = self.jetman.y + 4

    def stop(self):
        self.firing = False

    def fire(self):
        self.emit()
        self.firing = True
        play_sound("JETPACK_FIRE")

    def update(self):
        self._update_position()
        super().update()

    def draw(self):
        super().draw()