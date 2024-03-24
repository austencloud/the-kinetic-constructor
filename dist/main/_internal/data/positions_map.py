from objects.motion.motion import Motion
from constants import *
from Enums.MotionAttributes import Location
from Enums.Enums import SpecificPosition

positions_map: dict[tuple[Location], SpecificPosition] = {
    (SOUTH, NORTH): SpecificPosition.ALPHA1,
    (WEST, EAST): SpecificPosition.ALPHA2,
    (NORTH, SOUTH): SpecificPosition.ALPHA3,
    (EAST, WEST): SpecificPosition.ALPHA4,
    (NORTH, NORTH): SpecificPosition.BETA1,
    (EAST, EAST): SpecificPosition.BETA2,
    (SOUTH, SOUTH): SpecificPosition.BETA3,
    (WEST, WEST): SpecificPosition.BETA4,
    (WEST, NORTH): SpecificPosition.GAMMA1,
    (NORTH, EAST): SpecificPosition.GAMMA2,
    (EAST, SOUTH): SpecificPosition.GAMMA3,
    (SOUTH, WEST): SpecificPosition.GAMMA4,
    (EAST, NORTH): SpecificPosition.GAMMA5,
    (SOUTH, EAST): SpecificPosition.GAMMA6,
    (WEST, SOUTH): SpecificPosition.GAMMA7,
    (NORTH, WEST): SpecificPosition.GAMMA8,
}


def get_specific_start_end_pos(
    blue_motion: Motion, red_motion: Motion
) -> dict[str, SpecificPosition]:
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
