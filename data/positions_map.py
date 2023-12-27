from Enums import Color, Location, SpecificPosition
from objects.motion import Motion
from constants import *
from utilities.TypeChecking.TypeChecking import (
    Dict,
    SpecificStartEndPositionsDicts,
    Tuple,
)

positions_map: Dict[
    Tuple[Location, Color], Tuple[Location, Color], SpecificPosition
] = {
    # (blue_loc, red_loc): position
    (SOUTH, NORTH): ALPHA1,
    (WEST, EAST): ALPHA2,
    (NORTH, SOUTH): ALPHA3,
    (EAST, WEST): ALPHA4,
    (NORTH, NORTH): BETA1,
    (EAST, EAST): BETA2,
    (SOUTH, SOUTH): BETA3,
    (WEST, WEST): BETA4,
    (WEST, NORTH): GAMMA1,
    (NORTH, EAST): GAMMA2,
    (EAST, SOUTH): GAMMA3,
    (SOUTH, WEST): GAMMA4,
    (EAST, NORTH): GAMMA5,
    (SOUTH, EAST): GAMMA6,
    (WEST, SOUTH): GAMMA7,
    (NORTH, WEST): GAMMA8,
}

def get_specific_start_end_positions(
    blue_motion: Motion, red_motion: Motion
) -> SpecificStartEndPositionsDicts:
    start_locations = (
        blue_motion.start_location,
        red_motion.start_location,
    )
    end_locations = (
        red_motion.end_location,
        blue_motion.end_location,
    )

    specific_positions: SpecificStartEndPositionsDicts = {
        START_POSITION: positions_map.get(start_locations),
        END_POSITION: positions_map.get(end_locations),
    }
    return specific_positions
