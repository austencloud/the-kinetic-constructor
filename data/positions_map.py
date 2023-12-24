from Enums import Color, Location, PictographAttribute, SpecificPosition
from objects.motion import Motion
from constants.string_constants import *
from utilities.TypeChecking.TypeChecking import (
    Dict,
    SpecificStartEndPositionsDicts,
    Tuple,
)

positions_map: Dict[Tuple[Location, Color, Location, Color], SpecificPosition] = {
    (NORTH, RED, SOUTH, BLUE): ALPHA1,
    (EAST, RED, WEST, BLUE): ALPHA2,
    (SOUTH, RED, NORTH, BLUE): ALPHA3,
    (WEST, RED, EAST, BLUE): ALPHA4,
    (NORTH, RED, NORTH, BLUE): BETA1,
    (EAST, RED, EAST, BLUE): BETA2,
    (SOUTH, RED, SOUTH, BLUE): BETA3,
    (WEST, RED, WEST, BLUE): BETA4,
    (NORTH, RED, WEST, BLUE): GAMMA1,
    (EAST, RED, NORTH, BLUE): GAMMA2,
    (SOUTH, RED, EAST, BLUE): GAMMA3,
    (WEST, RED, SOUTH, BLUE): GAMMA4,
    (NORTH, RED, EAST, BLUE): GAMMA5,
    (EAST, RED, SOUTH, BLUE): GAMMA6,
    (SOUTH, RED, WEST, BLUE): GAMMA7,
    (WEST, RED, NORTH, BLUE): GAMMA8,
}


def get_specific_start_end_positions(
    red_motion: Motion, blue_motion: Motion
) -> SpecificStartEndPositionsDicts:
    if red_motion and blue_motion:
        start_locations = (
            red_motion.start_location,
            RED,
            blue_motion.start_location,
            BLUE,
        )
        end_locations = (
            red_motion.end_location,
            RED,
            blue_motion.end_location,
            BLUE,
        )

        specific_positions: SpecificStartEndPositionsDicts = {
            PictographAttribute.START_POSITION: positions_map.get(start_locations),
            PictographAttribute.END_POSITION: positions_map.get(end_locations),
        }

        return specific_positions
