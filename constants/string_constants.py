import os

current_script_path = os.path.abspath(__file__).replace("\\", "/")
current_script_path = current_script_path[0].upper() + current_script_path[1:]

current_dir = os.path.dirname(current_script_path)
tka_sequence_constructor_dir = os.path.dirname(current_dir)
tka_app_dir = os.path.dirname(tka_sequence_constructor_dir)
resources_path = tka_app_dir + "/resources"


PICTOGRAPH_DIR = "resources/images/pictographs/"
ARROW_DIR = "resources/images/arrows/"
PROP_DIR = "resources/images/props/"
LETTER_BTN_ICON_DIR = "resources/images/letter_button_icons"
LETTERS_TRIMMED_SVG_DIR = "resources/images/letters_trimmed/"
ICON_DIR = "resources/images/icons/"
GRID_DIR = "resources/images/grid/"
LETTER_JSON_DIR = "resources/json/"

SVG_NS = "http://www.w3.org/2000/svg"

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
FLOAT = "float"
DASH = "dash"
STATIC = "static"

COLOR = "color"
MOTION_TYPE = "motion_type"
ROTATION_DIRECTION = "rotation_direction"
TURNS = "turns"

DIAMOND = "diamond"
BOX = "box"

LOCATION = "location"
ARROW_LOCATION = "arrow_location"
START_LOCATION = "start_location"
END_LOCATION = "end_location"

START_POSITION = "start_position"
END_POSITION = "end_position"

START_ORIENTATION = "start_orientation"
END_ORIENTATION = "end_orientation"

CLOCKWISE = "cw"
COUNTER_CLOCKWISE = "ccw"



START_POS = "start_position"
END_POS = "end_position"

PROP_TYPE = "prop_type"
AXIS = "axis"
ORIENTATION = "orientation"

IN = "in"
OUT = "out"
CLOCK = "clock"
COUNTER = "counter"
CLOCK_IN = "clock-in"
CLOCK_OUT = "clock-out"
COUNTER_IN = "counter-in"
COUNTER_OUT = "counter-out"


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


ARROW = "arrow"
PROP = "prop"

GHOST_ARROW = "ghostarrow"
GHOST_PROP = "ghostprop"

RADIAL = "radial"
ANTIRADIAL = "antiradial"

STAFF = "staff"
BIGSTAFF = "bigstaff"
CLUB = "club"
BUUGENG = "buugeng"
BIGBUUGENG = "bigbuugeng"
FRACTALGENG = "fractalgeng"
FAN = "fan"
BIGFAN = "bigfan"
TRIAD = "triad"
BIGTRIAD = "bigtriad"
MINIHOOP = "minihoop"
BIGHOOP = "bighoop"
DOUBLESTAR = "doublestar"
BIGDOUBLESTAR = "bigdoublestar"
QUIAD = "quiad"
SWORD = "sword"
GUITAR = "guitar"
UKULELE = "ukulele"
CHICKEN = "chicken"
COLOR_MAP = {RED: RED_HEX, BLUE: BLUE_HEX}

### ICONS ###

CLOCK_DIR = ICON_DIR + "clock/"
CLOCKWISE_ICON = CLOCK_DIR + "clockwise.png"
COUNTER_CLOCKWISE_ICON = CLOCK_DIR + "counter_clockwise.png"
EMPTY_CLOCK_ICON = CLOCK_DIR + "empty_clock.png"
CLOCK_ICON = CLOCK_DIR + "clock.png"
SWAP_ICON = "swap.png"
MIRROR_ICON = "mirror.png"
DECREMENT_TURNS_ICON = "subtract_turns.png"
INCREMENT_TURNS_ICON = "add_turns.png"
SWAP_COLORS_ICON = "swap_colors.png"

ICON_PATHS = {
    "swap_icon": ICON_DIR + SWAP_ICON,
    "swap_start_end": ICON_DIR + MIRROR_ICON,
    "subtract_turns": ICON_DIR + DECREMENT_TURNS_ICON,
    "add_turns": ICON_DIR + INCREMENT_TURNS_ICON,
    "swap_colors": ICON_DIR + SWAP_COLORS_ICON,
    "clockwise": CLOCKWISE_ICON,
    "counter_clockwise": COUNTER_CLOCKWISE_ICON,
}

ARROW_ATTRIBUTES = [COLOR, LOCATION, MOTION_TYPE, TURNS]
PROP_ATTRIBUTES = [COLOR, LOCATION, PROP_TYPE, ORIENTATION]
