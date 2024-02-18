from enum import Enum, auto
from enum import Enum

class PropTypes(Enum):
    Staff = auto()
    BigStaff = auto()
    Club = auto()
    Buugeng = auto()
    BigBuugeng = auto()
    Fractalgeng = auto()
    EightRings = auto()
    Fan = auto()
    Triad = auto()
    MiniHoop = auto()
    BigHoop = auto()
    DoubleStar = auto()
    BigDoubleStar = auto()
    Quiad = auto()
    Sword = auto()
    Guitar = auto()
    Ukulele = auto()
    Chicken = auto()

    def get_prop_type(prop_type_value):
        for prop_type_enum in PropTypes:
            if str(prop_type_enum.name) == prop_type_value:
                return prop_type_enum

big_unilateral_prop_types = [
    PropTypes.BigHoop,
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
    PropTypes.EightRings,
]
non_strictly_placed_props = [
    PropTypes.Staff,
    PropTypes.Fan,
    PropTypes.Club,
    PropTypes.Buugeng,
    PropTypes.MiniHoop,
    PropTypes.Triad,
    PropTypes.Quiad,
    PropTypes.Ukulele,
    PropTypes.Chicken,
    PropTypes.Fractalgeng,
    PropTypes.EightRings,
]
strictly_placed_props = [
    PropTypes.BigHoop,
    PropTypes.DoubleStar,
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
    PropTypes.Triad,
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
