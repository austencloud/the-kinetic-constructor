from typing import TypedDict
from enum import Enum
from constants import *
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
    Orientations,
    PropRotDirs,
    SpecificPositions,
    Turns,
)
from utilities.TypeChecking.prop_types import PropTypes
from utilities.TypeChecking.Letters import Letters

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


class MotionCombinationType(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


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
    start_pos: SpecificPositions
    end_pos: SpecificPositions


### MOTION ATTRIBUTES ###
class MotionAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    prop_rot_dir: PropRotDirs
    loc: Locations
    turns: Turns
    start_loc: Locations
    start_ori: Orientations
    end_loc: Locations
    end_ori: Orientations


class ArrowAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    location: Locations
    turns: Turns


class PropAttributesDicts(TypedDict):
    color: Colors
    prop_type: PropTypes
    loc: Locations
    ori: Orientations


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
    letter: Letters
    start_pos: SpecificPositions
    end_pos: SpecificPositions
    blue_motion_type: MotionTypes
    blue_prop_rot_dir: PropRotDirs
    blue_start_loc: Locations
    blue_end_loc: Locations
    blue_turns: Turns
    blue_start_ori: Orientations
    blue_end_ori: Orientations
    red_motion_type: MotionTypes
    red_prop_rot_dir: PropRotDirs
    red_start_loc: Locations
    red_end_loc: Locations
    red_turns: Turns
    red_start_ori: Orientations
    red_end_ori: Orientations


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
