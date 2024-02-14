from objects.motion.motion import Motion
from constants import *
from Enums.MotionAttributes import Locations
from Enums.Enums import SpecificPositions

positions_map: dict[tuple[Locations], SpecificPositions] = {
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


def get_specific_start_end_pos(
    blue_motion: Motion, red_motion: Motion
) -> dict[str, SpecificPositions]:
    start_locs = (
        blue_motion.start_loc,
        red_motion.start_loc,
    )
    end_locs = (
        red_motion.end_loc,
        blue_motion.end_loc,
    )

    specific_positions = {
        START_POS: positions_map.get(start_locs),
        END_POS: positions_map.get(end_locs),
    }
    return specific_positions
