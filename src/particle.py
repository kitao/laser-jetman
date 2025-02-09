import pyxel

PARTICLES_SHAPE_POINT = 0
PARTICLES_SHAPE_CIRCLE = 1

class Particle:
    def __init__(self, x, y, vx, vy, life, color_order=(7,), size_order=(1,), shape=PARTICLES_SHAPE_CIRCLE):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.life_max = life
        self.color_order = color_order
        self.color = color_order[0]
        self.size_order = size_order
        self.size = size_order[0]
        self.shape = shape

    def update(self):
        self.life -= 1
        if self.life <= 0:
            return
        
        self.x += self.vx
        self.y += self.vy
        self.size = self.size_order[pyxel.floor((self.life / self.life_max) * len(self.size_order))]
        self.color = self.color_order[pyxel.floor((self.life / self.life_max) * len(self.color_order))]

    def draw(self):
        if self.life > 0:
            if self.shape == PARTICLES_SHAPE_POINT:
                pyxel.pset(self.x, self.y, self.color)
            elif self.shape == PARTICLES_SHAPE_CIRCLE:
                pyxel.circ(self.x, self.y, self.size, self.color)
                

class Emitter:
    def __init__(self, x, y, max_particles, particle_life):
        self.total_frames = 0
        self.x = x
        self.y = y
        self.max_particles = max_particles
        self.particles = []

        # Particle variables and ranges
        self.particles_shape = PARTICLES_SHAPE_CIRCLE
        self.particles_per_frame = 1
        self.particle_life_min = particle_life
        self.particle_life_max = particle_life
        self.particle_vx_min = -1
        self.particle_vx_max = 1
        self.particle_vy_min = -1
        self.particle_vy_max = 1
        self.particle_color_order = (7,)
        self.particle_size_order = (1,)
        self.particle_x_pos_range = 1
        self.particle_y_pos_range = 1

        # Used for single emit particles, i.e. explosion.
        self.single_use_particles_used = 0
        self.single_use_max_particles = -1
        self.finished = False

    def emit(self):
        for _ in range(self.particles_per_frame):
            if self.single_use_particles_used == self.single_use_max_particles:
                return
            
            if len(self.particles) >= self.max_particles:
                return

            x = self.x + pyxel.rndf(-self.particle_x_pos_range, self.particle_x_pos_range)
            y = self.y + pyxel.rndf(-self.particle_y_pos_range, self.particle_y_pos_range)
            particle = \
                Particle(x, y, 
                        pyxel.rndf(self.particle_vx_min, 
                                    self.particle_vx_max), 
                        pyxel.rndf(self.particle_vy_min, 
                                    self.particle_vy_max), 
                        pyxel.rndi(self.particle_life_min, 
                                    self.particle_life_max), 
                        list(reversed(self.particle_color_order)),
                        list(reversed(self.particle_size_order)),
                        shape=self.particles_shape)
            self.particles.append(particle)

            if self.single_use_max_particles > 0:
                self.single_use_particles_used += 1

    def update(self):
        self.total_frames += 1
        for particle in self.particles:
            particle.update()
        self.particles[:] = [p for p in self.particles if p.life > 0]
        if len(self.particles) == 0:
            if self.single_use_particles_used == self.single_use_max_particles:
                self.finished = True

    def draw(self):
        for particle in self.particles:
            particle.draw()

        #pyxel.text(0, 0, f"Particles: {len(self.particles)}", pyxel.COLOR_WHITE)