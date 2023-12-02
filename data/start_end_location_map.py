from settings.string_constants import (
    NORTHEAST,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ANTI,
    PRO,
    NORTH,
    EAST,
    SOUTH,
    WEST,
)
from utilities.TypeChecking.TypeChecking import (
    Locations,
    MotionTypes,
    RotationDirections,
    StartEndLocationsTuple,
)


start_end_location_map = {
    NORTHEAST: {
        CLOCKWISE: {ANTI: (EAST, NORTH), PRO: (NORTH, EAST)},
        COUNTER_CLOCKWISE: {ANTI: (NORTH, EAST), PRO: (EAST, NORTH)},
    },
    NORTHWEST: {
        CLOCKWISE: {ANTI: (NORTH, WEST), PRO: (WEST, NORTH)},
        COUNTER_CLOCKWISE: {ANTI: (WEST, NORTH), PRO: (NORTH, WEST)},
    },
    SOUTHEAST: {
        CLOCKWISE: {ANTI: (SOUTH, EAST), PRO: (EAST, SOUTH)},
        COUNTER_CLOCKWISE: {ANTI: (EAST, SOUTH), PRO: (SOUTH, EAST)},
    },
    SOUTHWEST: {
        CLOCKWISE: {ANTI: (WEST, SOUTH), PRO: (SOUTH, WEST)},
        COUNTER_CLOCKWISE: {ANTI: (SOUTH, WEST), PRO: (WEST, SOUTH)},
    },
}


def get_start_end_locations(
    motion_type: MotionTypes,
    rotation_direction: RotationDirections,
    arrow_location: Locations,
) -> StartEndLocationsTuple:
    """
    Get the start and end locations for the arrow based on the motion type,
    rotation direction, and arrow location.

    Args:
        motion_type (MotionTypes): The type of motion for the arrow.
        rotation_direction (RotationDirections): The direction of rotation for the arrow.
        arrow_location (Locations): The location of the arrow.

    Returns:
        StartEndLocationsTuple: A tuple containing the start and end locations for the arrow.
    """
    return (
        start_end_location_map.get(arrow_location, {})
        .get(rotation_direction, {})
        .get(motion_type, (None, None))
    )
