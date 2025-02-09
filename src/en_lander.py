import pyxel
import enemy
from gfx_data import ANIMS
import constants
import beam_up
from en_mutant import EnMutant
import enemy_bullet
from audio import play_sound

RESET_HEIGHT = 24

STATE_ROAM = 0
STATE_BEAM_UP = 1

MAX_BEAM_UP_FRAMES = 180 # 3 secs

MAX_NEXT_BEAM_ATTEMPT_FRAMES = 300

class EnLander(enemy.Enemy):
    def __init__(self, gameplay, x, y):
        super().__init__(gameplay, x, y, ANIMS["lander"][0], 
                         constants.ENEMY_TYPE_LANDER)

        self.angle_x = pyxel.rndi(0, 360)
        self.angle_y = pyxel.rndi(0, 360)

        self.state = STATE_ROAM
        self.state_frames = 0

        self.beam_up = None
        self.next_beam_attempt_frames = MAX_NEXT_BEAM_ATTEMPT_FRAMES

    def destroy(self):
        if self.beam_up is not None:
            self.beam_up.human.remove_beam()
            self.gameplay.current_abductions -= 1
        super().destroy()

    def _switch_state(self, new_state):
        self.state = new_state
        self.state_frames = 0

    def is_beaming_up_human(self):
        return self.state == STATE_BEAM_UP

    def _scanned_human_below(self):
        ground_w = self.gameplay.ground.width
        humans = self.gameplay.humans
        for h in humans:
            if not h.can_be_beamed_up():
                continue
            if (((self.x + 4) - (h.x + 4)) % ground_w) < 2:
                self.beam_up = h.start_beam_up(beam_up.TYPE_ENEMY, self.y + 8)
                self.gameplay.current_abductions += 1
                return True
        return False

    def _update_state_roam(self):
        self.next_beam_attempt_frames = max(0, self.next_beam_attempt_frames - 1)

        if self.gameplay.current_abductions == 0 and \
            self.next_beam_attempt_frames == 0:
            if self._scanned_human_below():
                self._switch_state(STATE_BEAM_UP)
                return

        self.angle_x = (self.angle_x + 0.1) % 360
        self.vel_x = pyxel.sin(self.angle_x) * 0.8

        self.angle_y = (self.angle_y + 6) % 360
        self.vel_y = pyxel.cos(self.angle_y) * 0.1

        self._move()
        self.flip_x = True if self.vel_x < 0 else False

    def _update_beam_up(self):
        if self.beam_up is not None:
            if self.beam_up.is_finished():
                self.gameplay.current_abductions -= 1
                self.next_beam_attempt_frames = MAX_NEXT_BEAM_ATTEMPT_FRAMES
                self.gameplay.enemies.append(
                    EnMutant(self.gameplay, self.beam_up.human.x,
                             self.beam_up.human.y))
                self.gameplay.mutants_created += 1
                self.gameplay.humans.remove(self.beam_up.human)
                self.beam_up = None
                self._switch_state(STATE_ROAM)
                return
            if pyxel.play_pos(3) is None:
                play_sound("ENEMY_BEAM_UP")
            self.beam_up.update()

    def update(self):
        self.total_frames += 1

        if self.state == STATE_ROAM:
            self._update_state_roam()
        elif self.state == STATE_BEAM_UP:
            self._update_beam_up()

        if self.total_frames % 420 == 0:
            self._shoot_at_player(enemy_bullet.SPEED_SLOW)

        self._update_invincible_frames()
        self._got_hit_check()

    def draw(self, scroll_x, ground_w):
        super().draw(scroll_x, ground_w)

        if self.beam_up is not None:
            self.beam_up.draw(self.last_draw_x)
        
        #pyxel.text(self.last_draw_x, self.y - 8, f"State: {self.state}", 7)