ARROW_DIR = "resources/images/arrows/"
PROP_DIR = "resources/images/props/"
LETTER_SVG_DIR = "resources/images/letters/"
ICON_DIR = "resources/images/icons/"

SVG_NS = "http://www.w3.org/2000/svg"

GRID_FILE_PATH = "resources/images/grid/grid.svg"
STAFF_SVG_FILE_PATH = "resources/images/props/staff.svg"
CLUB_SVG_FILE_PATH = "resources/images/props/club.svg"
BUUGENG_SVG_FILE_PATH = "resources/images/props/buugeng.svg"
FAN_SVG_FILE_PATH = "resources/images/props/fan.svg"
TRIAD_SVG_FILE_PATH = "resources/images/props/triad.svg"
HOOP_SVG_FILE_PATH = "resources/images/props/hoop.svg"

BLUE = "blue"
RED = "red"
RED_HEX = "#ED1C24"
BLUE_HEX = "#2E3192"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

PRO = "pro"
ANTI = "anti"
DASH = "dash"
STATIC = "static"

COLOR = "color"
MOTION_TYPE = "motion_type"
ROTATION_DIRECTION = "rotation_direction"
location = "location"
START_LOCATION = "start_location"
END_LOCATION = "end_location"
TURNS = "turns"

START_ORIENTATION = "start_orientation"
END_ORIENTATION = "end_orientation"

START_LAYER = "start_layer"
END_LAYER = "end_layer"

CLOCKWISE = "cw" or "CW"
COUNTER_CLOCKWISE = "ccw" or "CCW"

START_POS = "start_position"
END_POS = "end_position"

PROP_TYPE = "prop_type"
LOCATION = "location"
LAYER = "layer"
AXIS = "axis"
ORIENTATION = "orientation"

IN = "in"
OUT = "out"

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

PROP = "prop"
STAFF = "staff"
CLUB = "club"
BUUGENG = "buugeng"
FAN = "fan"
TRIAD = "triad"
HOOP = "hoop"

COLOR_MAP = {RED: RED_HEX, BLUE: BLUE_HEX}

### ICONS ###

CLOCK_DIR = ICON_DIR + "clock/"
CLOCKWISE_ICON = CLOCK_DIR + "clockwise.png"
COUNTER_CLOCKWISE_ICON = CLOCK_DIR + "counter_clockwise.png"
CLOCK_ICON = CLOCK_DIR + "clock.png"
SWAP_ICON = "swap.jpg"
MIRROR_ICON = "mirror.png"
DECREMENT_TURNS_ICON = "subtract_turns.png"
INCREMENT_TURNS_ICON = "add_turns.png"
SWAP_COLORS_ICON = "swap_colors.png"

ICON_PATHS = {
    "swap_motion_type": ICON_DIR + SWAP_ICON,
    "swap_start_end": ICON_DIR + MIRROR_ICON,
    "subtract_turns": ICON_DIR + DECREMENT_TURNS_ICON,
    "add_turns": ICON_DIR + INCREMENT_TURNS_ICON,
    "swap_colors": ICON_DIR + SWAP_COLORS_ICON,
    "clockwise": CLOCKWISE_ICON,
    "counter_clockwise": COUNTER_CLOCKWISE_ICON,
}

ARROW_ATTRIBUTES = [
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    location,
    START_LOCATION,
    END_LOCATION,
    TURNS,
]

STAFF_ATTRIBUTES = [
    COLOR,
    LOCATION,
    LAYER,
]
