from typing import TYPE_CHECKING, Union

from Enums.MotionAttributes import  Location, Orientations

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropUpdater:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop
        self.svg_file = (
            self.prop.pictograph.main_widget.graphical_object_svg_manager.get_svg_file(
                prop
            )
        )
        self.prop.setFlag(self.prop.GraphicsItemFlag.ItemIsSelectable, False)

    def update_prop(
        self, prop_dict: dict[str, Union[str, Location, Orientations]] = None
    ) -> None:

        if prop_dict:
            self.prop.attr_manager.update_attributes(prop_dict)
        self.prop.pictograph.main_widget.graphical_object_svg_manager.update_svg(
            self.prop
        )
        self.prop.rot_angle_manager.update_prop_rot_angle()
