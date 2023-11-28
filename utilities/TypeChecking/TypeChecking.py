from typing import *
from .Letters import *
from .SpecificPosition import SpecificPosition
from typing import Literal

Color = Literal["red", "blue"]
MotionType = Literal["pro", "anti", "dash", "static"]
Location = Literal["n", "e", "s", "w", "ne", "se", "sw", "nw"]
RotationDirection = Literal["cw", "ccw"]
Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2"]

### STAFF ATTRIBUTES ###

PropAttributes = Literal[
    "color", "prop_type", "location", "layer", "axis", "orientation"
]
PropType = Literal["staff", "buugeng", "club", "fan", "hoop", "triad"]
Layer = Literal[1, 2]
Axis = Literal["vertical", "horizontal"]
Layer1_Orientation = Literal["in", "out"]
Layer2_Orientation = Literal["cw", "ccw"]
Orientation = Literal["in", "out", "cw", "ccw"]

RotationAngle = Literal[0, 90, 180, 270]
Position = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
OptimalLocationEntries = Dict[Literal["x", "y"], float]
ColorHex = Literal["#ED1C24", "#2E3192"]
ColorMap = Dict[Color, ColorHex]
LetterType = Literal[
    "Dual-Shift", "Shift", "Cross-Shift", "Dash", "Dual-Dash", "Static"
]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPosition
    end_position: SpecificPosition


class OptimalLocationsDicts(TypedDict):
    optimal_red_location: OptimalLocationEntries
    optimal_blue_location: OptimalLocationEntries


class PropAttributesDicts(TypedDict):
    color: Color
    prop_type: PropType
    prop_location: Location
    layer: Layer
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
    start_layer: Layer

    end_location: Location
    end_orientation: Orientation
    end_layer: Layer


class ArrowAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    rotation_direction: RotationDirection
    arrow_location: Location
    start_location: Location
    end_location: Location
    turns: Turns


MotionAttributes = Literal[
    "color",
    "motion_type",
    "location",
    "rotation_direction",
    "turns",
    "start_location",
    "end_location",
    "start_orientation",
    "end_orientation",
    "start_layer",
    "end_layer",
]

MotionTypeCombinations = Literal[
    "pro_vs_pro",
    "anti_vs_anti",
    "static_vs_static",
    "pro_vs_anti",
    "static_vs_pro",
    "static_vs_anti",
    "dash_vs_pro",
    "dash_vs_anti",
    "dash_vs_static",
    "dash_vs_dash",
]

StartEndLocationTuple = Tuple[Location, Location]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letters, List[MotionAttributesDicts]]],
]
OptimalLocationsDicts = Dict[str, OptimalLocationEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationsDicts
)
DictVariantsLists = List[DictVariants]
LetterDictionary = Dict[Letters, List[List[DictVariants]]]


Mode = Optional[Literal["TS", "TO", "SS", "SO", "QTS", "QTO"]]


class PictographAttributesDict(TypedDict):
    start_position: Position
    end_position: Position
    letter_type: LetterType
    mode: Mode
    motion_type_combination: MotionTypeCombinations


HybridCombinations = Literal[
    "pro_vs_anti",
    "static_vs_pro",
    "static_vs_anti",
    "dash_vs_pro",
    "dash_vs_anti",
    "dash_vs_static",
]

### LETTER GROUPS ###

LetterGroupsByMotionType = Literal[
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


MotionTypeLetterGroupMap = Dict[MotionTypeCombinations, LetterGroupsByMotionType]
ParallelCombinationsSet = Set[Tuple[str, str, str, str]]
