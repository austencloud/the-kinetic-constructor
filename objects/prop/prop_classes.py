from typing import TYPE_CHECKING
from constants import *
from utilities.TypeChecking.prop_types import PropTypes

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from widgets.pictograph.pictograph import Pictograph

from objects.prop.prop import Prop


class Staff(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Staff
        super().__init__(pictograph, attributes, motion)


class BigStaff(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigStaff
        super().__init__(pictograph, attributes, motion)


class Triad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Triad
        super().__init__(pictograph, attributes, motion)


class BigTriad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigTriad
        super().__init__(pictograph, attributes, motion)


class MiniHoop(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.MiniHoop
        super().__init__(pictograph, attributes, motion)


class Fan(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Fan
        super().__init__(pictograph, attributes, motion)


class BigFan(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigFan
        super().__init__(pictograph, attributes, motion)


class Club(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Club
        super().__init__(pictograph, attributes, motion)


class Buugeng(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Buugeng
        super().__init__(pictograph, attributes, motion)


class BigBuugeng(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigBuugeng
        super().__init__(pictograph, attributes, motion)


class Fractalgeng(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Fractalgeng
        super().__init__(pictograph, attributes, motion)


class EightRings(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.EightRings
        super().__init__(pictograph, attributes, motion)


class DoubleStar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.DoubleStar
        super().__init__(pictograph, attributes, motion)


class BigHoop(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigHoop
        super().__init__(pictograph, attributes, motion)


class BigDoubleStar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.BigDoubleStar
        super().__init__(pictograph, attributes, motion)


class Quiad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Quiad
        super().__init__(pictograph, attributes, motion)


class Sword(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Sword
        super().__init__(pictograph, attributes, motion)


class Guitar(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Guitar
        super().__init__(pictograph, attributes, motion)


class Ukulele(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Ukulele
        super().__init__(pictograph, attributes, motion)


class Chicken(Prop):
    def __init__(self, pictograph: "Pictograph", attributes, motion: "Motion") -> None:
        attributes[PROP_TYPE] = PropTypes.Chicken
        super().__init__(pictograph, attributes, motion)
