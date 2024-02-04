from enum import Enum, auto

class PropTypes(Enum):
    Staff = auto()
    Bigstaff = auto()
    Club = auto()
    Buugeng = auto()
    Bigbuugeng = auto()
    Fractalgeng = auto()
    Fan = auto()
    Bigfan = auto()
    Triad = auto()
    Bigtriad = auto()
    Minihoop = auto()
    Bighoop = auto()
    Doublestar = auto()
    Bigdoublestar = auto()
    Quiad = auto()
    Sword = auto()
    Guitar = auto()
    Ukulele = auto()
    Chicken = auto()

big_unilateral_prop_types = [
    PropTypes.Bighoop,
    PropTypes.Bigfan,
    PropTypes.Bigtriad,
    PropTypes.Guitar,
    PropTypes.Sword,
    PropTypes.Chicken,
]
small_unilateral_prop_types = [
    PropTypes.Fan,
    PropTypes.Club,
    PropTypes.Minihoop,
    PropTypes.Triad,
    PropTypes.Ukulele,
]
big_bilateral_prop_types = [
    PropTypes.Bigstaff,
    PropTypes.Bigbuugeng,
    PropTypes.Bigdoublestar,
]
small_bilateral_prop_types = [
    PropTypes.Staff,
    PropTypes.Buugeng,
    PropTypes.Doublestar,
    PropTypes.Quiad,
    PropTypes.Fractalgeng,
]
non_strictly_placed_props = [
    PropTypes.Staff,
    PropTypes.Fan,
    PropTypes.Bigfan,
    PropTypes.Club,
    PropTypes.Buugeng,
    PropTypes.Minihoop,
    PropTypes.Triad,
    PropTypes.Quiad,
    PropTypes.Ukulele,
    PropTypes.Chicken,
    PropTypes.Fractalgeng,
]
strictly_placed_props = [
    PropTypes.Bighoop,
    PropTypes.Doublestar,
    PropTypes.Bigtriad,
    PropTypes.Bigfan,
    PropTypes.Bigbuugeng,
    PropTypes.Bigdoublestar,
]

### LISTS FOR ITERATION ###

PropTypeslist = [
    PropTypes.Staff,
    PropTypes.Bigstaff,
    PropTypes.Club,
    PropTypes.Buugeng,
    PropTypes.Bigbuugeng,
    PropTypes.Fractalgeng,
    PropTypes.Fan,
    PropTypes.Bigfan,
    PropTypes.Triad,
    PropTypes.Bigtriad,
    PropTypes.Minihoop,
    PropTypes.Bighoop,
    PropTypes.Doublestar,
    PropTypes.Bigdoublestar,
    PropTypes.Quiad,
    PropTypes.Sword,
    PropTypes.Guitar,
    PropTypes.Ukulele,
    PropTypes.Chicken,
]
