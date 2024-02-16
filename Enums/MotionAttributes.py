from enum import Enum
from typing import Literal


class Turns(Enum):
    INT = "int"
    FLOAT = "float"


class MotionTypes(Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class Locations(Enum):
    N = "n"
    NE = "ne"
    E = "e"
    SE = "se"
    S = "s"
    SW = "sw"
    W = "w"
    NW = "nw"


class Color(Enum):
    BLUE = "blue"
    RED = "red"

    def __str__(self, str: Literal["blue", "red"]):
        # return the item whose value matches the string
        return self[str]


class Orientations(Enum):
    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"


class PropRotDirs(Enum):
    CW = "cw"
    CCW = "ccw"
    NO_ROT = "no_rot"


class LeadStates(Enum):
    LEADING = "leading"
    TRAILING = "trailing"
