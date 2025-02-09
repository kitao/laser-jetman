import pyxel
import utils

SCREEN_SIZE = 256
LAYOUT_WIDTH = 128


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class TestAngles:
    def __init__(self):
        self.src_x = 64
        self.src_y = 64
        self.angle = 0
        self.label = ""

    def run(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, display_scale=2)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.src_x, self.src_y = pyxel.mouse_x, pyxel.mouse_y

        self.label = f"Angle from [{self.src_x % LAYOUT_WIDTH}, " + \
            f"{self.src_y}] to [{pyxel.mouse_x % LAYOUT_WIDTH}, " + \
            f"{pyxel.mouse_y}]"

        self.angle = utils.get_angle_wrap_x(self.src_x, self.src_y, 
                                            pyxel.mouse_x, pyxel.mouse_y, 
                                            LAYOUT_WIDTH)

    def draw(self):
        pyxel.cls(0)
        pyxel.line(LAYOUT_WIDTH, 0, LAYOUT_WIDTH, pyxel.height, 1)
        pyxel.text(8, 8, self.label, 4)

        end_x = self.src_x + pyxel.cos(self.angle) * 32
        end_y = self.src_y + pyxel.sin(self.angle) * 32

        pyxel.line(self.src_x, self.src_y, end_x, end_y, 1)

        pyxel.pset(self.src_x, self.src_y, 7)
        pyxel.text(self.src_x, self.src_y - 8, 
                   f"{self.src_x}, " + 
                   f"{self.src_y}", 8)
        
        pyxel.text(pyxel.mouse_x, pyxel.mouse_y - 8, 
                   f"{pyxel.mouse_x}, " +
                   f"{pyxel.mouse_y}", 7)
        pyxel.text(pyxel.mouse_x, pyxel.mouse_y + 8, 
                   f"Angle: {pyxel.floor(self.angle)}", 2)
        # pyxel.text(pyxel.mouse_x, pyxel.mouse_y + 16, 
        #            f"Result: {self.result}", 13)


class TestCollisions:
    def __init__(self):
        self.rect1 = Rect(0, 0, 32, 32)
        self.rect2 = Rect(0, 0, 32, 32)
        self.result = False

    def run(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, display_scale=2)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.rect1.x, self.rect1.y = pyxel.mouse_x, pyxel.mouse_y

        self.rect2.x, self.rect2.y = pyxel.mouse_x, pyxel.mouse_y

        self.result = utils.rect_collision_check_wrap_x(
            self.rect1.x, self.rect1.y, self.rect1.w, self.rect1.h, 
            self.rect2.x, self.rect2.y, self.rect2.w, self.rect2.h, 
            LAYOUT_WIDTH)

    def draw(self):
        pyxel.cls(0)
        pyxel.line(LAYOUT_WIDTH, 0, LAYOUT_WIDTH, pyxel.height, 1)

        pyxel.rectb(self.rect1.x, self.rect1.y, self.rect1.w, self.rect1.h, 8)
        pyxel.rectb(self.rect2.x, self.rect2.y, self.rect2.w, self.rect2.h, 7)
        
        pyxel.text(pyxel.mouse_x, pyxel.mouse_y - 8, 
                   f"Result: {self.result}", 13)


class TestsQuick:
    def run():
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE)

        rect1 = Rect(160, 64, 8, 8)
        rect2 = Rect(160, 96, 8, 8)

        result = utils.get_angle_wrap_x(rect1.x, rect1.y, 
                                        rect2.x, rect2.y, 
                                        LAYOUT_WIDTH)
        print(f"Angle from Rect1 to Rect2: {result}")
        result = utils.rect_collision_check_wrap_x(
            rect1.x, rect1.y, rect1.w, rect1.h, 
            rect2.x, rect2.y, rect2.w, rect2.h, 
            LAYOUT_WIDTH)
        print(f"Rect1 and Rect2 collide? : {result}")

        pyxel.quit()


TestAngles().run()
#TestCollisions().run()
#TestsQuick.run()