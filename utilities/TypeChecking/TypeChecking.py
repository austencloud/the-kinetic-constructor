from typing import TypedDict, Literal, Dict, List, Tuple, Set
from .Letters import Letters, GammaLetters
from .SpecificPosition import SpecificPosition

RotationAngle = Literal[0, 90, 180, 270]
Location = Literal["n", "e", "s", "w"]
Position = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
Color = Literal["red", "blue"]
MotionType = Literal["pro", "anti", "dash", "static", "float", "chu"]
Quadrant = Literal["ne", "se", "sw", "nw"]
RotationDirection = Literal["cw", "ccw"]
StartLocation = Location
EndLocation = Location
Turns = Literal[0, 1, 2]


class ArrowAttributes(TypedDict):
    color: Color
    motion_type: MotionType
    quadrant: Quadrant
    rotation_direction: RotationDirection
    start_location: StartLocation
    end_location: EndLocation
    turns: Turns


StartEndLocationTuple = Tuple[StartLocation, EndLocation]
SpecificStartEndPositionsDict = Dict[SpecificPosition, SpecificPosition]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDict, List[Tuple[Letters, List[ArrowAttributes]]]
]
OptimalLocation = Dict[Literal["x", "y"], float]
OptimalLocations = Dict[str, OptimalLocation]
Dict_Variant = ArrowAttributes | SpecificStartEndPositionsDict | OptimalLocations
Dict_Variants = List[List[Dict_Variant]]
LetterVariants = Dict[str, Dict_Variants]
LettersDict = Dict[str, Dict_Variants]


List[Tuple[str, List[Dict[str, str | int]]]]

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
