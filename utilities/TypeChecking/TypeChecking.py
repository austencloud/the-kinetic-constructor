from typing import *
from .Letters import *
from .SpecificPositions import SpecificPositions
from typing import Literal
from constants.string_constants import *
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


class OrientationType(Enum):
    RADIAL = "radial"
    ANTIRADIAL = "antiradial"


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


class Position(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class SpecificPosition(Enum):
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

big_bilateral_prop_types = [
    PropType.BIGSTAFF,
    PropType.BIGBUUGENG,
    PropType.BIGDOUBLESTAR,
]

small_bilateral_prop_types = [
    PropType.STAFF,
    PropType.BUUGENG,
    PropType.DOUBLESTAR,
    PropType.QUIAD,
    PropType.FRACTALGENG,
]

non_strictly_placed_props = [
    PropType.STAFF,
    PropType.FAN,
    PropType.BIGFAN,
    PropType.CLUB,
    PropType.BUUGENG,
    PropType.MINIHOOP,
    PropType.TRIAD,
    PropType.QUIAD,
    PropType.UKULELE,
    PropType.CHICKEN,
    PropType.FRACTALGENG,
]

strictly_placed_props = [
    PropType.BIGHOOP,
    PropType.DOUBLESTAR,
    PropType.BIGTRIAD,
    PropType.BIGFAN,
    PropType.BIGBUUGENG,
    PropType.BIGDOUBLESTAR,
]


class LetterType(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]


class PropAttribute(Enum):
    COLOR = "color"
    PROP_TYPE = "prop_type"
    LOCATION = "location"
    LAYER = "layer"
    AXIS = "axis"
    ORIENTATION = "orientation"

class MotionAttribute(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    ROTATION_DIRECTION = "rotation_direction"
    TURNS = "turns"
    START_LOCATION = "start_location"
    START_ORIENTATION = "start_orientation"
    END_LOCATION = "end_location"
    END_ORIENTATION = "end_orientation"

class OrientationCombination(Enum):
    IN_VS_IN = "in_vs_in"
    IN_VS_CLOCK_IN = "in_vs_clock-in"
    IN_VS_CLOCK = "in_vs_clock"
    IN_VS_CLOCK_OUT = "in_vs_clock-out"
    IN_VS_OUT = "in_vs_out"
    IN_VS_COUNTER_OUT = "in_vs_counter-out"
    IN_VS_COUNTER = "in_vs_counter"
    IN_VS_COUNTER_IN = "in_vs_counter-in"
    CLOCK_IN_VS_CLOCK_IN = "clock-in_vs_clock-in"
    CLOCK_IN_VS_CLOCK = "clock-in_vs_clock"
    CLOCK_IN_VS_CLOCK_OUT = "clock-in_vs_clock-out"
    CLOCK_IN_VS_OUT = "clock-in_vs_out"
    CLOCK_IN_VS_COUNTER_OUT = "clock-in_vs_counter-out"
    CLOCK_IN_VS_COUNTER = "clock-in_vs_counter"
    CLOCK_IN_VS_COUNTER_IN = "clock-in_vs_counter-in"
    CLOCK_VS_CLOCK = "clock_vs_clock"
    CLOCK_VS_CLOCK_OUT = "clock_vs_clock-out"
    CLOCK_VS_OUT = "clock_vs_out"
    CLOCK_VS_COUNTER_OUT = "clock_vs_counter-out"
    CLOCK_VS_COUNTER = "clock_vs_counter"
    CLOCK_VS_COUNTER_IN = "clock_vs_counter-in"
    CLOCK_OUT_VS_CLOCK_OUT = "clock-out_vs_clock-out"
    CLOCK_OUT_VS_OUT = "clock-out_vs_out"
    CLOCK_OUT_VS_COUNTER_OUT = "clock-out_vs_counter-out"
    CLOCK_OUT_VS_COUNTER = "clock-out_vs_counter"
    CLOCK_OUT_VS_COUNTER_IN = "clock-out_vs_counter-in"
    OUT_VS_OUT = "out_vs_out"
    OUT_VS_COUNTER_OUT = "out_vs_counter-out"
    OUT_VS_COUNTER = "out_vs_counter"
    OUT_VS_COUNTER_IN = "out_vs_counter-in"
    COUNTER_OUT_VS_COUNTER_OUT = "counter-out_vs_counter-out"
    COUNTER_OUT_VS_COUNTER = "counter-out_vs_counter"
    COUNTER_OUT_VS_COUNTER_IN = "counter-out_vs_counter-in"
    COUNTER_VS_COUNTER = "counter_vs_counter"
    COUNTER_VS_COUNTER_IN = "counter_vs_counter-in"
    COUNTER_IN_VS_COUNTER_IN = "counter-in_vs_counter-in"



RotationAngles = Literal[0, 90, 180, 270]
ColorsHex = Literal["#ED1C24", "#2E3192"]


GridModes = Literal["Box", "Diamond"]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPosition
    end_position: SpecificPosition


OptimalLocationsEntries = Dict[Literal["x", "y"], float]


class PropAttributesDicts(TypedDict):
    color: Color
    prop_type: PropType
    prop_location: Location
    orientation: Orientation


### MOTION ATTRIBUTES ###
class MotionAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    rotation_direction: RotationDirection
    location: Location
    turns: Turns

    start_location: Location
    start_orientation: Orientation

    end_location: Location
    end_orientation: Orientation


class ArrowAttributesDicts(TypedDict):
    color: Color
    location: Location
    motion_type: MotionType
    turns: Turns


class MotionAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    rotation_direction: RotationDirection
    start_location: Location
    end_location: Location
    turns: Turns
    start_orientation: Orientation
    end_orientation: Orientation

class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"

StartEndLocationsTuple = Tuple[Location, Location]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letters, List[MotionAttributesDicts]]],
]
OptimalLocationsDicts = Dict[str, OptimalLocationsEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationsDicts
)
DictVariantsLists = List[DictVariants]
PictographDataframe = Dict[Letters, List[DictVariantsLists]]

