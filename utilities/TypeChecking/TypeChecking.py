from enum import Enum


class ParallelCombinationsSet(Enum):
    SET = "set"


class Handpaths(Enum):
    DASH_HANDPATH = "dash_handpath"
    STATIC_HANDPATH = "static_handpath"
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class RotationAngles(Enum):
    ANGLE_0 = 0
    ANGLE_90 = 90
    ANGLE_180 = 180
    ANGLE_270 = 270


class OptimalLocationEntries(Enum):
    X = "x"
    Y = "y"


class StartEndLocationTuple(Enum):
    LOCATIONS = "Locations"


class OptimalLocationDicts(Enum):
    DICT = "dict"


class Positions(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class SpecificPositions(Enum):
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


class ShiftHandpaths(Enum):
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class HexColors(Enum):
    COLOR_1 = "#ED1C24"
    COLOR_2 = "#2E3192"


class Directions(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class GridModes(Enum):
    DIAMOND = "diamond"
    BOX = "box"


class RadialOrientations(Enum):
    IN = "in"
    OUT = "out"


class NonRadialOrientations(Enum):
    CLOCK = "clock"
    COUNTER = "counter"


class OrientationTypes(Enum):
    RADIAL = "radial"
    NONRADIAL = "nonradial"


class Axes(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class MotionTypeCombinations(Enum):
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



class VtgTimings(Enum):
    SPLIT = "split"
    TOGETHER = "together"


class VtgDirections(Enum):
    SAME = "same"
    OPP = "opp"


class OpenCloseStates(Enum):
    OPEN = "open"
    CLOSE = "close"


class Letters(Enum):
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
    Σ = "Σ"
    Δ = "Δ"
    θ = "θ"
    Ω = "Ω"
    W_DASH = "W-"
    X_DASH = "X-"
    Y_DASH = "Y-"
    Z_DASH = "Z-"
    Σ_DASH = "Σ-"
    Δ_DASH = "Δ-"
    θ_DASH = "θ-"
    Ω_DASH = "Ω-"
    Φ = "Φ"
    Ψ = "Ψ"
    Λ = "Λ"
    Φ_DASH = "Φ-"
    Ψ_DASH = "Ψ-"
    Λ_DASH = "Λ-"
    α = "α"
    β = "β"
    Γ = "Γ"


class AdjustmentStrs(Enum):
    MINUS_1 = "-1"
    MINUS_0_5 = "-0.5"
    PLUS_1 = "+1"
    PLUS_0_5 = "+0.5"


class AdjustmentNums(Enum):
    FLOAT = float
    INT = int




class LetterTypeDescriptions(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class MotionAttributes(Enum):
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
    LEAD_STATE = "lead_state"


class Pictograph_Key(Enum):
    KEY = str
