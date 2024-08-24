from enum import Enum
from typing import Literal




class MotionType(Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class Location(Enum):
    N = "n"
    NE = "ne"
    E = "e"
    SE = "se"
    S = "s"
    SW = "sw"
    W = "w"
    NW = "nw"





class Orientations(Enum):
    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"


class PropRotDir(Enum):
    CW = "cw"
    CCW = "ccw"
    NO_ROT = "no_rot"


class LeadStates(Enum):
    LEADING = "leading"
    TRAILING = "trailing"