class Mode(Enum):
    TOG_SAME = "TS"
    TOG_OPPOSITE = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPPOSITE = "SO"
    QUARTER_TIME_SAME = "QTS"
    QUARTER_TIME_OPPOSITE = "QTO"
    
class PictographAttributesDict(TypedDict):
    start_position: Position
    end_position: Position
    letter_type: LetterType
    mode: Mode
    motion_type_combination: MotionTypeCombination




### LETTER GROUPS ###

class MotionTypesCombinations(Enum):
    PRO_VS_PRO = "ADGJMPS"
    ANTI_VS_ANTI = "BEHKNQT"
    STATIC_VS_STATIC = "αβΓ"
    PRO_VS_ANTI = "CFILORUV"
    STATIC_VS_PRO = "WYΣθ"
    STATIC_VS_ANTI = "XZΔΩ"
    DASH_VS_PRO = "W-Y-Σ-θ-"
    DASH_VS_ANTI = "X-Z-Δ-Ω-"
    DASH_VS_STATIC = "ΦΨΛ"
    DASH_VS_DASH = "Φ-Ψ-Λ-"

LetterGroupsByMotionTypes = Literal[
    "ADGJMPS",
    "BEHKNQT",
    "CFILORUV",
    "WYΣθ",
    "XZΔΩ",
    "W-Y-Σ-θ-",
    "X-Z-Δ-Ω-",
    "ΦΨΛ",
    "Φ-Ψ-Λ-",
    "αβΓ",
]




MotionTypesLetterGroupMap = Dict[MotionTypesCombinations, LetterGroupsByMotionTypes]
ParallelCombinationsSet = Set[Tuple[str, str, str, str]]
