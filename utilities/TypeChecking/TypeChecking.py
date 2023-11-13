from typing import TypedDict, Literal, Dict, List, Tuple
from .Letter import Letter
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

SpecificStartEndPositions = Dict[SpecificPosition, SpecificPosition]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositions, List[Tuple[str, List[ArrowAttributes]]]
]
OptimalLocation = Dict[str, float]
OptimalLocations = Dict[str, OptimalLocation]
Variant = ArrowAttributes | SpecificStartEndPositions | OptimalLocations
Variants = List[List[Variant]]
LetterVariants = Dict[str, Variants]
LettersDict = Dict[str, Variants]

