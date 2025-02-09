import pyxel
from gfx_data import ANIMS
from human import HUMANS_PER_STAGE

ANCHOR_Y = 120

HUMAN_X = 56

CYCLE_COLOURS = ( 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )

def draw(gameplay):
    pyxel.rect(0, pyxel.height - 8, pyxel.width, 8, 0)

    col = CYCLE_COLOURS[(pyxel.floor(pyxel.frame_count * 0.2)) % len(CYCLE_COLOURS)]
    pyxel.text(2, ANCHOR_Y + 1, f"SC:{gameplay.score:06}", col)

    pyxel.text(HUMAN_X, ANCHOR_Y + 1, f"{HUMANS_PER_STAGE[gameplay.stage_num]:02}", 7)
    pyxel.blt(HUMAN_X + 8, ANCHOR_Y, ANIMS["human"][0], 0, 0, 8, 8)
    pyxel.text(HUMAN_X + 16, ANCHOR_Y + 1, f"{gameplay.humans_rescued:02}", 3)
    pyxel.text(HUMAN_X + 26, ANCHOR_Y + 1, ":", 7)
    pyxel.text(HUMAN_X + 32, ANCHOR_Y + 1, f"{gameplay.mutants_created:02}", 8)

    # Draw lives
    for i in range(gameplay.lives):
        pyxel.blt(pyxel.width - 2 - (gameplay.lives * 9) + (i * 9), ANCHOR_Y, ANIMS["jetman_idle"][0], 0, 0, 8, 8)