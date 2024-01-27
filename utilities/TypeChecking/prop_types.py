from typing import Literal
from constants import *

PropTypes = Literal[
    "staff",
    "bigstaff",
    "club",
    "buugeng",
    "bigbuugeng",
    "fractalgeng",
    "fan",
    "bigfan",
    "triad",
    "bigtriad",
    "minihoop",
    "bighoop",
    "doublestar",
    "bigdoublestar",
    "quiad",
    "sword",
    "guitar",
    "ukulele",
    "chicken",
]

big_unilateral_prop_types = [
    BIGHOOP,
    BIGFAN,
    BIGTRIAD,
    GUITAR,
    SWORD,
    CHICKEN,
]
small_unilateral_prop_types = [
    FAN,
    CLUB,
    MINIHOOP,
    TRIAD,
    UKULELE,
]
big_bilateral_prop_types = [
    BIGSTAFF,
    BIGBUUGENG,
    BIGDOUBLESTAR,
]
small_bilateral_prop_types = [
    STAFF,
    BUUGENG,
    DOUBLESTAR,
    QUIAD,
    FRACTALGENG,
]
non_strictly_placed_props = [
    STAFF,
    FAN,
    BIGFAN,
    CLUB,
    BUUGENG,
    MINIHOOP,
    TRIAD,
    QUIAD,
    UKULELE,
    CHICKEN,
    FRACTALGENG,
]
strictly_placed_props = [
    BIGHOOP,
    DOUBLESTAR,
    BIGTRIAD,
    BIGFAN,
    BIGBUUGENG,
    BIGDOUBLESTAR,
]


### LISTS FOR ITERATION ###

PropTypeslist = (
    "staff",
    "bigstaff",
    "club",
    "buugeng",
    "bigbuugeng",
    "fractalgeng",
    "fan",
    "bigfan",
    "triad",
    "bigtriad",
    "minihoop",
    "bighoop",
    "doublestar",
    "bigdoublestar",
    "quiad",
    "sword",
    "guitar",
    "ukulele",
    "chicken",
)
