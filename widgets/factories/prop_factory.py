from objects.prop.prop_classes import *
from utilities.TypeChecking.prop_types import PropTypes


class PropFactory:
    def __init__(self):
        self.prop_classes = {
            STAFF: Staff,
            BIGSTAFF: BigStaff,
            TRIAD: Triad,
            BIGTRIAD: BigTriad,
            MINIHOOP: MiniHoop,
            FAN: Fan,
            BIGFAN: BigFan,
            CLUB: Club,
            BUUGENG: Buugeng,
            BIGBUUGENG: BigBuugeng,
            FRACTALGENG: Fractalgeng,
            DOUBLESTAR: DoubleStar,
            BIGHOOP: BigHoop,
            BIGDOUBLESTAR: BigDoubleStar,
            QUIAD: Quiad,
            SWORD: Sword,
            GUITAR: Guitar,
            UKULELE: Ukulele,
            CHICKEN: Chicken,
        }

    def create_prop_of_type(
        self, existing_prop: Prop, target_prop_type: PropTypes
    ) -> Prop:
        # if the prop type is a str, use it If it's an enum use the name
        if isinstance(target_prop_type, str):
            target_prop_type = PropTypes[target_prop_type]
        elif isinstance(target_prop_type, PropTypes):
            target_prop_type = target_prop_type
        if target_prop_type.name.lower() in self.prop_classes:
            return self.prop_classes[target_prop_type.name.lower()](
                existing_prop.pictograph, existing_prop.prop_dict, existing_prop.motion
            )
        else:
            raise ValueError(f"Unknown prop type: {target_prop_type}")
