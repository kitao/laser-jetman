import pyxel
from constants import STATE_MAIN_MENU, STATE_LOAD_NEXT_STAGE, STATE_GAME_COMPLETE
import constants
from jetman import Jetman
from ground import Ground
from lava import Lava
import lava
from minimap import Minimap
from utils import lerp, draw_centre_x_label
from starfield import Starfield
import hud
import input
from player_explosion import PlayerExplosion
import human
import enemy_spawn
import enemy_bullet
import sprite
from human import HUMANS_PER_STAGE
from collectable_shield import CollectableShield
from audio import play_sound

STATE_GET_READY = "GET_READY"
STATE_PLAY = "PLAY"
STATE_PLAYER_EXPLODE = "PLAYER_EXPLODE"
STATE_STAGE_COMPLETE = "STAGE_COMPLETE"
STATE_GAME_OVER = "GAME_OVER"
STATE_PAUSED = "PAUSED"
STATE_BEAM_UP_HUMAN = "BEAM_UP_HUMAN"

GET_READY_FRAMES = 120
GAME_OVER_FRAMES = 180
STAGE_COMPLETE_FRAMES = 180

CHECK_NEW_SHIELD_FRAMES = 120

class Gameplay:
    def __init__(self, stage_num):
        self.stage_num = stage_num
        self.state = STATE_GET_READY
        self.state_before_pause = STATE_GET_READY

        self.player = Jetman(self)
        self.ground = Ground()
        self.lava = Lava(pyxel.width / 2, pyxel.height - lava.HEIGHT)
        self.scroll_x = 0
        self.scroll_x_target = 0
        self.lasers = []
        self.explosions = []
        self.enemies = []
        self.enemy_bullets = []
        self.enemy_spawns = []
        enemy_spawn.create_all(self)

        self.humans = []
        human.spawn_all(self)
        self.human_to_beam_up = None
        self.mutants_created = 0
        self.humans_rescued = 0
        self.current_abductions = 0

        self.collectables = []
        self.shield_cnt = 0
        self.spawn_shield_check_frames = CHECK_NEW_SHIELD_FRAMES

        self.starfield = Starfield()

        self.stage_frames = 0
        self.time_bonus_achieved = False

        self.lives = 3
        self.score = 0

        self.state_frame_cnt = 0

        self.minimap = Minimap(self)

        self._switch_state(STATE_GET_READY)
        self.player.respawn()
        self.lives = max(0, self.lives - 1)

    def add_score(self, sc):
        self.score = min(constants.MAX_SCORE, self.score + sc)

    def player_died(self):
        self.lasers = []
        self.explosions.append(PlayerExplosion(self.player))
        self._switch_state(STATE_PLAYER_EXPLODE)

    def _update_effects(self):
        self.scroll_x = lerp(self.scroll_x, self.scroll_x_target, 0.1)
        self.lava.update()
        self.starfield.update()
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if not e.finished]

    def _check_new_shield_required(self):
        self.spawn_shield_check_frames -= 1
        if self.spawn_shield_check_frames == 0:
            self.spawn_shield_check_frames = CHECK_NEW_SHIELD_FRAMES
            if not self.player.has_shield and self.shield_cnt == 0:
                self.collectables.append(CollectableShield(self))

    def _update_objects(self, current_input):
        for s in self.lasers:
            s.update()
        self.lasers = [s for s in self.lasers if not s.remove]
        self.player.update(current_input)

        self._check_new_shield_required()
        for c in self.collectables:
            c.update()
        self.collectables = [c for c in self.collectables if not c.remove]

        for h in self.humans:
            h.update()

        for e in self.enemy_spawns:
            e.update()

        for e in self.enemies:
            e.update()
        self.enemies = [e for e in self.enemies if not e.remove]

        for e in self.enemy_bullets:
            e.update()
        self.enemy_bullets = [e for e in self.enemy_bullets if not e.remove]

    def _check_for_game_over(self):
        return self.mutants_created > HUMANS_PER_STAGE[self.stage_num] // 2

    def _update_get_ready(self):
        if self.state_frame_cnt == GET_READY_FRAMES:
            self._switch_state(STATE_PLAY)
        self._update_effects()
        return None
    
    def _player_died_in_lava_check(self):
        if self.player.has_shield:
            return False
        if self.player.y + 7 > pyxel.height - lava.HEIGHT:
            if self.player.got_hit_check():
                self.player_died()
                return True
        return False
    
    def _player_hit_enemy_bullet_check(self):
        for e in self.enemy_bullets:
            if self.player.hit_rect_check(e.x, e.y, 
                                          enemy_bullet.SIZE, 
                                          enemy_bullet.SIZE):
                e.remove = True
                e.visible = False
                if self.player.got_hit_check():
                    self.player_died()
                    return True
        return False
    
    def _player_hit_enemy_check(self):
        for e in self.enemies:
            if e.invincible_frames > 0:
                continue
            if self.player.hit_rect_check(e.x, e.y, 
                                          sprite.SIZE, 
                                          sprite.SIZE):
                e.destroy()
                if self.player.got_hit_check():
                    self.player_died()
                    return True
        return False
    
    def _update_play(self, current_input):
        if current_input[input.BUTTON_START]:
            self.state_before_pause = STATE_PLAY
            self._switch_state(STATE_PAUSED)
            return None

        if self._player_died_in_lava_check():
            return None
        
        if self._player_hit_enemy_bullet_check():
            return None
        
        if self._player_hit_enemy_check():
            return None
        
        self.human_to_beam_up = self.player.rescued_human_check(self.humans)
        if self.human_to_beam_up is not None:
            self._switch_state(STATE_BEAM_UP_HUMAN)
            return None

        self._update_objects(current_input)

        if self._check_for_game_over():
            self._switch_state(STATE_GAME_OVER)
            return None
        
        # Last human was mutated but not > half, so stage complete.
        if len(self.humans) == 0:
            self._switch_state(STATE_STAGE_COMPLETE)
            return None

        if self.player.flip_x:
            self.scroll_x_target = self.player.x - 96
        else:
            self.scroll_x_target = self.player.x - 24

        self._update_effects()

        self.stage_frames += 1

        return None
    
    def centre_scroll_x(self):
        self.scroll_x_target = self.player.x - 60
    
    def _update_player_explode(self):
        self._update_effects()
        if len(self.explosions) == 0:
            if self.lives > 0:
                self._switch_state(STATE_GET_READY)
                self.player.respawn()
                self.lives = max(0, self.lives - 1)
                self.enemy_bullets = []
            else:
                #play_sound("GAME_OVER")
                self._switch_state(STATE_GAME_OVER)
        return None
    
    def _update_beam_up_human(self, current_input):
        if current_input[input.BUTTON_START]:
            self.state_before_pause = STATE_BEAM_UP_HUMAN
            self._switch_state(STATE_PAUSED)
            return None

        #self._update_effects()
        self.human_to_beam_up.update()
        if self.human_to_beam_up.remove:
            self.add_score(constants.SCORE_RESCUE_HUMAN)
            self._switch_state(STATE_PLAY)
            self.human_to_beam_up.remove = True
            self.humans_rescued += 1
            for h in self.humans:
                if h.remove:
                    self.humans.remove(h)
        if len(self.humans) == 0:
            if self.stage_frames < constants.STAGE_MAX_TIME_BONUS[self.stage_num] * 60:
                self.time_bonus_achieved = True
                self.add_score(constants.SCORE_TIME_BONUS)
            if self.humans_rescued == HUMANS_PER_STAGE[self.stage_num]:
                self.add_score(constants.SCORE_100PC_RESCUE_BONUS)
            play_sound("STAGE_COMPLETE")
            self._switch_state(STATE_STAGE_COMPLETE)
        return None
    
    def _update_stage_complete(self):
        if self.state_frame_cnt == STAGE_COMPLETE_FRAMES:
            if self.stage_num == constants.NUM_STAGES - 1:
                return STATE_GAME_COMPLETE
            else:
                return STATE_LOAD_NEXT_STAGE
        
        self._update_effects()

        return None
    
    def _update_game_over(self):
        if self.state_frame_cnt == GAME_OVER_FRAMES:
            return STATE_MAIN_MENU
        self._update_effects()
        return None
    
    def _update_paused(self, current_input):
        if current_input[input.BUTTON_START]:
            self._switch_state(self.state_before_pause)
        elif current_input[input.BUTTON_2]:
            return STATE_MAIN_MENU
        return None
   
    def _switch_state(self, new_state):
        self.state = new_state
        self.state_frame_cnt = 0

    def update(self, current_input):
        self.state_frame_cnt += 1

        if self.state == STATE_GET_READY:
            return self._update_get_ready()
        elif self.state == STATE_PLAY:
            return self._update_play(current_input)
        elif self.state == STATE_PAUSED:
            return self._update_paused(current_input)
        elif self.state == STATE_GAME_OVER:
            return self._update_game_over()
        elif self.state == STATE_PLAYER_EXPLODE:
            return self._update_player_explode()
        elif self.state == STATE_BEAM_UP_HUMAN:
            return self._update_beam_up_human(current_input)
        else: # self.state == STATE_STAGE_COMPLETE:
            return self._update_stage_complete()
   
    def draw(self):
        self.starfield.draw(self.scroll_x)
        self.lava.draw(self.scroll_x)
        self.ground.draw(self.scroll_x)

        for h in self.humans:
            h.draw(self.scroll_x, self.ground.width)

        for c in self.collectables:
            c.draw(self.scroll_x, self.ground.width)

        # Relative camera
        pyxel.camera(self.scroll_x, 0)
        for s in self.lasers:
            s.draw()
        self.player.draw()
        for e in self.explosions:
            e.draw()

        # Reset camera
        pyxel.camera()
        for e in self.enemy_spawns:
            e.draw(self.scroll_x, self.ground.width)
        for e in self.enemies:
            e.draw(self.scroll_x, self.ground.width)
        for e in self.enemy_bullets:
            e.draw(self.scroll_x, self.ground.width)

        self.minimap.draw()
        hud.draw(self)

        if self.state == STATE_GET_READY:
            draw_centre_x_label(24, f"STAGE {self.stage_num + 1}")
            draw_centre_x_label(56, "GET READY", label_col=pyxel.COLOR_PURPLE)
        elif self.state == STATE_PAUSED:
            draw_centre_x_label(56, "PAUSED")
            draw_centre_x_label(72, "PRESS BUTTON B TO EXIT")
        elif self.state == STATE_GAME_OVER:
            draw_centre_x_label(56, "GAME OVER")
        elif self.state == STATE_STAGE_COMPLETE:
            draw_centre_x_label(56, "STAGE COMPLETE")
            if self.time_bonus_achieved:
                draw_centre_x_label(24, f"TIME BONUS: {constants.SCORE_TIME_BONUS}", label_col=pyxel.COLOR_GREEN)
            if self.humans_rescued == HUMANS_PER_STAGE[self.stage_num]:
                draw_centre_x_label(40, f"100% RESCUE BONUS: {constants.SCORE_100PC_RESCUE_BONUS}", label_col=pyxel.COLOR_GREEN)

        # pyxel.text(0, 8, f"Time: {self.stage_frames // 60}", 7)

        #pyxel.text(0, 8, f"En: {len(self.enemies)}", 7)
        #pyxel.text(0, 16, f"Ex: {len(self.explosions)}", 7)

        #pyxel.text(0, 8, f"{self.state}", 7)
        #pyxel.text(0, 16, f"Scroll X: {self.scroll_x}", 7)