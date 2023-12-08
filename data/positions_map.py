
from objects.motion import Motion
from settings.string_constants import *
from utilities.TypeChecking.TypeChecking import Colors, Locations, SpecificPositions, Dict, SpecificStartEndPositionsDicts, Tuple

positions_map: Dict[Tuple[Locations, Colors, Locations, Colors], SpecificPositions] = {
    (NORTH, RED, SOUTH, BLUE): 'alpha1',
    (EAST, RED, WEST, BLUE): 'alpha2',
    (SOUTH, RED, NORTH, BLUE): 'alpha3',
    (WEST, RED, EAST, BLUE): 'alpha4',
    
    (NORTH, RED, NORTH, BLUE): 'beta1',
    (EAST, RED, EAST, BLUE): 'beta2',
    (SOUTH, RED, SOUTH, BLUE): 'beta3',
    (WEST, RED, WEST, BLUE): 'beta4',
    
    (NORTH, RED, WEST, BLUE): 'gamma1',
    (EAST, RED, NORTH, BLUE): 'gamma2',
    (SOUTH, RED, EAST, BLUE): 'gamma3',
    (WEST, RED, SOUTH, BLUE): 'gamma4',
    (NORTH, RED, EAST, BLUE): 'gamma5',
    (EAST, RED, SOUTH, BLUE): 'gamma6',
    (SOUTH, RED, WEST, BLUE): 'gamma7',
    (WEST, RED, NORTH, BLUE): 'gamma8',
}


def get_specific_start_end_positions(red_motion:Motion, blue_motion:Motion) -> SpecificStartEndPositionsDicts:
    if red_motion and blue_motion:
        start_locations = (
            red_motion.start_location,
            "red",
            blue_motion.start_location,
            "blue",
        )
        end_locations = (
            red_motion.end_location,
            "red",
            blue_motion.end_location,
            "blue",
        )

        specific_positions: SpecificStartEndPositionsDicts = {
            "start_position": positions_map.get(start_locations),
            "end_position": positions_map.get(end_locations),
        }

        return specific_positions