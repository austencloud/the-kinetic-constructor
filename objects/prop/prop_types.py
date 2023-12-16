from typing import TYPE_CHECKING
from constants.string_constants import *

if TYPE_CHECKING:
    from objects.motion import Motion
    from objects.pictograph.pictograph import Pictograph

from objects.prop.prop import Prop


class Staff(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = STAFF
        super().__init__(pictograph, attributes, motion)


class BigStaff(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = BIGSTAFF
        super().__init__(pictograph, attributes, motion)


class Triad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = TRIAD
        super().__init__(pictograph, attributes, motion)


class MiniHoop(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = MINIHOOP
        super().__init__(pictograph, attributes, motion)


class Fan(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = FAN
        super().__init__(pictograph, attributes, motion)


class Club(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = CLUB
        super().__init__(pictograph, attributes, motion)


class Buugeng(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = BUUGENG
        super().__init__(pictograph, attributes, motion)


class DoubleStar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = DOUBLESTAR
        super().__init__(pictograph, attributes, motion)


class BigHoop(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = BIGHOOP
        super().__init__(pictograph, attributes, motion)


class BigDoubleStar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = BIGDOUBLESTAR
        super().__init__(pictograph, attributes, motion)


class Quiad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = QUIAD
        super().__init__(pictograph, attributes, motion)


class Sword(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = SWORD
        super().__init__(pictograph, attributes, motion)


class Guitar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = GUITAR
        super().__init__(pictograph, attributes, motion)


class Ukulele(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = UKULELE
        super().__init__(pictograph, attributes, motion)


class Chicken(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = CHICKEN
        super().__init__(pictograph, attributes, motion)
