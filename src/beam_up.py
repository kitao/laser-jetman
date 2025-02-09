import pyxel
from utils import lerp

MAX_DITHER = 0.5

STATE_BEAM_GO_DOWN = 0
STATE_HUMAN_GO_UP = 1
STATE_BEAM_GO_UP = 2
STATE_MAX = 3

TYPE_PLAYER = 0
TYPE_ENEMY = 1

TOTAL_FRAMES = (60, 300)
COLOURS = ((12, 5, 1), (10, 8, 2))
MAX_WIDTH = (12, 6)

class BeamUp:
    def __init__(self, human, type, y):
        self.type = type
        self.state = STATE_BEAM_GO_DOWN
        self.frames_per_state = TOTAL_FRAMES[type] // STATE_MAX
        self.human = human
        self.y = y
        self.bottom = human.y + 7
        self.width = 0
        self.height = 0
        self.max_height = self.bottom - self.y
        self.frames = 0
        self.dither = 0

    def is_finished(self):
        return self.frames == self.frames_per_state and self.state == STATE_BEAM_GO_UP

    def update(self):
        if self.is_finished():
            return

        self.frames = min(self.frames_per_state, self.frames + 1)
        progress = self.frames / self.frames_per_state

        if self.state == STATE_BEAM_GO_DOWN:
            self.width = lerp(0, MAX_WIDTH[self.type], progress)
            self.height = lerp(0, self.max_height, progress)
            self.dither = lerp(0, MAX_DITHER, progress)
        elif self.state == STATE_HUMAN_GO_UP:
            top = self.y-8 if self.type == TYPE_PLAYER else self.y
            self.human.y = lerp(self.bottom - 7, top, progress)
        elif self.state == STATE_BEAM_GO_UP:
            self.width = lerp(MAX_WIDTH[self.type], 0, progress)
            self.height = lerp(self.max_height, 0, progress)
            self.dither = lerp(MAX_DITHER, 0, progress)

        if self.frames == self.frames_per_state:
            if self.state != STATE_BEAM_GO_UP:
                self.state += 1
                self.frames = 0
    
    def draw(self, draw_x):
        pyxel.dither(self.dither)

        x = (draw_x + 4) - (self.width // 2)
        h = (self.height // 3)
        y = self.y
        for i in range(3):
            pyxel.rect(x, y, self.width, h, COLOURS[self.type][i])
            y += h
            
        x = (draw_x + 4)
        pyxel.rect(x - 1, self.y, 2, self.height, 6)

        pyxel.dither(1)