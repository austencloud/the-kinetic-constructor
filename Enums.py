from typing import TypedDict
from enum import Enum
from constants import *

image_path = "resources/images/"


class LetterNumberType(Enum):
    TYPE_1 = (
        [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ],
        "Type1",
    )
    TYPE_2 = (["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"], "Type2")
    TYPE_3 = (["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"], "Type3")
    TYPE_4 = (["Φ", "Ψ", "Λ"], "Type4")
    TYPE_5 = (["Φ-", "Ψ-", "Λ-"], "Type5")
    TYPE_6 = (["α", "β", "Γ"], "Type6")

    def __init__(self, letters, description):
        self._letters = letters
        self._description = description

    @property
    def letters(self):
        return self._letters

    @property
    def description(self):
        return self._description


class ShiftHandpaths(Enum):
    CW_HANDPATH = "cw"
    CCW_HANDPATH = "ccw"


class Handpath(Enum):
    CW_HANDPATH = "cw"
    CCW_HANDPATH = "ccw"
    STATIC_HANDPATH = "static_handpath"
    DASH_HANDPATH = "dash_handpath"


class Color(Enum):
    BLUE = "blue"
    RED = "red"


class HexColor(Enum):
    RED = "#ED1C24"
    BLUE = "#2E3192"


class BodySide(Enum):
    LEFT = "left"
    RIGHT = "right"


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Filter(Enum):
    BLUE_TURNS = "blue_turns"
    RED_TURNS = "red_turns"
    BLUE_END_ORI = "blue_end_ori"
    RED_END_ORI = "red_end_ori"


