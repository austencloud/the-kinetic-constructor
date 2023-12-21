from typing import *
from .Letters import *
from .SpecificPositions import SpecificPositions
from typing import Literal

Colors = Literal["red", "blue"]
MotionTypes = Literal["pro", "anti", "dash", "static"]
Locations = Literal["n", "e", "s", "w", "ne", "se", "sw", "nw"]
RotationDirections = Literal["cw", "ccw"]
Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]

### STAFF ATTRIBUTES ###

PropAttributes = Literal[
    "color", "prop_type", "location", "layer", "axis", "orientation"
]
PropTypes = Literal[
    "staff",
    "bigstaff",
    "buugeng",
    "bigbuugeng",
    "club",
    "fan",
    "bigfan",
    "minihoop",
    "triad",
    "bigtriad",
    "bighoop",
    "doublestar",
    "bigdoublestar",
    "quiad",
    "sword",
    "guitar",
    "ukulele",
    "chicken",
]
Layers = Literal[1, 2]
Axes = Literal["vertical", "horizontal"]
Orientations = Literal[
    "in",
    "clock-in",
    "clock",
    "clock-out",
    "out",
    "counter-out",
    "counter",
    "counter-in",
]

OrientationCombinations = Literal[
    "in_vs_in",
    "in_vs_clock-in",
    "in_vs_clock",
    "in_vs_clock-out",
    "in_vs_out",
    "in_vs_counter-out",
    "in_vs_counter",
    "in_vs_counter-in",
    "clock-in_vs_clock-in",
    "clock-in_vs_clock",
    "clock-in_vs_clock-out",
    "clock-in_vs_out",
    "clock-in_vs_counter-out",
    "clock-in_vs_counter",
    "clock-in_vs_counter-in",
    "clock_vs_clock",
    "clock_vs_clock-out",
    "clock_vs_out",
    "clock_vs_counter-out",
    "clock_vs_counter",
    "clock_vs_counter-in",
    "clock-out_vs_clock-out",
    "clock-out_vs_out",
    "clock-out_vs_counter-out",
    "clock-out_vs_counter",
    "clock-out_vs_counter-in",
    "out_vs_out",
    "out_vs_counter-out",
    "out_vs_counter",
    "out_vs_counter-in",
    "counter-out_vs_counter-out",
    "counter-out_vs_counter",
    "counter-out_vs_counter-in",
    "counter_vs_counter",
    "counter_vs_counter-in",
    "counter-in_vs_counter-in",
]


RotationAngles = Literal[0, 90, 180, 270]
Positions = Literal["alpha", "beta", "gamma"]
Direction = Literal["right", "left", "down", "up"]
ColorsHex = Literal["#ED1C24", "#2E3192"]
LetterType = Literal[
    "Dual-Shift", "Shift", "Cross-Shift", "Dash", "Dual-Dash", "Static"
]

GridModes = Literal["Box", "Diamond"]


class SpecificStartEndPositionsDicts(TypedDict):
    start_position: SpecificPositions
    end_position: SpecificPositions


OptimalLocationsEntries = Dict[Literal["x", "y"], float]


class OptimalLocationsDicts(TypedDict):
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
    location: Locations
    motion_type: MotionTypes
    turns: Turns


class MotionAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    rotation_direction: RotationDirections
    start_location: Locations
    end_location: Locations
    turns: Turns
    start_orientation: Orientations
    end_orientation: Orientations
    start_layer: Layers
    end_layer: Layers


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
OptimalLocationsDicts = Dict[str, OptimalLocationsEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationsDicts
)
DictVariantsLists = List[DictVariants]
LetterDictionary = Dict[Letters, List[DictVariantsLists]]


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
