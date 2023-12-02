from settings.string_constants import *

start_end_location_mapping = {
    NORTHEAST: {
        CLOCKWISE: {ANTI: (EAST, NORTH), PRO: (NORTH, EAST)},
        COUNTER_CLOCKWISE: {ANTI: (NORTH, EAST), PRO: (EAST, NORTH)}
    },
    NORTHWEST: {
        CLOCKWISE: {ANTI: (NORTH, WEST), PRO: (WEST, NORTH)},
        COUNTER_CLOCKWISE: {ANTI: (WEST, NORTH), PRO: (NORTH, WEST)}
    },
    SOUTHEAST: {
        CLOCKWISE: {ANTI: (SOUTH, EAST), PRO: (EAST, SOUTH)},
        COUNTER_CLOCKWISE: {ANTI: (EAST, SOUTH), PRO: (SOUTH, EAST)}
    },
    SOUTHWEST: {
        CLOCKWISE: {ANTI: (WEST, SOUTH), PRO: (SOUTH, WEST)},
        COUNTER_CLOCKWISE: {ANTI: (SOUTH, WEST), PRO: (WEST, SOUTH)}
    }
}
