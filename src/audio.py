import pyxel
from sound_data import SOUNDS

def play_sound(name, looping=False):
    s = SOUNDS.get(name)
    if s is not None:
        pyxel.play(s["channel"], s["index"], loop=looping)