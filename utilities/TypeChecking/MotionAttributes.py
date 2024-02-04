from enum import Enum, auto


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


class Colors(Enum):
    BLUE = "blue"
    RED = "red"


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

