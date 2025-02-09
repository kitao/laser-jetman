import particle

class PlayerExplosion(particle.Emitter):
    def __init__(self, player):
        super().__init__(player.x + 4, player.y + 4, 
                         30, 30)

        # Particle variables and ranges
        self.particles_per_frame = 3
        self.particle_life_min = 20
        self.particle_life_max = 80
        self.particle_vx_min = -1
        self.particle_vx_max = 1
        self.particle_vy_min = -1
        self.particle_vy_max = 1
        self.particle_color_order = (7, 13, 12, 5, 1)
        self.particle_size_order = (3, 4, 3, 2, 1, 1, 1)
        self.particle_x_pos_range = 3
        self.particle_y_pos_range = 3

        # Used for single emit particles, i.e. explosion.
        self.single_use_max_particles = 30

    def update(self):
        super().update()
        self.emit()

    # def draw(self):
    #     super().draw()
