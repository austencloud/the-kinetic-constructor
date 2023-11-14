from typing import TypedDict, Literal, Dict, List, Tuple, Set
from .Letters import Letters, GammaLetters
from .SpecificPosition import SpecificPosition

RotationAngle = Literal[0, 90, 180, 270]
Location = Literal["n", "e", "s", "w"]
Position = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
OptimalLocationEntries = Dict[Literal["x", "y"], float]
Layer = Literal[0, 1, 2, 3]

### ARROW ATTRIBUTES ###

Color = Literal["red", "blue"]
ColorHex = Literal["#ED1C24", "#2E3192"]
MotionType = Literal["pro", "anti", "dash", "static", "float", "chu"]
Quadrant = Literal["ne", "se", "sw", "nw"]
RotationDirection = Literal["cw", "ccw"]
StartLocation = Location
EndLocation = Location
Turns = Literal[0, 1, 2]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPosition
    end_position: SpecificPosition


class ArrowAttributesDicts(TypedDict):
    color: Color
    motion_type: MotionType
    quadrant: Quadrant
    rotation_direction: RotationDirection
    start_location: StartLocation
    end_location: EndLocation
    turns: Turns


class OptimalLocationsDicts(TypedDict):
    optimal_red_location: OptimalLocationEntries
    optimal_blue_location: OptimalLocationEntries


### STAFF ATTRIBUTES ###


class StaffAttributesDicts(TypedDict):
    color: Color
    location: Location
    layer: Layer


StartEndLocationTuple = Tuple[StartLocation, EndLocation]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letters, List[ArrowAttributesDicts]]],
]
OptimalLocationsDicts = Dict[str, OptimalLocationEntries]
DictVariants = (
    ArrowAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationsDicts
)
DictVariantsLists = List[List[DictVariants]]
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
