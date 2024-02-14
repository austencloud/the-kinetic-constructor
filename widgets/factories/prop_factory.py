from objects.prop.prop_classes import *
from Enums.PropTypes import PropTypes


class PropFactory:
    def __init__(self):
        self.prop_classes = {
            PropTypes.Staff.name.lower(): Staff,
            PropTypes.BigStaff.name.lower(): BigStaff,
            PropTypes.Triad.name.lower(): Triad,
            PropTypes.BigTriad.name.lower(): BigTriad,
            PropTypes.MiniHoop.name.lower(): MiniHoop,
            PropTypes.Fan.name.lower(): Fan,
            PropTypes.BigFan.name.lower(): BigFan,
            PropTypes.Club.name.lower(): Club,
            PropTypes.Buugeng.name.lower(): Buugeng,
            PropTypes.BigBuugeng.name.lower(): BigBuugeng,
            PropTypes.Fractalgeng.name.lower(): Fractalgeng,
            PropTypes.EightRings.name.lower(): EightRings,
            PropTypes.DoubleStar.name.lower(): DoubleStar,
            PropTypes.BigHoop.name.lower(): BigHoop,
            PropTypes.BigDoubleStar.name.lower(): BigDoubleStar,
            PropTypes.Quiad.name.lower(): Quiad,
            PropTypes.Sword.name.lower(): Sword,
            PropTypes.Guitar.name.lower(): Guitar,
            PropTypes.Ukulele.name.lower(): Ukulele,
            PropTypes.Chicken.name.lower(): Chicken,
        }

    def create_prop_of_type(
        self, existing_prop: Prop, target_prop_type: PropTypes
    ) -> Prop:
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
