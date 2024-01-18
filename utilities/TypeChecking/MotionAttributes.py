from typing import Literal, Union


Turns = Union[int, float]
MotionTypes = Literal["pro", "anti", "float", "dash", "static"]
Locations = Literal["n", "ne", "e", "se", "s", "sw", "w", "nw"]
Colors = Literal["blue", "red"]
Orientations = Literal["in", "out", "clock", "counter"]
PropRotDirs = Literal["cw", "ccw", "no_rot"]
