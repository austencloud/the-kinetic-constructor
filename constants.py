import os

current_script_path = os.path.abspath(__file__).replace("\\", "/")
current_script_path = current_script_path[0].upper() + current_script_path[1:]

current_dir = os.path.dirname(current_script_path)
tka_sequence_constructor_dir = os.path.dirname(current_dir)
tka_app_dir = os.path.dirname(tka_sequence_constructor_dir)
resources_path = tka_app_dir + "/resources"

NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"
NORTHEAST = "ne"
SOUTHEAST = "se"
SOUTHWEST = "sw"
NORTHWEST = "nw"

VERTICAL = "vertical"
HORIZONTAL = "horizontal"

CLOCKWISE = "cw"
COUNTER_CLOCKWISE = "ccw"
NO_ROT = "no_rot"

CW_HANDPATH = "cw_handpath"
CCW_HANDPATH = "ccw_handpath"


START_POS = "start_pos"
END_POS = "end_pos"

BLUE_MOTION_TYPE = "blue_motion_type"
BLUE_PROP_ROT_DIR = "blue_prop_rot_dir"
BLUE_START_LOC = "blue_start_loc"
BLUE_END_LOC = "blue_end_loc"
BLUE_START_ORI = "blue_start_ori"
BLUE_END_ORI = "blue_end_or"
BLUE_TURNS = "blue_turns"

RED_MOTION_TYPE = "red_motion_type"
RED_PROP_ROT_DIR = "red_prop_rot_dir"
RED_START_LOC = "red_start_loc"
RED_END_LOC = "red_end_loc"
RED_START_ORI = "red_start_ori"
RED_END_ORI = "red_end_or"
RED_TURNS = "red_turns"


RED = "red"
BLUE = "blue"


HEX_RED = "#ED1C24"
HEX_BLUE = "#2E3192"

RADIAL = "radial"
ANTIRADIAL = "antiradial"

IN = "in"
OUT = "out"
CLOCK = "clock"
COUNTER = "counter"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

LETTER = "letter"
PRO = "pro"
ANTI = "anti"
FLOAT = "float"
DASH = "dash"
STATIC = "static"

COLOR = "color"
ARROW = "arrow"
GHOST_ARROW = "ghost_arrow"
PROP = "prop"
GHOST_PROP = "ghost_prop"
LETTER_ITEM = "letter_item"
LOC = "location"
MOTION_TYPE = "motion_type"
TURNS = "turns"
PROP_TYPE = "prop_type"
PROP_LOC = "prop_loc"
PROP_ORI = "prop_ori"
PROP_ROT_DIR = "prop_rot_dir"
ORIENTATION = "ori"
START_ORI = "start_ori"
END_ORI = "end_ori"
AXIS = "axis"
START_LOC = "start_loc"
END_LOC = "end_loc"

STATIC_HANDPATH = "static_handpath"
DASH_HANDPATH = "dash_handpath"

PICTOGRAPH_DIR = "resources/images/pictographs/"
ARROW_DIR = "resources/images/arrows/"
PROP_DIR = "resources/images/props/"
LETTER_BTN_ICON_DIR = "resources/images/letter_button_icons"
LETTERS_TRIMMED_SVG_DIR = "resources/images/letters_trimmed/"
ICON_DIR = "resources/images/icons/"
GRID_DIR = "resources/images/grid/"


GHOST = "ghost"

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


MAIN = "main"
OPTION = "option"
BEAT = "beat"
START_POS_BEAT = "start_pos_beat"
IG_PICTOGRAPH = "ig_pictograph"

DIAMOND = "diamond"
BOX = "box"

ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"

ALPHA1 = "alpha1"
ALPHA2 = "alpha2"
ALPHA3 = "alpha3"
ALPHA4 = "alpha4"
BETA1 = "beta1"
BETA2 = "beta2"
BETA3 = "beta3"
BETA4 = "beta4"
GAMMA1 = "gamma1"
GAMMA2 = "gamma2"
GAMMA3 = "gamma3"
GAMMA4 = "gamma4"
GAMMA5 = "gamma5"
GAMMA6 = "gamma6"
GAMMA7 = "gamma7"
GAMMA8 = "gamma8"


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

DISTANCE = 40
