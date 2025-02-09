import pyxel
import sprite
from enemy_explosion import EnemyExplosion
import constants
from enemy_bullet import EnemyBullet
from audio import play_sound

SPAWN_INVINCIBLE_FRAMES = 60

class Enemy(sprite.Sprite):
    def __init__(self, gameplay, x, y, img, type):
        super().__init__(x, y, img)

        self.gameplay = gameplay
        self.total_frames = 0
        self.type = type
        self.vel_x = 0
        self.vel_y = 0
        self.hp = 1
        self.frame = 0
        self.remove = False
        self.score = constants.ENEMY_SCORES[type]
        self.last_draw_x = 0
        self.invincible_frames = SPAWN_INVINCIBLE_FRAMES
        gameplay.enemies.append(self)

    def explode(self):
        explode_x = (self.x + 4 - self.gameplay.scroll_x) % self.gameplay.ground.width
        explode_x += self.gameplay.scroll_x
        self.gameplay.explosions.append(EnemyExplosion(explode_x, self.y + 4))
        play_sound("ENEMY_EXPLOSION")

    def _shoot_at_player(self, speed):
        EnemyBullet(self.gameplay, 
                    self.x + sprite.HALF_SIZE, 
                    self.y + sprite.HALF_SIZE,
                    speed)
        
    def destroy(self):
        self.invincible_frames = 0
        self.hp = 0
        self.visible = False
        self.remove = True
        self.explode()

    def _hit(self):
        self.hp = max(0, self.hp - 1)
        if self.hp == 0:
            self.destroy()
            self.gameplay.add_score(self.score)

    def _got_hit_check(self):
        if self.invincible_frames > 0:
            return

        for s in self.gameplay.lasers:
            if s.hit_rect_check(self.x, self.y, sprite.SIZE, sprite.SIZE):
                s.remove = True
                self._hit()
                break

    def _move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def _update_invincible_frames(self):
        if self.invincible_frames > 0:
            self.invincible_frames -= 1
            if self.invincible_frames == 0:
                self.visible = True
            else:
                if self.total_frames % 5 == 0:
                    self.visible = not self.visible

    def update(self):
        self.total_frames += 1
        self._move()
        self._update_invincible_frames()
        self._got_hit_check()

    def draw(self, scroll_x, ground_w):
        if not self.visible:
            return
        
        # Fix to ensure sprites within -8 pixels left of scroll_x get partially drawn.
        self.last_draw_x = self.x - (scroll_x % ground_w)
        if self.last_draw_x <= -sprite.SIZE or self.last_draw_x > 0:
            self.last_draw_x = (self.x - scroll_x) % ground_w

        if self.last_draw_x <= -sprite.SIZE or self.last_draw_x >= pyxel.width:
          return

        w = -sprite.SIZE if self.flip_x else sprite.SIZE
        h = -sprite.SIZE if self.flip_y else sprite.SIZE
        pyxel.blt(self.last_draw_x, self.y, self.img, 0, 0, w, h, pyxel.COLOR_BLACK)

        #pyxel.text(self.last_draw_x, self.y - 8, f"x: {pyxel.floor(self.x)}", 7)
