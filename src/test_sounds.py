import pyxel
from sound_data import SOUNDS
import sound_data

class App:
    def __init__(self):
        pyxel.init(128, 128, display_scale=3)
        pyxel.mouse(True)

        sound_data.add_all()

        self.num_sounds = len(SOUNDS)
        self.num = 0
        self.playing = False
        self.loop = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.num -= 1
            if self.num < 0:
                self.num = self.num_sounds - 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.num += 1
            if self.num == self.num_sounds:
                self.num = 0

        if pyxel.btnp(pyxel.KEY_L):
            self.loop = not self.loop

        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(0, self.num, loop=self.loop)

        if pyxel.btnp(pyxel.KEY_S):
            pyxel.stop()
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(8, 8, f"Sound: {self.num}", 7)
        pyxel.text(8, 16, f"Loop: {self.loop}", 7)

App()