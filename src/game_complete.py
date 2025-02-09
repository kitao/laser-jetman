import pyxel
import input
from constants import STATE_MAIN_MENU
from utils import draw_centre_x_label
from audio import play_sound
from lava import Lava
import lava
from starfield import Starfield

CYCLE_COLOURS = ( 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )

class GameComplete:
   def __init__(self):
      self.no_skip_frame_cnt = 0
      self.final_score = 0
      self.lava = Lava(pyxel.width / 2, pyxel.height - lava.HEIGHT)
      self.starfield = Starfield()

   def enter(self):
      play_sound("GAME_COMPLETE_DRUMS", True)
      play_sound("GAME_COMPLETE_MELODY", True)
   
   def update(self, current_input):
      self.no_skip_frame_cnt += 1

      self.lava.update()
      self.starfield.update()

      if self.no_skip_frame_cnt > 180:
         if current_input[input.BUTTON_START]:
            pyxel.stop()
            return STATE_MAIN_MENU
      
      return None
   
   def draw(self):
      self.starfield.draw(0)
      self.lava.draw(0)

      y = 40 + pyxel.cos(pyxel.frame_count * 4) * 8
      draw_centre_x_label(y, "CONGRATULATIONS!", 7)
      col = CYCLE_COLOURS[(pyxel.floor(pyxel.frame_count * 0.2)) % len(CYCLE_COLOURS)]
      draw_centre_x_label(72, f"FINAL SCORE: {self.final_score:06}", col)