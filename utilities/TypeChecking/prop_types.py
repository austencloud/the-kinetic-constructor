from enum import Enum, auto
from enum import Enum

class PropTypes(Enum):
    Staff = auto()
    BigStaff = auto()
    Club = auto()
    Buugeng = auto()
    BigBuugeng = auto()
    Fractalgeng = auto()
    Fan = auto()
    BigFan = auto()
    Triad = auto()
    BigTriad = auto()
    MiniHoop = auto()
    BigHoop = auto()
    DoubleStar = auto()
    BigDoubleStar = auto()
    Quiad = auto()
    Sword = auto()
    Guitar = auto()
    Ukulele = auto()
    Chicken = auto()

big_unilateral_prop_types = [
    PropTypes.BigHoop,
    PropTypes.BigFan,
    PropTypes.BigTriad,
    PropTypes.Guitar,
    PropTypes.Sword,
    PropTypes.Chicken,
]
small_unilateral_prop_types = [
    PropTypes.Fan,
    PropTypes.Club,
    PropTypes.MiniHoop,
    PropTypes.Triad,
    PropTypes.Ukulele,
]
big_bilateral_prop_types = [
    PropTypes.BigStaff,
    PropTypes.BigBuugeng,
    PropTypes.BigDoubleStar,
]
small_bilateral_prop_types = [
    PropTypes.Staff,
    PropTypes.Buugeng,
    PropTypes.DoubleStar,
    PropTypes.Quiad,
    PropTypes.Fractalgeng,
]
non_strictly_placed_props = [
    PropTypes.Staff,
    PropTypes.Fan,
    PropTypes.BigFan,
    PropTypes.Club,
    PropTypes.Buugeng,
    PropTypes.MiniHoop,
    PropTypes.Triad,
    PropTypes.Quiad,
    PropTypes.Ukulele,
    PropTypes.Chicken,
    PropTypes.Fractalgeng,
]
strictly_placed_props = [
    PropTypes.BigHoop,
    PropTypes.DoubleStar,
    PropTypes.BigTriad,
    PropTypes.BigFan,
    PropTypes.BigBuugeng,
    PropTypes.BigDoubleStar,
]

### LISTS FOR ITERATION ###

PropTypeslist = [
    PropTypes.Staff,
    PropTypes.BigStaff,
    PropTypes.Club,
    PropTypes.Buugeng,
    PropTypes.BigBuugeng,
    PropTypes.Fractalgeng,
    PropTypes.Fan,
    PropTypes.BigFan,
    PropTypes.Triad,
    PropTypes.BigTriad,
    PropTypes.MiniHoop,
    PropTypes.BigHoop,
    PropTypes.DoubleStar,
    PropTypes.BigDoubleStar,
    PropTypes.Quiad,
    PropTypes.Sword,
    PropTypes.Guitar,
    PropTypes.Ukulele,
    PropTypes.Chicken,
]
