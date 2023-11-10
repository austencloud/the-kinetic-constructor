ARROW_DIR = "resources/images/arrows/"
STAFF_DIR = "resources/images/props/"
LETTER_SVG_DIR = "resources/images/letters/"
ICON_DIR = "resources/images/icons/"

GRID_FILE_PATH = "resources/images/grid/grid.svg"
STAFF_SVG_FILE_PATH = "resources/images/props/staff.svg"

BLUE = "blue"
RED = "red"
RED_HEX = "#ED1C24"
BLUE_HEX = "#2E3192"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

STATIC = "static"
PRO = "pro"
ANTI = "anti"

COLOR = "color"
MOTION_TYPE = "motion_type"
ROTATION_DIRECTION = "rotation_direction"
QUADRANT = "quadrant"
START_LOCATION = "start_location"
END_LOCATION = "end_location"
TURNS = "turns"


CLOCKWISE = "r"
COUNTER_CLOCKWISE = "l"

START_POS = "start_position"
END_POS = "end_position"

LOCATION = "location"
LAYER = "layer"

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
NORTH = "n"
SOUTH = "s"
EAST = "e"
WEST = "w"

NORTHWEST = "nw"
NORTHEAST = "ne"
SOUTHWEST = "sw"
SOUTHEAST = "se"

ARROWS = "arrows"
STAFFS = "staffs"

COLOR_MAP = {RED: RED_HEX, BLUE: BLUE_HEX}

### ICONS ###

CLOCK_DIR = ICON_DIR + "clock/"
CLOCKWISE_ICON = CLOCK_DIR + "clockwise.png"
COUNTER_CLOCKWISE_ICON = CLOCK_DIR + "counter_clockwise.png"
CLOCK_ICON = CLOCK_DIR + "clock.png"

SWAP_ICON = "swap.png"


ARROW_ATTRIBUTES = [
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    TURNS,
]

STAFF_ATTRIBUTES = [
    COLOR,
    LOCATION,
    LAYER,
]
