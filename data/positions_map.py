from objects.motion.motion import Motion
from data.constants import *
from Enums.MotionAttributes import Location
from Enums.Enums import SpecificPosition


positions_map: dict[tuple[Location], str    ] = {
    (SOUTH, NORTH): "alpha1",
    (SOUTHWEST, NORTHEAST): "alpha2",
    (WEST, EAST): "alpha3",
    (NORTHWEST, SOUTHEAST): "alpha4",
    (NORTH, SOUTH): "alpha5",
    (NORTHEAST, SOUTHWEST): "alpha6",
    (EAST, WEST): "alpha7",
    (SOUTHEAST, NORTHWEST): "alpha8",
    (NORTH, NORTH): "beta1",
    (NORTHEAST, NORTHEAST): "beta2",
    (EAST, EAST): "beta3",
    (SOUTHEAST, SOUTHEAST): "beta4",
    (SOUTH, SOUTH): "beta5",
    (SOUTHWEST, SOUTHWEST): "beta6",
    (WEST, WEST): "beta7",
    (NORTHWEST, NORTHWEST): "beta8",
    (WEST, NORTH): "gamma1",
    (NORTHWEST, NORTHEAST): "gamma2",
    (NORTH, EAST): "gamma3",
    (NORTHEAST, SOUTHEAST): "gamma4",
    (EAST, SOUTH): "gamma5",
    (SOUTHEAST, SOUTHWEST): "gamma6",
    (SOUTH, WEST): "gamma7",
    (SOUTHWEST, NORTHWEST): "gamma8",
    (EAST, NORTH): "gamma9",
    (SOUTHEAST, NORTHEAST): "gamma10",
    (SOUTH, EAST): "gamma11",
    (SOUTHWEST, SOUTHEAST): "gamma12",
    (WEST, SOUTH): "gamma13",
    (NORTHWEST, SOUTHWEST): "gamma14",
    (NORTH, WEST): "gamma15",
    (NORTHEAST, NORTHWEST): "gamma16",
}

# As you can see, alpha1 became alpha1 (staying the same). alpha2 became alpha3, alpha3 became alpha5, alpha4 became alpha7. 
# beta1 became beta1 (staying the same). beta2 became beta3, beta3 became beta5, beta4 became beta7.
# gamma1 became gamma1 (staying the same). gamma2 became gamma3, gamma3 became gamma5, gamma4 became gamma7. gamma5 became gamma9, gamma6 became gamma11, gamma7 became gamma13, gamma8 became gamma15. 

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
