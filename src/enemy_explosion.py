import particle

class EnemyExplosion(particle.Emitter):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30)

        # Particle variables and ranges
        self.particles_per_frame = 3
        self.particle_life_min = 10
        self.particle_life_max = 30
        self.particle_vx_min = -1
        self.particle_vx_max = 1
        self.particle_vy_min = -1
        self.particle_vy_max = 1
        self.particle_color_order = (7, 10, 9, 8, 2, 1)
        self.particle_size_order = (2, 3, 2, 1, 1)
        self.particle_x_pos_range = 2
        self.particle_y_pos_range = 2

        # Used for single emit particles, i.e. explosion.
        self.single_use_max_particles = 20

    def update(self):
        super().update()
        self.emit()

    # def draw(self):
    #     super().draw()
