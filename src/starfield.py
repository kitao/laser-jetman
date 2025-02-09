import pyxel

STAR_FRAMES_MIN = 60
STAR_FRAMES_MAX = 180

class Star:
    def __init__(self, starfield):
        self.starfield = starfield
        self.x = 0
        self.y = 0
        self.col = pyxel.rndi(0, pyxel.NUM_COLORS-1)
        self.life = 0
        self._respawn()

    def _respawn(self):
        self.x = pyxel.rndi(0, self.starfield.width-1)
        self.y = pyxel.rndi(0, self.starfield.height-1)
        self.life = pyxel.rndi(STAR_FRAMES_MIN, STAR_FRAMES_MAX)

    def update(self):
        self.col = pyxel.rndi(0, pyxel.NUM_COLORS-1)
        self.life -= 1
        if self.life <= 0:
            self._respawn()


MAX_STARS = 25

class Starfield:
    def __init__(self):
        self.width = pyxel.width
        self.height = pyxel.height
        self.img = pyxel.Image(self.width, self.height)
        self.stars = []
        for _ in range(MAX_STARS):
            self.stars.append(Star(self))

    def update(self):
        for s in self.stars:
            s.update()

    def draw(self, scroll_x):
        self.img.cls(0)
        for s in self.stars:
            self.img.pset(s.x, s.y, s.col)

        w = self.width - ((scroll_x // 4) % pyxel.width)
        pyxel.blt(0, 0, 
                  self.img, 
                  (scroll_x // 4) % pyxel.width, 0, 
                  w, 
                  self.height)
        
        pyxel.blt(w, 0, 
                  self.img, 
                  0, 0, 
                  self.width, 
                  self.height)
