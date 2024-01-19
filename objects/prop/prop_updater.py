from typing import TYPE_CHECKING, Dict, Union

from utilities.TypeChecking.MotionAttributes import Colors, Locations, Orientations

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropUpdater:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def update_prop(
        self, prop_dict: Dict[str, Union[Colors, Locations, Orientations]] = None
    ) -> None:
        if prop_dict:
            self.prop.attr_manager.update_attributes(prop_dict)
        self.prop.svg_manager.update_svg()
        self.prop.svg_manager.update_color()
        self.prop.rot_angle_manager.update_prop_rot_angle()
