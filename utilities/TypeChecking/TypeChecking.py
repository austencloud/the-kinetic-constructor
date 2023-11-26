from typing import *
from .Letters import *
from .SpecificPosition import SpecificPosition

### ARROW ATTRIBUTES ###


ArrowAttributes = Literal[
    "color",
    "motion_type",
    "quadrant",
    "rotation_direction",
    "start_location",
    "end_location",
    "turns",
]
Color = Literal["red", "blue"]
MotionType = Literal["pro", "anti", "dash", "static", "float", "chu"]
Quadrant = Literal["ne", "se", "sw", "nw"]
RotationDirection = Literal["cw", "ccw"]
Location = Literal["n", "e", "s", "w"]
Turns = float | Literal[0, 1, 2]  # Allowed values: 0, 0.5, 1, 1.5, 2, 2.5


class ArrowAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    quadrant: Quadrant
    rotation_direction: RotationDirection
    start_location: Location
    end_location: Location
    turns: Turns


### STAFF ATTRIBUTES ###

PropAttributes = Literal["color", "location", "layer", "axis", "orientation"]
Layer = Literal[1, 2]
Axis = Literal["vertical", "horizontal"]
Layer1_Orientation = Literal["in", "out"]
Layer2_Orientation = Literal["cw", "ccw"]

RotationAngle = Literal[0, 90, 180, 270]
Position = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
OptimalLocationEntries = Dict[Literal["x", "y"], float]
ColorHex = Literal["#ED1C24", "#2E3192"]
ColorMap = Dict[Color, ColorHex]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPosition
    end_position: SpecificPosition


class OptimalLocationsDicts(TypedDict):
    optimal_red_location: OptimalLocationEntries
    optimal_blue_location: OptimalLocationEntries


### STAFF ATTRIBUTES ###


class PropAttributesDicts(TypedDict):
    color: Color
    location: Location
    layer: Layer
    axis: Axis
    orientation: Layer1_Orientation | Layer2_Orientation


StartEndLocationTuple = Tuple[Location, Location]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letters, List[ArrowAttributesDicts]]],
]
OptimalLocationsDicts = Dict[str, OptimalLocationEntries]
DictVariants = (
    ArrowAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationsDicts
)
DictVariantsLists = List[DictVariants]
LetterDictionary = Dict[Letters, List[List[DictVariants]]]

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
