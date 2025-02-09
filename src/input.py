import pyxel

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
BUTTON_1 = "button_1"
BUTTON_2 = "button_2"
BUTTON_START = "button_start"

# Constants for input
KEY_UP = pyxel.KEY_W
KEY_DOWN = pyxel.KEY_S
KEY_LEFT = pyxel.KEY_A
KEY_RIGHT = pyxel.KEY_D
KEY_BUTTON_1 = pyxel.KEY_J
KEY_BUTTON_2 = pyxel.KEY_K
KEY_BUTTON_START = pyxel.KEY_RETURN

# Alternative keyboard constants using arrow keys
KEY_ALT_UP = pyxel.KEY_UP
KEY_ALT_DOWN = pyxel.KEY_DOWN
KEY_ALT_LEFT = pyxel.KEY_LEFT
KEY_ALT_RIGHT = pyxel.KEY_RIGHT

# Constants for gamepad input
GAMEPAD_UP = pyxel.GAMEPAD1_BUTTON_DPAD_UP
GAMEPAD_DOWN = pyxel.GAMEPAD1_BUTTON_DPAD_DOWN
GAMEPAD_LEFT = pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
GAMEPAD_RIGHT = pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
GAMEPAD_BUTTON_1 = pyxel.GAMEPAD1_BUTTON_A
GAMEPAD_BUTTON_2 = pyxel.GAMEPAD1_BUTTON_B
GAMEPAD_BUTTON_START = pyxel.GAMEPAD1_BUTTON_START

def poll():
    up = pyxel.btn(KEY_UP) or pyxel.btn(KEY_ALT_UP) or pyxel.btn(GAMEPAD_UP)
    down = pyxel.btn(KEY_DOWN) or pyxel.btn(KEY_ALT_DOWN) or pyxel.btn(GAMEPAD_DOWN)
    left = pyxel.btn(KEY_LEFT) or pyxel.btn(KEY_ALT_LEFT) or pyxel.btn(GAMEPAD_LEFT)
    right = pyxel.btn(KEY_RIGHT) or pyxel.btn(KEY_ALT_RIGHT) or pyxel.btn(GAMEPAD_RIGHT)
    button_1 = pyxel.btn(KEY_BUTTON_1) or pyxel.btn(GAMEPAD_BUTTON_1)
    button_2 = pyxel.btn(KEY_BUTTON_2) or pyxel.btn(GAMEPAD_BUTTON_2)
    button_start = pyxel.btnp(KEY_BUTTON_START) or pyxel.btnp(GAMEPAD_BUTTON_START)
    
    return {
        UP: up,
        DOWN: down,
        LEFT: left,
        RIGHT: right,
        BUTTON_1: button_1,
        BUTTON_2: button_2,
        BUTTON_START : button_start
    }
