import pyxel
import particle

HEIGHT = 24

class Lava(particle.Emitter):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 10)

        self.img = pyxel.Image(pyxel.width, pyxel.height)
        self.update_img = True

        # Jetpack specific variables and ranges
        self.particles_per_frame = 3
        self.particle_life_min = 10
        self.particle_life_max = 20
        self.particle_vx_min = 0
        self.particle_vx_max = 0
        self.particle_vy_min = -0.25
        self.particle_vy_max = -1.5
        self.particle_color_order = (10, 9, 8, 1)
        self.particle_size_order = (2, 2, 1, 1, 1)
        self.particle_x_pos_range = pyxel.width / 2
        self.particle_y_pos_range = 0

    def update(self):
        super().update()

        if self.total_frames % 20 == 0:
            self.emit()

        self.update_img = True

    def draw(self, scroll_x):
        # Draw wave
        if self.update_img:
            self.img.cls(0)
            x_dir = pyxel.cos(self.total_frames % 360) * 32
            for x in range(pyxel.width):
                sine_wave = pyxel.sin((x + x_dir + scroll_x) * 8)
                lava_y = pyxel.height - HEIGHT + int(sine_wave * pyxel.rndf(1, 3))
                self.img.line(x, pyxel.height, x, lava_y, pyxel.COLOR_RED)
            self.update_img = False
        pyxel.blt(0, 0, self.img, 0, 0, pyxel.width, pyxel.height, 0)

        # Draw particles
        super().draw()