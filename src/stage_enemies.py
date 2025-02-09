
# Note: Mutants and Swarmers are created by other
# enemies and do not need to be created at a spawn.
# They are part of this list for completeness.

# [ redeye, bomber, lander, mutant, pod, swarmer ]
SPAWNS = (
    # STAGE 1
    (
        8, 0, 0, 0, 0, 0,
    ),
    # STAGE 2
    (
        4, 4, 0, 0, 0, 0,
    ),
    # STAGE 3
    (
        0, 4, 4, 0, 0, 0,
    ),
    # STAGE 4
    (
        3, 2, 3, 0, 0, 0,
    ),
    # STAGE 5
    (
        0, 0, 4, 0, 4, 0,
    ),
    # STAGE 6
    (
        2, 0, 3, 0, 3, 0,
    ),
    # STAGE 7
    (
        2, 2, 2, 0, 2, 0,
    ),
    # STAGE 8
    (
        2, 2, 2, 0, 2, 0,
    ),
)

# [ redeye, bomber, lander, mutant, pod, swarmer ]
MAX_PER_SPAWN = (
    # STAGE 1
    (
        16, 0, 0, 0, 0, 0,
    ),
    # STAGE 2
    (
        10, 10, 0, 0, 0, 0,
    ),
    # STAGE 3
    (
        0, 12, 12, 0, 0, 0,
    ),
    # STAGE 4
    (
        10, 0, 10, 0, 8, 0,
    ),
    # STAGE 5
    (
        0, 0, 16, 0, 16, 0,
    ),
    # STAGE 6
    (
        14, 0, 12, 0, 12, 0,
    ),
    # STAGE 7
    (
        12, 10, 10, 0, 10, 0,
    ),
    # STAGE 8
    (
        12, 11, 12, 0, 11, 0,
    ),
)

MAX_ACTIVE_ENEMIES = (
    8, 10, 10, 12, 14, 16, 18, 20
)
