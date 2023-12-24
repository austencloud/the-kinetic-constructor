from enum import Enum

# Colors
class Color(Enum):
    BLUE = "blue"
    RED = "red"

# Hexadecimal Colors
class HexColor(Enum):
    RED = "#ED1C24"
    BLUE = "#2E3192"

# Directions
class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

# Motion Types
class MotionType(Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"

# Grid Modes
class GridMode(Enum):
    DIAMOND = "diamond"
    BOX = "box"

# Locations
class Location(Enum):
    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    NORTHWEST = "nw"
    NORTHEAST = "ne"
    SOUTHWEST = "sw"
    SOUTHEAST = "se"

# Rotation Directions
class RotationDirection(Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"

# Orientations
class Orientation(Enum):
    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"
    CLOCK_IN = "clock-in"
    CLOCK_OUT = "clock-out"
    COUNTER_IN = "counter-in"
    COUNTER_OUT = "counter-out"

# Axes
class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

# Prop Types
class PropType(Enum):
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

# Lists of specific Prop Types
big_unilateral_prop_types = [
    PropType.BIGHOOP,
    PropType.BIGFAN,
    PropType.BIGTRIAD,
    PropType.GUITAR,
    PropType.SWORD,
    PropType.CHICKEN,
]
small_unilateral_prop_types = [
    PropType.FAN,
    PropType.CLUB,
    PropType.MINIHOOP,
    PropType.TRIAD,
    PropType.UKULELE,
]
