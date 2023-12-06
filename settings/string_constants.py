import os

current_script_path = os.path.abspath(__file__).replace('\\', '/')
current_script_path = current_script_path[0].upper() + current_script_path[1:]

current_dir = os.path.dirname(current_script_path)
tka_sequence_constructor_dir = os.path.dirname(current_dir)
tka_app_dir = os.path.dirname(tka_sequence_constructor_dir)
resources_path = tka_app_dir + '/resources'

STAFF_SVG_FILE_PATH = resources_path + "/images/props/staff.svg"
CLUB_SVG_FILE_PATH = resources_path + "/images/props/club.svg"
BUUGENG_SVG_FILE_PATH = resources_path + "/images/props/buugeng.svg"
FAN_SVG_FILE_PATH = resources_path + "/images/props/fan.svg"
TRIAD_SVG_FILE_PATH = resources_path + "/images/props/triad.svg"
HOOP_SVG_FILE_PATH = resources_path + "/images/props/hoop.svg"

PICTOGRAPH_DIR = resources_path + "/images/pictographs/"
ARROW_DIR = resources_path + "/images/arrows/"
PROP_DIR = resources_path + "/images/props/"
LETTER_SVG_DIR = resources_path + "/images/letters/"
ICON_DIR = resources_path + "/images/icons/"
GRID_DIR = resources_path + "/images/grid/"
LETTER_JSON_DIR = resources_path + "/json/"

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
DASH = "dash"
STATIC = "static"

COLOR = "color"
MOTION_TYPE = "motion_type"
ROTATION_DIRECTION = "rotation_direction"
TURNS = "turns"


LOCATION = "location"
ARROW_LOCATION = "arrow_location"
PROP_LOCATION = "prop_location"
START_LOCATION = "start_location"
END_LOCATION = "end_location"

START_ORIENTATION = "start_orientation"
END_ORIENTATION = "end_orientation"

START_LAYER = "start_layer"
END_LAYER = "end_layer"

CLOCKWISE = "cw" or "CW"
COUNTER_CLOCKWISE = "ccw" or "CCW"

START_POS = "start_position"
END_POS = "end_position"

PROP_TYPE = "prop_type"
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

ARROW_ATTRIBUTES = [
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    ARROW_LOCATION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
]

PROP_ATTRIBUTES = [COLOR, PROP_TYPE, PROP_LOCATION, LAYER, ORIENTATION]
