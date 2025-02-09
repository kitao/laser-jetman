import pyxel
from main_menu import MainMenu
from gameplay import Gameplay
from game_complete import GameComplete
import input
from constants import STATE_MAIN_MENU, STATE_GAMEPLAY, STATE_LOAD_NEXT_STAGE, STATE_GAME_COMPLETE
import gfx_data
import sound_data

class App:
    def __init__(self):
        self.state = STATE_MAIN_MENU # STATE_GAME_COMPLETE
        self.current_input = None
        pyxel.init(128, 128, title="Laser Jetman", 
                    fps=60, display_scale=4, capture_scale=1,
                    capture_sec=60)
        
        gfx_data.make_all()
        sound_data.add_all()
        self.high_score = 0
        self.main_menu = MainMenu(self)
        self.main_menu.enter()
        self.gameplay = None
        self.game_complete = GameComplete()
        #self.game_complete.enter()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.current_input = input.poll()
        new_state = None

        if self.state == STATE_MAIN_MENU:
            new_state = self.main_menu.update(self.current_input)
        elif self.state == STATE_GAMEPLAY:
            new_state = self.gameplay.update(self.current_input)
            self.high_score = max(self.gameplay.score, self.high_score)
        elif self.state == STATE_GAME_COMPLETE:
            new_state = self.game_complete.update(self.current_input)

        if new_state is not None:
            if new_state == STATE_GAMEPLAY:
                self._new_stage(0)
            elif new_state == STATE_LOAD_NEXT_STAGE:
                self._load_next_stage()
            elif new_state == STATE_MAIN_MENU:
                self.state = STATE_MAIN_MENU
                self.main_menu.enter()
            elif new_state == STATE_GAME_COMPLETE:
                self.state = STATE_GAME_COMPLETE
                self.game_complete.final_score = self.gameplay.score
                self.game_complete.enter()

    def _load_next_stage(self):
        lives = self.gameplay.lives
        score = self.gameplay.score
        self._new_stage(self.gameplay.stage_num + 1)
        self.gameplay.lives = lives
        self.gameplay.score = score

    def _new_stage(self, stage_num):
        self.state = STATE_GAMEPLAY
        pyxel.rseed(pyxel.frame_count)
        pyxel.nseed(pyxel.rndi(0, pyxel.frame_count))
        self.gameplay = Gameplay(stage_num)

    def draw(self):
        pyxel.cls(0)
        if self.state == STATE_MAIN_MENU:
            self.main_menu.draw()
        elif self.state == STATE_GAMEPLAY:
            self.gameplay.draw()
        elif self.state == STATE_GAME_COMPLETE:
            self.game_complete.draw()

if __name__ == "__main__":
    App()
