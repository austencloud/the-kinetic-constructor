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
    "eightrings": PropTypes.EightRings,
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
            prop_type_enum = string_to_enum_map[prop.prop_type]

            if prop_type_enum in big_unilateral_prop_types:
                self.big_uni.append(prop)
            elif prop_type_enum in small_unilateral_prop_types:
                self.small_uni.append(prop)
            elif prop_type_enum in small_bilateral_prop_types:
                self.small_bi.append(prop)
            elif prop_type_enum in big_bilateral_prop_types:
                self.big_bi.append(prop)

        self.big_props = self.big_uni + self.big_bi
        self.small_props = self.small_uni + self.small_bi
