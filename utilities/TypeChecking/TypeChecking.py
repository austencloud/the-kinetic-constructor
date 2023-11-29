from typing import *
from .Letters import *
from .SpecificPositions import SpecificPositions
from typing import Literal

Colors = Literal["red", "blue"]
MotionTypes = Literal["pro", "anti", "dash", "static"]
Locations = Literal["n", "e", "s", "w", "ne", "se", "sw", "nw"]
RotationDirections = Literal["cw", "ccw"]
Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2"]

### STAFF ATTRIBUTES ###

PropAttributes = Literal[
    "color", "prop_type", "location", "layer", "axis", "orientation"
]
PropTypes = Literal["staff", "buugeng", "club", "fan", "hoop", "triad"]
Layers = Literal[1, 2]
Axes = Literal["vertical", "horizontal"]
Orientations = Literal["in", "out", "cw", "ccw"]

RotationAngles = Literal[0, 90, 180, 270]
Positions = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
ColorsHex = Literal["#ED1C24", "#2E3192"]
LetterType = Literal[
    "Dual-Shift", "Shift", "Cross-Shift", "Dash", "Dual-Dash", "Static"
]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPositions
    end_position: SpecificPositions



OptimalLocationsEntries = Dict[Literal["x", "y"], float]
class OptimalLocationssDicts(TypedDict):
    optimal_red_location: OptimalLocationsEntries
    optimal_blue_location: OptimalLocationsEntries


class PropAttributesDicts(TypedDict):
    color: Colors
    prop_type: PropTypes
    prop_location: Locations
    layer: Layers
    orientation: Orientations


### MOTION ATTRIBUTES ###
class MotionAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    rotation_direction: RotationDirections
    location: Locations
    turns: Turns

    start_location: Locations
    start_orientation: Orientations
    start_layer: Layers

    end_location: Locations
    end_orientation: Orientations
    end_layer: Layers


class ArrowAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    rotation_direction: RotationDirections
    arrow_location: Locations
    start_location: Locations
    end_location: Locations
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

MotionTypesCombinations = Literal[
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

StartEndLocationsTuple = Tuple[Locations, Locations]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letters, List[MotionAttributesDicts]]],
]
OptimalLocationssDicts = Dict[str, OptimalLocationsEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationssDicts
)
DictVariantsLists = List[DictVariants]
LetterDictionary = Dict[Letters, List[List[DictVariants]]]


Mode = Optional[Literal["TS", "TO", "SS", "SO", "QTS", "QTO"]]


class PictographAttributesDict(TypedDict):
    start_position: Positions
    end_position: Positions
    letter_type: LetterType
    mode: Mode
    motion_type_combination: MotionTypesCombinations


HybridCombinations = Literal[
    "pro_vs_anti",
    "static_vs_pro",
    "static_vs_anti",
    "dash_vs_pro",
    "dash_vs_anti",
    "dash_vs_static",
]

### LETTER GROUPS ###

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
