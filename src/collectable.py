import pyxel
import sprite

TYPE_SHIELD = 0

class Collectable(sprite.Sprite):
    def __init__(self, gameplay, type, x, y, img):
        super().__init__(x, y, img)

        self.gameplay = gameplay
        self.type = type
        self.remove = False

        self.angle = 0

    def collected(self):
        self.remove = True
        self.visible = False

    def update(self):
        self.angle = (self.angle + 10) % 360
        self.y += pyxel.cos(self.angle)
    
    def draw(self, scroll_x, ground_w):
        # Fix to ensure sprites within -8 pixels left of scroll_x get partially drawn.
        draw_x = self.x - (scroll_x % ground_w)
        if draw_x <= -sprite.SIZE or draw_x > 0:
            draw_x = (self.x - scroll_x) % ground_w

        if draw_x <= -sprite.SIZE or draw_x >= pyxel.width:
          return

        pyxel.blt(draw_x, self.y, self.img, 0, 0, sprite.SIZE, sprite.SIZE, pyxel.COLOR_BLACK)
