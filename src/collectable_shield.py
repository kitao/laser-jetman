import pyxel
import collectable
from gfx_data import ANIMS
import lava

class CollectableShield(collectable.Collectable):
    def __init__(self, gameplay):
        super().__init__(gameplay, collectable.TYPE_SHIELD, 0, 8, ANIMS["icon_shield"][0])
        self.gameplay.shield_cnt += 1
        self.x = pyxel.rndi(0, self.gameplay.ground.width-1)
        self.y = 32 + pyxel.rndi(-8, 8)

    def collected(self):
        super().collected()
        self.gameplay.player.add_shield()
        self.gameplay.shield_cnt -= 1