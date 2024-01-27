from typing import TYPE_CHECKING, Union

from utilities.TypeChecking.MotionAttributes import Colors, Locations, Orientations

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropUpdater:
    def __init__(self, prop: "Prop") -> None:
        self.p = prop
        self.svg_file = self.p.svg_manager.get_svg_file()
        self.p.svg_manager.setup_svg_renderer(self.svg_file)

    def update_prop(
        self, prop_dict: dict[str, Union[Colors, Locations, Orientations]] = None
    ) -> None:
        if prop_dict:
            self.p.attr_manager.update_attributes(prop_dict)
        self.p.svg_manager.update_svg()
        self.p.svg_manager.update_color()
        self.p.rot_angle_manager.update_prop_rot_angle()
