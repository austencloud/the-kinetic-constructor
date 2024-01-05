from typing import *


from .Letters import *
from typing import Literal
from constants import *


MotionTypes = Literal["pro", "anti", "float", "dash", "static"]
Locations = Literal["n", "ne", "e", "se", "s", "sw", "w", "nw"]
Colors = Literal["blue", "red"]
Turns = Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
Orientations = Literal["in", "out", "clock", "counter"]
ParallelCombinationsSet = Set[Tuple[str, str, str, str]]
Handpaths = Literal["dash_handpath", "static_handpath", "cw_handpath", "ccw_handpath"]
Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
RotationAngles = Literal[0, 90, 180, 270]
PropRotDirs = Literal["cw", "ccw"]
OptimalLocationEntries = Dict[Literal["x", "y"], float]
StartEndLocationTuple = Tuple[Locations, Locations]
OptimalLocationDicts = Dict[str, OptimalLocationEntries]

