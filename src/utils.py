import pyxel

def rect_collision(x1, y1, width1, height1, x2, y2, width2, height2):
    return (
        x1 < x2 + width2 and
        x1 + width1 > x2 and
        y1 < y2 + height2 and
        y1 + height1 > y2
    )

def check_overlapping_ranges(lower1, width1, lower2, width2, layout_width):
    lower2 = (lower2 - lower1) % layout_width
    return lower2 <= width1 or lower2 + width2 >= layout_width

def rect_collision_check_wrap_x(rect1_x, rect1_y, rect1_w, rect1_h,
                                rect2_x, rect2_y, rect2_w, rect2_h, 
                                layout_width):
    return (
        check_overlapping_ranges(rect1_x, rect1_w, rect2_x, rect2_w, 
                                 layout_width) and
            rect1_y < rect2_y + rect2_h and 
            rect1_y + rect1_h > rect2_y
    )

def get_angle_wrap_x(x1, y1, x2, y2, layout_width):
    dx = (x2 - x1) % layout_width
    if dx > layout_width / 2:
        dx -= layout_width
    return pyxel.atan2(y2 - y1, dx)

def lerp(a, b, t):
    return (1 - t) * a + t * b

def text(x, y, str, text_col=pyxel.COLOR_WHITE):
    pyxel.text(x + 1, y + 1, str, pyxel.COLOR_BLACK)
    pyxel.text(x, y, str, text_col)

def draw_label(x, y, str, text_col=pyxel.COLOR_WHITE, label_col=pyxel.COLOR_DARK_BLUE):
   str_w = (len(str) * pyxel.FONT_WIDTH)
   pyxel.rect(x - 8 + 1, y + 1, str_w + 16, 8, pyxel.COLOR_NAVY)
   pyxel.rect(x - 8, y, str_w + 16, 8, label_col)
   text(x, y + 1, str, text_col)

def draw_centre_x_label(y, str, text_col=pyxel.COLOR_WHITE, label_col=pyxel.COLOR_DARK_BLUE):
   x = (pyxel.width // 2) - (get_str_width(str) // 2)
   draw_label(x, y, str, text_col, label_col)

def get_str_width(str):
    return len(str) * pyxel.FONT_WIDTH

