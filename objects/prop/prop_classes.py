from Enums.PropTypes import PropType
from data.constants import PROP_TYPE
from objects.prop.prop import Prop

prop_types = [
    "Hand",
    "Staff",
    "BigStaff",
    "Triad",
    "MiniHoop",
    "Fan",
    "Club",
    "Buugeng",
    "BigBuugeng",
    "Fractalgeng",
    "EightRings",
    "BigEightRings",
    "DoubleStar",
    "BigHoop",
    "BigDoubleStar",
    "Quiad",
    "Sword",
    "Guitar",
    "Ukulele",
    "Chicken",
]

for prop_type in prop_types:

    def init(self, pictograph, attributes, motion, prop_type=prop_type):
        attributes[PROP_TYPE] = getattr(PropType, prop_type)
        super(type(self), self).__init__(pictograph, attributes, motion)

    prop_class = type(prop_type, (Prop,), {"__init__": init})
    globals()[prop_type] = prop_class
