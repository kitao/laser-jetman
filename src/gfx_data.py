import pyxel

# Add new sprite string lists to bottom.

JETMAN_SPRITE_IDLE = [
    "00777700",
    "77711100",
    "77711100",
    "77777700",
    "77777777",
    "00777000",
    "00700700",
    "00700700"
]

JETMAN_SPRITE_WALK = [
    "00777700",
    "77711100",
    "77711100",
    "77777700",
    "77777777",
    "00077700",
    "00077000",
    "00077000"
]

HUMAN_1 = [
    "00011000",
    "00144100",
    "001EE100",
    "071EE170",
    "00733700",
    "00033000",
    "00077000",
    "00077000",
    "00088000"
]

HUMAN_2 = [
    "00011000",
    "00144100",
    "001EE100",
    "001EE100",
    "07733770",
    "00033000",
    "00077000",
    "00077000",
    "00088000"
]

EN_REDEYE = [
    "003AA300",
    "03318810",
    "0AA88780",
    "0AA88880",
    "03318810",
    "00333300",
    "0A0AA0A0",
    "03000030"
]

EN_BOMBER = [
    "0000BB00",
    "000333B0",
    "15533315",
    "00113187",
    "00113188",
    "15533311",
    "00053350",
    "00005500"
]

EN_LANDER = [
    "01111110",
    "15888851",
    "58111185",
    "51888815",
    "21877812",
    "02277220",
    "02000020",
    "0A0000A0"
]

EN_MUTANT = [
    "0BB00BB0",
    "BBBBBBBB",
    "88B33B88",
    "78333387",
    "11311311",
    "00133100",
    "00311300",
    "00011000"
]

EN_POD = [
    "00088000",
    "08011080",
    "00211200",
    "81172118",
    "81122118",
    "00211200",
    "08011080",
    "00088000"
]

EN_SWARMER = [
    "00000000",
    "000EE000",
    "00EEEE00",
    "0E8EE8E0",
    "EE8EE8EE",
    "05EEEE50",
    "00555500",
    "00000000"
]

ICON_SHIELD = [
    "00C77C00",
    "0C0000C0",
    "C066660C",
    "C070000C",
    "50777705",
    "50000705",
    "05666650",
    "00555500"
]

TITLE_LETTER_L = (
    "00000000",
    "80000000",
    "80000000",
    "80000000",
    "80000000",
    "80000000",
    "08000000",
    "00888888"
)

TITLE_LETTER_A = (
    "00000000",
    "00888000",
    "08000800",
    "80000080",
    "80888080",
    "80000080",
    "80000080",
    "80000080"
)

TITLE_LETTER_S = (
    "00000000",
    "08888880",
    "80000000",
    "80000000",
    "08888800",
    "00000080",
    "00000080",
    "88888800"
)

TITLE_LETTER_E = (
    "00000000",
    "00888880",
    "08000000",
    "80000000",
    "80888000",
    "80000000",
    "08000000",
    "00888880"
)

TITLE_LETTER_R = (
    "00000000",
    "88888800",
    "00000080",
    "00000080",
    "08888800",
    "80000000",
    "80000800",
    "80000080"
)

TITLE_LETTER_J = (
    "00000000",
    "00000080",
    "00000080",
    "00000080",
    "00000080",
    "00000080",
    "00000800",
    "88888000"
)

TITLE_LETTER_T = (
    "00000000",
    "88808880",
    "00080000",
    "00080000",
    "00080000",
    "00080000",
    "00080000",
    "00080000"
)

TITLE_LETTER_M = (
    "00000000",
    "00888000",
    "08000800",
    "80080080",
    "80080080",
    "80080080",
    "80000080",
    "80000080"
)

TITLE_LETTER_N = (
    "00000000",
    "00888000",
    "08000800",
    "80000080",
    "80000080",
    "80000080",
    "80000080",
    "80000080"
)

# Add new sprite string lists above here.

ANIMS = {}

def _make_anim(name, frames):
    anim = []
    for data in frames:
        img = pyxel.Image(8, 8)
        img.set(0, 0, data)
        anim.append(img)
    ANIMS[name] = anim

def make_all():
    _make_anim("jetman_idle", [JETMAN_SPRITE_IDLE])
    _make_anim("jetman_walk", [JETMAN_SPRITE_IDLE, JETMAN_SPRITE_WALK])
    _make_anim("human", [HUMAN_1, HUMAN_2])
    _make_anim("redeye", [EN_REDEYE])
    _make_anim("bomber", [EN_BOMBER])
    _make_anim("lander", [EN_LANDER])
    _make_anim("mutant", [EN_MUTANT])
    _make_anim("icon_shield", [ICON_SHIELD])
    _make_anim("pod", [EN_POD])
    _make_anim("swarmer", [EN_SWARMER])
    _make_anim("title_letter_l", [TITLE_LETTER_L])
    _make_anim("title_letter_a", [TITLE_LETTER_A])
    _make_anim("title_letter_s", [TITLE_LETTER_S])
    _make_anim("title_letter_e", [TITLE_LETTER_E])
    _make_anim("title_letter_r", [TITLE_LETTER_R])
    _make_anim("title_letter_j", [TITLE_LETTER_J])
    _make_anim("title_letter_t", [TITLE_LETTER_T])
    _make_anim("title_letter_m", [TITLE_LETTER_M])
    _make_anim("title_letter_n", [TITLE_LETTER_N])