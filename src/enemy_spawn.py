import random
import pyxel
from en_redeye import EnRedeye
from en_bomber import EnBomber
from en_lander import EnLander
from en_mutant import EnMutant
from en_pod import EnPod
from en_swarmer import EnSwarmer
import en_lander
import constants
from stage_enemies import SPAWNS, MAX_PER_SPAWN, MAX_ACTIVE_ENEMIES
from utils import lerp

MIN_NEXT_SPAWN_FRAMES = 120
MAX_ADD_NEXT_SPAWN_FRAMES = 180

SPAWN_ANIM_FRAMES = 45

SPAWN_RADIUS = 8
COL = [ 7, 6, 5, 1, 0 ]

class EnemySpawn:
    def __init__(self, gameplay, x, y, enemy_type, spawn_max):
        self.gameplay = gameplay

        self.x = x
        self.y = y
        self.enemy_type = enemy_type # only need one spawn per enemy type.
        self.spawn_max = spawn_max
        self.spawned_cnt = 0
        self.next_spawn_frames = pyxel.rndi(0, MIN_NEXT_SPAWN_FRAMES)
        self.just_spawned_frames = 0

        self.gameplay.enemy_spawns.append(self)

    def _spawn_next(self):
        self.next_spawn_frames = MIN_NEXT_SPAWN_FRAMES + \
            pyxel.rndi(0, MAX_ADD_NEXT_SPAWN_FRAMES)
        self.just_spawned_frames = SPAWN_ANIM_FRAMES
        if self.enemy_type == constants.ENEMY_TYPE_REDEYE:
            EnRedeye(self.gameplay, self.x, self.y)
        elif self.enemy_type == constants.ENEMY_TYPE_BOMBER:
            EnBomber(self.gameplay, self.x, self.y)
        elif self.enemy_type == constants.ENEMY_TYPE_LANDER:
            EnLander(self.gameplay, self.x, self.y)
        elif self.enemy_type == constants.ENEMY_TYPE_MUTANT:
            EnMutant(self.gameplay, self.x, self.y)
        elif self.enemy_type == constants.ENEMY_TYPE_POD:
            EnPod(self.gameplay, self.x, self.y)
        elif self.enemy_type == constants.ENEMY_TYPE_SWARMER:
            EnSwarmer(self.gameplay, self.x, self.y)
        self.spawned_cnt += 1

    def update(self):
        if self.next_spawn_frames == 0:
            if self.spawned_cnt < self.spawn_max:
                if len(self.gameplay.enemies) < MAX_ACTIVE_ENEMIES[self.gameplay.stage_num]:
                    self._spawn_next()

        self.next_spawn_frames = max(0, self.next_spawn_frames - 1)
        self.just_spawned_frames = max(0, self.just_spawned_frames - 1)

    def draw(self, scroll_x, ground_w):
        if self.just_spawned_frames <= 0:
            return
        
        draw_x = self.x - (scroll_x % ground_w)
        if draw_x <= -8 or draw_x > 0:
            draw_x = (self.x - scroll_x) % ground_w

        if draw_x <= -8 or draw_x >= pyxel.width:
          return
        
        progress = 1 - (self.just_spawned_frames / SPAWN_ANIM_FRAMES)
        r = lerp(SPAWN_RADIUS, 0, progress)
        col = pyxel.floor(lerp(0, len(COL)-1, progress))
        pyxel.circ(draw_x, self.y, r, COL[col])

# [ redeye, bomber, lander, mutant, pod, swarmer ]
MIN_Y = (
    40, 40, en_lander.RESET_HEIGHT, 40, 40, 40
)
ADD_RANDOM_Y = (
    16, 16, 0, 16, 16, 16
)

def create_all(gameplay):
    spawn_types_needed = []
    for t in range(constants.ENEMY_TYPE_MAX):
        qty = SPAWNS[gameplay.stage_num][t]
        for _ in range(qty):
            spawn_types_needed.append(t)
    random.shuffle(spawn_types_needed)

    ground = gameplay.ground
    step_width = ground.width // len(spawn_types_needed)
    x = pyxel.rndi(0, 128)
    spawn_x = []
    for _ in range(len(spawn_types_needed)):
        spawn_x.append(x)
        x += step_width
        if step_width >= ground.width:
            x -= ground.width
    random.shuffle(spawn_x)

    for i, t in enumerate(spawn_types_needed):
        EnemySpawn(gameplay, 
                   spawn_x[i], 
                   MIN_Y[t] + (pyxel.rndi(-ADD_RANDOM_Y[t], ADD_RANDOM_Y[t])), 
                   t, MAX_PER_SPAWN[gameplay.stage_num][t])