class MotionType(Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class GridMode(Enum):
    DIAMOND = "diamond"
    BOX = "box"


class Location(Enum):
    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    NORTHWEST = "nw"
    NORTHEAST = "ne"
    SOUTHWEST = "sw"
    SOUTHEAST = "se"


class PropRotationDirection(Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"


class Orientation(Enum):
    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"
    CLOCK_IN = "clock-in"
    CLOCK_OUT = "clock-out"
    COUNTER_IN = "counter-in"
    COUNTER_OUT = "counter-out"


class RadialOrientation(Enum):
    IN = "in"
    OUT = "out"


class AntiradialOrientation(Enum):
    CLOCK = "clock"
    COUNTER = "counter"


class OrientationType(Enum):
    RADIAL = "radial"
    ANTIRADIAL = "antiradial"


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Letter(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    Sigma = "Σ"
    Delta = "Δ"
    Theta = "θ"
    Omega = "Ω"
    W_dash = "W-"
    X_dash = "X-"
    Y_dash = "Y-"
    Z_dash = "Z-"
    Sigma_dash = "Σ-"
    Delta_dash = "Δ-"
    Theta_dash = "θ-"
    Omega_dash = "Ω-"
    Phi = "Φ"
    Psi = "Ψ"
    Lambda = "Λ"
    Phi_dash = "Φ-"
    Psi_dash = "Ψ-"
    Lambda_dash = "Λ-"
    Alpha = "α"
    Beta = "β"
    Gamma = "Γ"
    Eta = "η"
    Zeta = "ζ"
    Terra = "⊕"
    Tau = "𝛕"
    Mu = "μ"
    Nu = "ν"


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


class Letter(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    W_dash = "W-"
    X_dash = "X-"
    Y_dash = "Y-"
    Z_dash = "Z-"
    Sigma = "Σ"
    Delta = "Δ"
    Theta = "θ"
    Omega = "Ω"
    Phi = "Φ"
    Psi = "Ψ"
    Lambda = "Λ"
    Sigma_dash = "Σ-"
    Delta_dash = "Δ-"
    Theta_dash = "θ-"
    Omega_dash = "Ω-"
    Phi_dash = "Φ-"
    Psi_dash = "Ψ-"
    Lambda_dash = "Λ-"
    Alpha = "α"
    Beta = "β"
    Terra = "⊕"
    Tau = "𝛕"
    Mu = "μ"
    Nu = "ν"
    Zeta = "ζ"
    Eta = "η"


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


big_unilateral_prop_types = [
    BIGHOOP,
    BIGFAN,
    BIGTRIAD,
    GUITAR,
    SWORD,
    CHICKEN,
]
small_unilateral_prop_types = [
    FAN,
    CLUB,
    MINIHOOP,
    TRIAD,
    UKULELE,
]
big_bilateral_prop_types = [
    BIGSTAFF,
    BIGBUUGENG,
    BIGDOUBLESTAR,
]
small_bilateral_prop_types = [
    STAFF,
    BUUGENG,
    DOUBLESTAR,
    QUIAD,
    FRACTALGENG,
]
non_strictly_placed_props = [
    STAFF,
    FAN,
    BIGFAN,
    CLUB,
    BUUGENG,
    MINIHOOP,
    TRIAD,
    QUIAD,
    UKULELE,
    CHICKEN,
    FRACTALGENG,
]
strictly_placed_props = [
    BIGHOOP,
    DOUBLESTAR,
    BIGTRIAD,
    BIGFAN,
    BIGBUUGENG,
    BIGDOUBLESTAR,
]


class MotionCombinationType(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class Turns(Enum):
    FL = "fl"
    ZERO = "0"
    HALF = "0.5"
    ONE = "1"
    ONE_HALF = "1.5"
    TWO = "2"
    TWO_HALF = "2.5"
    THREE = "3"


class ArrowAttribute(Enum):
    COLOR = "color"
    LOC = "loc"
    MOTION_TYPE = "motion_type"
    TURNS = "turns"


class PropAttribute(Enum):
    COLOR = "color"
    PROP_TYPE = "prop_type"
    LOC = "loc"
    AXIS = "axis"
    ORI = "ori"


class MotionAttribute(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    PROP_ROT_DIR = "prop_rot_dir"
    TURNS = "turns"
    START_LOC = "start_loc"
    START_ORI = "start_ori"
    END_LOC = "end_loc"
    END_ORI = "end_ori"


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


class SpecificStartEndPositionsDicts(TypedDict):
    start_pos: SpecificPosition
    end_pos: SpecificPosition


### MOTION ATTRIBUTES ###
class MotionAttributesDicts(TypedDict):
    color: Color

    motion_type: MotionType
    rot_dir: PropRotationDirection
    loc: Location
    turns: Turns
    start_loc: Location
    start_ori: Orientation
    end_loc: Location
    end_ori: Orientation


class ArrowAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    location: Location
    turns: Turns


class PropAttributesDicts(TypedDict):
    color: Color
    prop_type: PropType
    loc: Location
    ori: Orientation


### LETTER GROUPS ###
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


class MotionTypeLetterGroups(Enum):
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


class VTGHandpathMode(Enum):
    TOG_SAME = "TS"
    TOG_OPPOSITE = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPPOSITE = "SO"
    QUARTER_TIME_SAME = "QTS"
    QUARTER_TIME_OPPOSITE = "QTO"


class TKAHandpathMode(Enum):
    ALPHA_TO_ALPHA = "α→α"  # ABC
    BETA_TO_ALPHA = "β→α"  # DEF
    BETA_TO_BETA = "β→β"  # GHI
    ALPHA_TO_BETA = "α→β"  # JKL
    GAMMA_TO_GAMMA_OPP_ANTIPARALLEL = "Γ→Γ_opp_antiparallel"  # MNO
    GAMMA_TO_GAMMA_OPP_PARALLEL = "Γ→Γ_opp_parallel"  # PQR
    GAMMA_TO_GAMMA_SAME_DIR = "Γ→Γ_same"  # STUV

    GAMMACLOCK_TO_GAMMACLOCK = "Γclock→Γclock"
    GAMMACLOCK_TO_GAMMACOUNTER = "Γclock→Γcounter"
    GAMMACOUNTER_TO_GAMMACOUNTER = "Γcounter→Γcounter"
    GAMMACOUNTER_TO_GAMMACLOCK = "Γcounter→Γclock"


class PictographAttributesDict(TypedDict):
    letter: Letter
    start_pos: Position
    end_pos: Position
    blue_motion_type: MotionType
    blue_prop_rot_dir: PropRotationDirection
    blue_start_loc: Location
    blue_end_loc: Location
    blue_turns: Turns
    blue_start_ori: Orientation
    blue_end_ori: Orientation
    red_motion_type: MotionType
    red_prop_rot_dir: PropRotationDirection
    red_start_loc: Location
    red_end_loc: Location
    red_turns: Turns
    red_start_ori: Orientation
    red_end_ori: Orientation


class PictographType(Enum):
    MAIN = "main"
    OPTION = "option"
    BEAT = "beat"
    START_POS = "start_pos"
    IG_PICTOGRAPH = "ig_pictograph"


class Mode(Enum):
    TOG_SAME = "TS"
    TOG_OPPOSITE = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPPOSITE = "SO"
    QUARTER_TIME_SAME = "QTS"
    QUARTER_TIME_OPPOSITE = "QTO"


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


class LetterGroupsByMotionType(Enum):
    ADGJMPS = "ADGJMPS"
    BEHKNQT = "BEHKNQT"
    αβΓ = "αβΓ"
    CFILORUV = "CFILORUV"
    WYΣθ = "WYΣθ"
    XZΔΩ = "XZΔΩ"
    X_Z_Δ_Ω_ = "X-Z-Δ-Ω-"
    ΦΨΛ = "ΦΨΛ"
    Φ_Ψ_Λ_ = "Φ-Ψ-Λ-"
