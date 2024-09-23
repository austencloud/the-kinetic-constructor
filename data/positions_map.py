from objects.motion.motion import Motion
from data.constants import *
from Enums.MotionAttributes import Location
from Enums.Enums import SpecificPosition

positions_map: dict[tuple[Location], str] = {
    (SOUTH, NORTH): "alpha1",
    (WEST, EAST): "alpha2",
    (NORTH, SOUTH): "alpha3",
    (EAST, WEST): "alpha4",
    (NORTH, NORTH): "beta1",
    (EAST, EAST): "beta2",
    (SOUTH, SOUTH): "beta3",
    (WEST, WEST): "beta4",
    (WEST, NORTH): "gamma1",
    (NORTH, EAST): "gamma2",
    (EAST, SOUTH): "gamma3",
    (SOUTH, WEST): "gamma4",
    (EAST, NORTH): "gamma5",
    (SOUTH, EAST): "gamma6",
    (WEST, SOUTH): "gamma7",
    (NORTH, WEST): "gamma8",
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
