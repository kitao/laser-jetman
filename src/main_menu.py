import pyxel
from utils import draw_centre_x_label, lerp
import input
from constants import STATE_GAMEPLAY
import gfx_data
from particle import Emitter, PARTICLES_SHAPE_POINT
from audio import play_sound

STATE_TOP_LASER = 0
STATE_TITLE_LASER = 1
STATE_BOTTOM_LASER = 2
STATE_AWAIT_INPUT = 3

STATE_TOP_LASER_FRAMES = 40
STATE_TITLE_LASER_FRAMES = 70
STATE_BOTTOM_LASER_FRAMES = 95

CYCLE_COLOURS = ( 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )

class MainMenu:
   def __init__(self, app):
      self.app = app
      self.titles_img = self._make_title_img()
      self.state = STATE_TOP_LASER
      self.state_frames = 0
      self.emitter = None

   def enter(self):
      self.emitter = self._make_sparks_emitter()
      self._switch_state(STATE_TOP_LASER)
      pyxel.stop()
      play_sound("JETPACK_FIRE", True)

   def _make_sparks_emitter(self):
      e = Emitter(40, 0, 50, 30)
      e.particles_shape = PARTICLES_SHAPE_POINT
      e.particles_per_frame = 5
      e.particle_life_min = 10
      e.particle_life_max = 30
      #
      e.particle_color_order = ( 10, 9, 8, 1 )
      return e

   def _switch_state(self, new_state):
      self.state = new_state
      self.state_frames = 0

   def _update_top_laser(self):
      n = lerp(0, 33, self.state_frames / STATE_TOP_LASER_FRAMES)
      self.emitter.y = n
      self.emitter.emit()
      if self.state_frames == STATE_TOP_LASER_FRAMES:
         self._switch_state(STATE_TITLE_LASER)
         self.emitter.y += 9
         self.emitter.particle_y_pos_range = 10
      return None
   
   def _update_title_laser(self):
      n = lerp(0, 47, self.state_frames / STATE_TITLE_LASER_FRAMES)
      self.emitter.x = 40 + n
      self.emitter.emit()
      if self.state_frames == STATE_TITLE_LASER_FRAMES:
         self._switch_state(STATE_BOTTOM_LASER)
         self.emitter.y += 9
         self.emitter.particle_y_pos_range = 1
      return None
   
   def _update_bottom_laser(self):
      n = lerp(0, 78, self.state_frames / STATE_BOTTOM_LASER_FRAMES)
      self.emitter.y = 50 + n
      self.emitter.emit()
      if self.state_frames == STATE_BOTTOM_LASER_FRAMES:
         pyxel.stop()
         play_sound("PLAYER_EXPLOSION")
         self._switch_state(STATE_AWAIT_INPUT)
      return None
   
   def _update_await_input(self, current_input):
      if current_input[input.BUTTON_START]:
         return STATE_GAMEPLAY
      return None
   
   def _make_title_img(self):
      img = pyxel.Image(47, 18)

      laser = (
         gfx_data.ANIMS["title_letter_l"],
         gfx_data.ANIMS["title_letter_a"],
         gfx_data.ANIMS["title_letter_s"],
         gfx_data.ANIMS["title_letter_e"],
         gfx_data.ANIMS["title_letter_r"],
      )
      jetman = (
         gfx_data.ANIMS["title_letter_j"],
         gfx_data.ANIMS["title_letter_e"],
         gfx_data.ANIMS["title_letter_t"],
         gfx_data.ANIMS["title_letter_m"],
         gfx_data.ANIMS["title_letter_a"],
         gfx_data.ANIMS["title_letter_n"],
      )

      img.cls(0)

      for i in range(len(laser)):
         img.blt(i * 8, 0, laser[i][0], 0, 0, 8, 8, 0)
      
      for i in range(len(jetman)):
         img.blt(i * 8, 10, jetman[i][0], 0, 0, 8, 8, 0)

      return img

   def update(self, current_input):
      self.state_frames += 1
      self.emitter.update()
      if self.state == STATE_TOP_LASER:
         return self._update_top_laser()
      elif self.state == STATE_TITLE_LASER:
         return self._update_title_laser()
      elif self.state == STATE_BOTTOM_LASER:
         return self._update_bottom_laser()
      else: # if self.state == STATE_AWAIT_INPUT:
         return self._update_await_input(current_input)
   
   def draw(self):
      if self.state == STATE_TOP_LASER:
         n = lerp(0, 33, self.state_frames / STATE_TOP_LASER_FRAMES)
         pyxel.line(40, 0, 40, n, 8)
      elif self.state == STATE_TITLE_LASER:
         pyxel.line(40, 0, 40, 33, 8)
         n = lerp(0, 47, self.state_frames / STATE_TITLE_LASER_FRAMES)
         pyxel.blt(40, 32, self.titles_img, 0, 0, n, 18, 0)
      elif self.state == STATE_BOTTOM_LASER:
         pyxel.line(40, 0, 40, 33, 8)
         pyxel.blt(40, 32, self.titles_img, 0, 0, 47, 18, 0)
         n = lerp(0, 78, self.state_frames / STATE_BOTTOM_LASER_FRAMES)
         pyxel.line(86, 50, 86, 50 + n, 8)
      else: # if self.state == STATE_AWAIT_INPUT:
         pyxel.line(40, 0, 40, 33, 8)
         pyxel.blt(40, 32, self.titles_img, 0, 0, 47, 18, 0)
         pyxel.line(86, 50, 86, 128, 8)
         draw_centre_x_label(80, "PRESS START", 7)

         col = CYCLE_COLOURS[(pyxel.floor(pyxel.frame_count * 0.2)) % len(CYCLE_COLOURS)]
         pyxel.text(34, 120, f"HI-SCORE:{self.app.high_score:06}", col)

      self.emitter.draw()
      # pyxel.text(0,0, f"{self.state},{self.state_frames}", 7)