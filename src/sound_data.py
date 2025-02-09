import pyxel

_data = {
    
# note: [cdefgab] + [ #-] + [0-4] or [r]
# tone: [t]riangle [s]quare [p]ulse [n]oise
# volume: [0-7]
# effect: [n]one [s]lide [v]ibrato [f]adeout

    # In-Game Effects Channel 0

    "STAGE_RESPAWN" : {
        "channel": 0,
        "notes" : "c0 c1 c2 c3 c4",
        "tones" : "n",
        "volumes" : "1 2 2 3 4",
        "effects" : "s",
        "speed" : 32
    },
    "STAGE_COMPLETE" : {
        "channel": 0,
        "notes" : "f4e4d4c4 f3e3d3c3 f2e2d2c2 f1e1d1c1",
        "tones" : "snsnsnsn snsnsnsn snsnsnsn snsnsnsn",
        "volumes" : "1111 2222 3333 4444",
        "effects" : "svsvsvsv svsvsvsv svsvsvsv svsvsvsv",
        "speed" : 8
    },
    "LASER" : {
        "channel": 0,
        "notes" : "c4c4 c3c3 c2c2 c1c1 c0c0",
        "tones" : "t",
        "volumes" : "22222 11111",
        "effects" : "s",
        "speed" : 3
    },
    "PLAYER_EXPLOSION" : {
        "channel": 0,
        "notes" : "c4d4e3f3 g3a3b2c2 d2e1f1g1 a1b0c0d0",
        "tones" : "n",
        "volumes" : "4444 3333 2222 1111",
        "effects" : "",
        "speed" : 12
    },
    "RESCUE_BEAM_UP" : {
        "channel": 0,
        "notes" : "c4 c3 c4 c3",
        "tones" : "t",
        "volumes" : "2",
        "effects" : "s",
        "speed" : 4
    },

    # In-Game Effects Channel 1

    "PLAYER_LANDS" : {
        "channel": 1,
        "notes" : "c4d4e3f3",
        "tones" : "n",
        "volumes" : "3",
        "effects" : "",
        "speed" : 2
    },
    "JETPACK_FIRE" : {
        "channel": 1,
        "notes" : "c2",
        "tones" : "n",
        "volumes" : "1",
        "effects" : "",
        "speed" : 2
    },

    # In-Game Effects Channel 2

    "ENEMY_EXPLOSION" : {
        "channel": 2,
        "notes" : "c4d4e3f3 g3a3b2c2 d2e1f1g1 a1b0c0d0",
        "tones" : "n",
        "volumes" : "4444 3333 2222 1111",
        "effects" : "",
        "speed" : 4
    },
    "GOT_SHIELD" : {
        "channel": 2,
        "notes" : "c1c1 c2c2 c3c3 c4c4",
        "tones" : "s",
        "volumes" : "5",
        "effects" : "s",
        "speed" : 3
    },

    # In-Game Effects Channel 3

    "ENEMY_BEAM_UP" : {
        "channel": 3,
        "notes" : "c4 c3 c4 c3",
        "tones" : "p",
        "volumes" : "2",
        "effects" : "s",
        "speed" : 32
    },

    # Music

    "GAME_COMPLETE_DRUMS" : {
        "channel": 0,
        "notes" : 
            "c2c2a#4r c2c2a#4r c2c2a#4r c2c2a#4a#4" 
            "c2c2a#4r c2c2a#4r c2c2a#4r c2c2a#4a#4"
            "c2c2a#4r c2c2a#4r c2c2a#4r c2c2a#4a#4"
            "c2c2a#4r c2c2a#4r a#4a#4a#4a#4 a#4a#4a#4a#4"
            ,
        "tones" : "n",
        "volumes" : "2",
        "effects" : "fffn fffn fffn ffff",
        "speed" : 25
    },
    "GAME_COMPLETE_MELODY" : {
        "channel": 1,
        "notes" : 
            "c2c1a1b1 c1d1e1e1 f1f1g1g1 e1e1f1g1"
            "c2c1a1b1 c1d1e1e1 f1f1g1g1 e1e1f1g1"
            "c2c1a1b1 c1d1e1e1 f1f1g1g1 e1e1f1g1"
            "c2c1a1b1 c1d1e1e1 f1f1g1g1 e1e1f1g1"
            "c2ra1r c1re1r f1f1g1g1 c1c1f1g1"
            "a2c1a1b1 a2d1e1e1 a2f1g1g1 a2b2f1g1"
            "c2ra1r c1re1r f1f1g1g1 c1c1f1g1"
            "a2c1a1b1 a2d1e1e1 a2f1g1g1 a2b2f1g1"
            ,
        "tones" : "s",
        "volumes" : "6",
        "effects" : "v",
        "speed" : 25
    },
}

# LASER = {
#     "notes" : "",
#     "tones" : "",
#     "volumes" : "",
#     "effects" : "",
#     "speed" : 1
# }

SOUNDS = {}

def _add_sound(name):
    num_sounds = len(SOUNDS)
    if num_sounds >= pyxel.NUM_SOUNDS:
        return
    
    d = _data.get(name)
    if d is None:
        return
    
    SOUNDS[name] = {
        "channel" : d.get("channel", 0),
        "index" : num_sounds
    }
    pyxel.sounds[num_sounds].set(
        d.get("notes", ""),
        d.get("tones", ""),
        d.get("volumes", ""),
        d.get("effects", ""),
        d.get("speed", 1)
    )

def add_all():
    for name in _data:
        _add_sound(name)
    # for k, v in _data.items():
    #     print(k)
    #     print(v)