import pyxel
from utils import lerp

class Ground:
    def __init__(self, width=1024, max_height=64):
        self.width = width
        self.max_height = max_height
        self.wavelength = 0.025 # Lower values make the hills wider
        self.amplitude = 0.01 # Lower values make the hills taller and valleys deeper.
        #self.frequency = 0.05
        self.surface = self.generate_surface()

    def generate_surface(self):
        surface = []
        for x in range(self.width):
            noise_value = pyxel.noise(x * self.wavelength, x * self.amplitude)

            # Transform the range to [0.0, 1.0], from [-1.0, 1.0]
            noise_value += 1.0
            noise_value /= 2.0

            height = int(self.max_height * noise_value)
            surface.append(height)

        # Smooth out the last 20 values back to the beginning height.
        for i in range(1, 21):
            surface[-i] = lerp(surface[0], surface[-i], i / 20)

        return surface

    def get_height_at(self, x):
        return self.surface[x % self.width]
    
    def draw(self, scroll_x):
        for x in range(pyxel.width):
            ground_height = self.get_height_at(x + int(scroll_x) % self.width)
            pyxel.line(x, pyxel.height, x, pyxel.height - ground_height, pyxel.COLOR_NAVY)

        # Fade at bottom
        # pyxel.dither(0.25)
        # pyxel.rect(0, pyxel.height - 16, pyxel.width, 4, 0)
        # pyxel.dither(0.5)
        # pyxel.rect(0, pyxel.height - 12, pyxel.width, 4, 0)
        #pyxel.dither(1) # Solid
        #pyxel.rect(0, pyxel.height - 8, pyxel.width, 8, 0)
