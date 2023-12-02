from settings.string_constants import *

positions_map = {
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
