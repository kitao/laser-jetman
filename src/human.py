import pyxel
import sprite
from gfx_data import ANIMS
from beam_up import BeamUp
import beam_up
from audio import play_sound

class Human(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, ANIMS["human"][0])

        self.total_frames = 0
        self.spawn_height = y
        self.frame = 0
        self.remove = False
        self.beam_up = None

    def remove_beam(self):
        self.beam_up = None

    def can_be_beamed_up(self):
        return self.beam_up == None

    def start_beam_up(self, type, top_y):
        self.beam_up = BeamUp(self, type, top_y)
        return self.beam_up

    def update(self):
        self.total_frames += 1

        if self.beam_up is not None:
            # enemy updates it's own beam.
            if self.beam_up.type == beam_up.TYPE_PLAYER:
                if pyxel.play_pos(0) is None:
                    play_sound("RESCUE_BEAM_UP")
                self.beam_up.update()
                self.remove = self.beam_up.is_finished()
        else:
            if self.total_frames % 15 == 0:
                self.frame = 1 if self.frame == 0 else 0
                self.img = ANIMS["human"][self.frame]

            if self.y < self.spawn_height:
                self.y += 1

    def draw(self, scroll_x, ground_w):
        if not self.visible:
            return
        
        # Fix to ensure sprites within -8 pixels left of scroll_x get partially drawn.
        draw_x = self.x - (scroll_x % ground_w)
        if draw_x <= -sprite.SIZE or draw_x > 0:
            draw_x = (self.x - scroll_x) % ground_w

        if draw_x <= -sprite.SIZE or draw_x >= pyxel.width:
          return
        
        if self.beam_up is not None:
            self.beam_up.draw(draw_x)

        w = -sprite.SIZE if self.flip_x else sprite.SIZE
        h = -sprite.SIZE if self.flip_y else sprite.SIZE
        pyxel.blt(draw_x, self.y, self.img, 0, 0, w, h, pyxel.COLOR_BLACK)

        pyxel.circb(draw_x + 4, self.y + 4, 7, 12)

        # pyxel.text(draw_x, self.y + 8, f"beam: {self.beam_up}", 7)
        # pyxel.text(draw_x, self.y + 8, f"y: {self.y}", 7)
        # pyxel.text(draw_x, self.y + 16, f"y: {self.spawn_height}", 7)

# NUM_STAGES = 8
HUMANS_PER_STAGE = (
    7, 9, 11, 13, 15, 15, 17, 19
)

def spawn_all(gameplay):
    ground = gameplay.ground
    step = ground.width // HUMANS_PER_STAGE[gameplay.stage_num]
    for x in range(32, ground.width, step):
        h = ground.get_height_at(x)
        gameplay.humans.append(Human(x - 4, pyxel.height - h - 8))