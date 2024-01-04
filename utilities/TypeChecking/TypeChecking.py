from typing import *

from Enums import (
    Letter,
    Location,
    MotionAttributesDicts,
    SpecificStartEndPositionsDicts,
)
from .Letters import *
from typing import Literal
from constants import *
from enum import Enum
from typing import Dict
from Enums import MotionTypeCombination


Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
RotationAngles = Literal[0, 90, 180, 270]
OptimalLocationEntries = Dict[Literal["x", "y"], float]
StartEndLocationTuple = Tuple[Location, Location]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letter, List[MotionAttributesDicts]]],
]
OptimalLocationDicts = Dict[str, OptimalLocationEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationDicts
)
DictVariantsLists = List[DictVariants]

MotionTypes = Literal["pro", "anti", "float", "dash", "static"]
Locations = Literal["n", "ne", "e", "se", "s", "sw", "w", "nw"]
Colors = Literal["blue", "red"]
Turns = Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
Orientations = Literal["in", "out", "clock", "counter"]
ParallelCombinationsSet = Set[Tuple[str, str, str, str]]
Handpaths = Literal["dash_handpath", "static_handpath", "cw_handpath", "ccw_handpath"]