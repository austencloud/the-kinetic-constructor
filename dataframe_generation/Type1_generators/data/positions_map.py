from data.Enums import Location, SpecificPosition
from data.constants import *
from typing import Dict, Tuple

positions_map: Dict[
    Tuple[Location, Location], SpecificPosition
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

