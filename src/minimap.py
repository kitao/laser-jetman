import pyxel
import lava
import constants

# [ redeye, bomber, lander, mutant, pod, swarmer ]
ENEMY_COLOUR = (
    pyxel.COLOR_YELLOW,
    pyxel.COLOR_GREEN,
    pyxel.COLOR_RED,
    pyxel.COLOR_LIME,
    pyxel.COLOR_PURPLE,
    pyxel.COLOR_PINK
)

class Minimap:
    def __init__(self, gameplay, width=128, height=8):
        self.gameplay = gameplay
        self.ground = gameplay.ground
        self.player = gameplay.player
        self.width = width
        self.height = height

    def draw(self):
        div_width = self.ground.width / self.width
        player_x = int(self.player.x * self.width / self.ground.width)
        scroll_x = player_x - self.width // 2

        pyxel.rect(0, 0, pyxel.width, self.height, pyxel.COLOR_BLACK)

        for x in range(self.width):
            ground_x = int((x + scroll_x) % self.width * div_width)
            height = self.ground.get_height_at(ground_x)
            col = pyxel.COLOR_NAVY if height >= lava.HEIGHT else pyxel.COLOR_PURPLE
            pyxel.pset(x, self.height - (height * self.height // self.ground.max_height), col)
        
        # Draw the player
        pyxel.circ(self.width // 2, (self.player.y / pyxel.height) * 8, 1, pyxel.COLOR_WHITE)

        # Draw humans
        for h in self.gameplay.humans:
            human_x = int((h.x * self.width / self.ground.width) - scroll_x) % self.width
            pyxel.pset(human_x, (h.y / pyxel.height) * 8, pyxel.COLOR_WHITE)

        # Draw Collectables
        for c in self.gameplay.collectables:
            collect_x = int((c.x * self.width / self.ground.width) - scroll_x) % self.width
            pyxel.circ(collect_x, (c.y / pyxel.height) * 8, 1, pyxel.COLOR_DARK_BLUE)

        # Draw enemies
        for e in self.gameplay.enemies:
            enemy_x = int((e.x * self.width / self.ground.width) - scroll_x) % self.width
            pyxel.pset(enemy_x, (e.y / pyxel.height) * 8, ENEMY_COLOUR[e.type])
            if e.type == constants.ENEMY_TYPE_LANDER and e.is_beaming_up_human():
                pyxel.circb(enemy_x, (e.y / pyxel.height) * 8, 3, pyxel.COLOR_RED)

        # Screen width lines
        scroll = 4 if not self.gameplay.player.flip_x else -4
        x = 55 + scroll
        pyxel.line(x, 7, x + 16, 7, pyxel.COLOR_DARK_BLUE)