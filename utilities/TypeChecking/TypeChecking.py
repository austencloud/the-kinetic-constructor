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
StartEndLocationTuple = Tuple[Locations]
OptimalLocationDicts = Dict[str, OptimalLocationEntries]
Positions = Literal["alpha", "beta", "gamma"]
SpecificPositions = Literal[
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


ShiftHandpaths = Literal["cw_handpath", "ccw_handpath"]
Handpaths = Literal["dash_handpath", "static_handpath", "cw_handpath", "ccw_handpath"]
HexColors = Literal["#ED1C24", "#2E3192"]
Directions = Literal["left", "right", "up", "down"]
GridModes = Literal["diamond", "box"]
RadialOrientations = Literal["in", "out"]
AntiradialOrientations = Literal["clock", "counter"]
OrientationTypes = Literal["radial", "antiradial"]
Axes = Literal["horizontal", "vertical"]
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

