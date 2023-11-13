from typing import Dict, Literal, List

# Defining individual types
Color = Literal["red", "blue"]
MotionType = Literal["pro", "anti", "dash", "static", "float", "chu"]
Quadrant = Literal["ne", "se", "sw", "nw"]
RotationDirection = Literal["cw", "ccw"]
Location = Literal["n", "e", "s", "w"]
Turns = Literal[0, 1]

# Arrow attributes
ArrowAttributes = Dict[
    str, Color | MotionType | Quadrant | RotationDirection | Location | Location | Turns
]

# Other definitions
SpecificPosition = Literal[
    "alpha1",
    "alpha2",
    "alpha3",
    "alpha4",
    "beta1",
    "beta2",
    "beta3",
    "beta4",
    "gamma1",
    "gamma2",
    "gamma3",
    "gamma4",
    "gamma5",
    "gamma6",
    "gamma7",
    "gamma8",
]
Position = Literal["alpha", "beta", "gamma"]
SpecificStartEndPositions = Dict[SpecificPosition, SpecificPosition]
OptimalLocation = Dict[str, float]
OptimalLocations = Dict[str, OptimalLocation]
Variant = ArrowAttributes | SpecificStartEndPositions | OptimalLocations
Variants = List[List[Variant]]
LetterVariants = Dict[str, Variants]
LettersDict = Dict[str, Variants]
Direction = Literal["right", "left", "down", "up"]
