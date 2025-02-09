import pyxel

SIZE = 8
HALF_SIZE = SIZE // 2

class Sprite:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.flip_x = False
        self.flip_y = False
        self.visible = True

    def draw(self):
        if not self.visible:
            return
        w = -SIZE if self.flip_x else SIZE
        h = -SIZE if self.flip_y else SIZE
        pyxel.blt(self.x, self.y, self.img, 0, 0, w, h, pyxel.COLOR_BLACK)