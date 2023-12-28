from Enums import Location, MotionType, PropRotationDirection
from constants import *
from utilities.TypeChecking.TypeChecking import (
    StartEndLocationTuple,
)


start_end_location_map = {
    NORTHEAST: {
        CLOCKWISE: {
            ANTI: (EAST, NORTH),
            PRO: (NORTH, EAST),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (NORTH, EAST),
            PRO: (EAST, NORTH),
        },
    },
    NORTHWEST: {
        CLOCKWISE: {
            ANTI: (NORTH, WEST),
            PRO: (WEST, NORTH),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (WEST, NORTH),
            PRO: (NORTH, WEST),
        },
    },
    SOUTHEAST: {
        CLOCKWISE: {
            ANTI: (SOUTH, EAST),
            PRO: (EAST, SOUTH),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (EAST, SOUTH),
            PRO: (SOUTH, EAST),
        },
    },
    SOUTHWEST: {
        CLOCKWISE: {
            ANTI: (WEST, SOUTH),
            PRO: (SOUTH, WEST),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (SOUTH, WEST),
            PRO: (WEST, SOUTH),
        },
    },
}


def get_start_end_locations(
    motion_type: MotionType,
    rot_dir: PropRotationDirection,
    arrow_location: Location,
) -> StartEndLocationTuple:
    """
    Get the start and end locations for the arrow based on the motion type,
    rotation direction, and arrow location.

    Args:
        motion_type (MotionType): The type of motion for the arrow.
        rot_dir (PropRotationDirection): The direction of rotation for the arrow.
        arrow_location (Location): The location of the arrow.

    Returns:
        StartEndLocationTuple: A tuple containing the start and end locations for the arrow.
    """
    return (
        start_end_location_map.get(arrow_location, {})
        .get(rot_dir, {})
        .get(motion_type, (None, None))
    )
