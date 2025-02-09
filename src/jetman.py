import pyxel
import sprite
from gfx_data import ANIMS
import input
import jetpack
from laser_gun import LaserGun
import utils
import beam_up
from audio import play_sound

AIR_VEL_X = 1
GROUND_VEL_X = 0.5
GRAVITY = 0.25
JETPACK_VEL_Y = -1
MAX_VEL_Y = 2   
WALK_ANIM_SPEED = 4

RESPAWN_INVINCIBLE_FRAMES = 120

class Jetman(sprite.Sprite):
    def __init__(self, gameplay):
        super().__init__(0, 42, ANIMS["jetman_idle"][0])
        self.gameplay = gameplay
        self.total_frames = 0
        self.jetpack = jetpack.Jetpack(self)
        self.grounded = False
        self.grounded_height = 0
        self.vel_x = 0
        self.vel_y = 0
        self.walk_frame = 0
        self.walk_frame_counter = 0
        self.laser_gun = LaserGun()
        self.invincible_frames = 0
        self.has_shield = False

    def kill(self):
        self.visible = False
        play_sound("PLAYER_EXPLOSION")

    def add_shield(self):
        self.has_shield = True
        play_sound("GOT_SHIELD")

    def remove_shield(self):
        self.has_shield = False

    def got_collectables_check(self):
        colls = self.gameplay.collectables
        for c in colls:
            if utils.rect_collision_check_wrap_x(
                self.x, self.y, sprite.SIZE, sprite.SIZE,
                c.x, c.y, sprite.SIZE, sprite.SIZE,
                self.gameplay.ground.width):
                c.collected()

    def rescued_human_check(self, humans):
        for h in humans:
            if not h.can_be_beamed_up():
                continue
            if utils.rect_collision_check_wrap_x(
                self.x, self.y, sprite.SIZE, sprite.SIZE,
                h.x, h.y, sprite.SIZE, sprite.SIZE,
                self.gameplay.ground.width):
                h.start_beam_up(beam_up.TYPE_PLAYER, 0)
                return h
        return None
    
    def hit_rect_check(self, x, y, w, h):
        return utils.rect_collision_check_wrap_x(
            self.x, self.y, sprite.SIZE, sprite.SIZE,
            x, y, w, h,
            self.gameplay.ground.width)

    def got_hit_check(self):
        if self.invincible_frames > 0:
            return False

        if self.has_shield:
            self.remove_shield()
            self.invincible_frames = RESPAWN_INVINCIBLE_FRAMES
            return False
        
        self.kill()
        return True

    def respawn(self):
        self.total_frames = 0
        self.y = 42
        self.visible = True
        self.vel_x = 0
        self.vel_y = 0
        self.img = ANIMS["jetman_idle"][0]
        self.gameplay.centre_scroll_x()
        self.invincible_frames = RESPAWN_INVINCIBLE_FRAMES
        self.has_shield = False
        self.jetpack.reset()
        self.laser_gun.reset()
        play_sound("STAGE_RESPAWN")

    def _check_grounded(self, ground):
        self.grounded_height = ground.get_height_at(pyxel.floor(self.x + 4))
        height = pyxel.height - self.grounded_height
        if self.vel_y >= 0:
            if self.y + sprite.SIZE >= height:
                self.y = height - sprite.SIZE
                self.vel_y = 0
                if self.grounded == False:
                    play_sound("PLAYER_LANDS")
                self.grounded = True
            else:
                self.grounded = False
        else:
            self.grounded = False

    def update(self, current_input):
        self.total_frames += 1

        self.vel_y = min(MAX_VEL_Y, self.vel_y + GRAVITY)
        if current_input[input.UP]:
            self.jetpack.fire()
            self.vel_y = JETPACK_VEL_Y
        else:
            self.jetpack.stop()

        self.laser_gun.update()
        if current_input[input.BUTTON_1]:
            x = self.x - 1 if self.flip_x else self.x + sprite.SIZE
            self.laser_gun.shoot(self.gameplay, x, self.y + 4, -1 if self.flip_x else 1)

        vel_x = 0
        if current_input[input.LEFT]:
            vel_x = -1
            self.flip_x = True
        elif current_input[input.RIGHT]:
            vel_x = 1
            self.flip_x = False

        if self.grounded:
            self.vel_x = vel_x * GROUND_VEL_X
            if vel_x != 0:
                self.walk_frame_counter += 1
                if self.walk_frame_counter >= WALK_ANIM_SPEED:
                    self.walk_frame_counter = 0
                    self.walk_frame = (self.walk_frame + 1) % len(ANIMS["jetman_walk"])
                self.img = ANIMS["jetman_walk"][self.walk_frame]
            else:
                self.img = ANIMS["jetman_idle"][0]
        else:
            self.vel_x = vel_x * AIR_VEL_X
            self.img = ANIMS["jetman_idle"][0]

        self.x += self.vel_x
        self.y = max(8, self.y + self.vel_y)

        self._check_grounded(self.gameplay.ground)

        self.got_collectables_check()

        self.jetpack.update()

        if self.invincible_frames > 0:
            self.invincible_frames -= 1
            if self.invincible_frames == 0:
                self.visible = True
            else:
                if self.total_frames % 5 == 0:
                    self.visible = not self.visible

    def draw(self):
        if not self.visible:
            return

        self.jetpack.draw()
        super().draw()
        x = self.x - 1 if self.flip_x else self.x + sprite.SIZE
        self.laser_gun.draw(x, self.y + 4)

        if self.has_shield:
            pyxel.circb(self.x + 4, self.y + 4, 8, 12)

        #pyxel.text(self.x, self.y - 8, 
        #           f"x: {pyxel.floor(self.x % self.gameplay.ground.width)}", 7)