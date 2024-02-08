from typing import TYPE_CHECKING
from utilities.TypeChecking.prop_types import (
    PropTypes,
    big_unilateral_prop_types,
    small_unilateral_prop_types,
    small_bilateral_prop_types,
    big_bilateral_prop_types,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


string_to_enum_map = {
    "staff": PropTypes.Staff,
    "bigstaff": PropTypes.BigStaff,
    "club": PropTypes.Club,
    "buugeng": PropTypes.Buugeng,
    "bigbuugeng": PropTypes.BigBuugeng,
    "fractalgeng": PropTypes.Fractalgeng,
    "fan": PropTypes.Fan,
    "bigfan": PropTypes.BigFan,
    "triad": PropTypes.Triad,
    "bigtriad": PropTypes.BigTriad,
    "minihoop": PropTypes.MiniHoop,
    "bighoop": PropTypes.BigHoop,
    "doublestar": PropTypes.DoubleStar,
    "bigdoublestar": PropTypes.BigDoubleStar,
    "quiad": PropTypes.Quiad,
    "sword": PropTypes.Sword,
    "guitar": PropTypes.Guitar,
    "ukulele": PropTypes.Ukulele,
    "chicken": PropTypes.Chicken,

    # Add mappings for the rest of your prop types
}

class PropClassifier:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.classify_props()

    def classify_props(self) -> None:
        self.big_uni = []
        self.small_uni = []
        self.small_bi = []
        self.big_bi = []

        for prop in self.pictograph.props.values():
            # Convert string prop_type to enum member
            enum_prop_type = string_to_enum_map.get(prop.prop_type)  # Use .lower() to handle case differences
            if not enum_prop_type:
                continue  # Skip if prop_type is not recognized

            if enum_prop_type in big_unilateral_prop_types:
                self.big_uni.append(prop)
            elif enum_prop_type in small_unilateral_prop_types:
                self.small_uni.append(prop)
            elif enum_prop_type in small_bilateral_prop_types:
                self.small_bi.append(prop)
            elif enum_prop_type in big_bilateral_prop_types:
                self.big_bi.append(prop)

        self.big_props = self.big_uni + self.big_bi
        self.small_props = self.small_uni + self.small_bi