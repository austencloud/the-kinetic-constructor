from enum import Enum, auto
from enum import Enum


class PropType(Enum):
    Hand = auto()
    Staff = auto()
    BigStaff = auto()
    Club = auto()
    Buugeng = auto()
    BigBuugeng = auto()
    Fractalgeng = auto()
    EightRings = auto()
    BigEightRings = auto()
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
        for prop_type_enum in PropType:
            if str(prop_type_enum.name) == prop_type_value:
                return prop_type_enum


big_unilateral_prop_types = [
    PropType.BigHoop,
    PropType.Guitar,
    PropType.Sword,
    PropType.Chicken,
]
small_unilateral_prop_types = [
    PropType.Fan,
    PropType.Club,
    PropType.MiniHoop,
    PropType.Triad,
    PropType.Ukulele,
]
big_bilateral_prop_types = [
    PropType.BigStaff,
    PropType.BigBuugeng,
    PropType.BigDoubleStar,
    PropType.BigEightRings,
]
small_bilateral_prop_types = [
    PropType.Staff,
    PropType.Buugeng,
    PropType.DoubleStar,
    PropType.Quiad,
    PropType.Fractalgeng,
    PropType.EightRings,
]
non_strictly_placed_props = [
    PropType.Staff,
    PropType.Fan,
    PropType.Club,
    PropType.Buugeng,
    PropType.MiniHoop,
    PropType.Triad,
    PropType.Quiad,
    PropType.Ukulele,
    PropType.Chicken,
    PropType.Fractalgeng,
    PropType.EightRings,
    PropType.BigEightRings,
]
strictly_placed_props = [
    PropType.BigHoop,
    PropType.DoubleStar,
    PropType.BigBuugeng,
    PropType.BigDoubleStar,
]

### LISTS FOR ITERATION ###

PropTypesList = [
    PropType.Staff,
    PropType.BigStaff,
    PropType.Club,
    PropType.Buugeng,
    PropType.BigBuugeng,
    PropType.Fractalgeng,
    PropType.Fan,
    PropType.Triad,
    PropType.MiniHoop,
    PropType.BigHoop,
    PropType.DoubleStar,
    PropType.BigDoubleStar,
    PropType.Quiad,
    PropType.Sword,
    PropType.Guitar,
    PropType.Ukulele,
    PropType.Chicken,
]
