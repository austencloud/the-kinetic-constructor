from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItem

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowUpdater:
    def __init__(self, arrow: "Arrow") -> None:
        self.a = arrow

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.a.attr_manager.update_attributes(arrow_dict)
            if not self.a.is_ghost and self.a.ghost:
                self.a.ghost.attr_manager.update_attributes(arrow_dict)
        if not self.a.is_ghost:
            self.a.ghost.transform = self.a.transform
        self.a.svg_manager.update_svg()
        self.a.mirror_manager.update_mirror()
        self.a.svg_manager.update_color()
        self.a.location_calculator.update_location()
        self.a.rot_angle_calculator.update_rotation()
