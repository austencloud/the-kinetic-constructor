from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *

from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING
)


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowMouseEventHandler:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def handle_mouse_press(self, event) -> None:
        self.arrow.pictograph.clear_selections()
        self.arrow.setSelected(True)
        if hasattr(self.arrow, GHOST) and self.arrow.ghost:
            self.arrow.ghost.show()

        self.arrow.scene.state_updater.update_pictograph()

    def hand_mouse_move(self, event: "QGraphicsSceneMouseEvent") -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_location = self.arrow.scene.grid.get_closest_layer2_point(
                event.scenePos()
            )[0]
            new_pos = event.scenePos() - self.arrow.get_center()
            self.arrow.set_drag_pos(new_pos)
            if new_location != self.arrow.loc:
                self.arrow.location_calculator.update_location(new_location)

    def handle_mouse_release(self, event) -> None:
        self.arrow.scene.arrows[self.arrow.color] = self.arrow
        self.arrow.scene.state_updater.update_pictograph()
        self.arrow.ghost.hide()
