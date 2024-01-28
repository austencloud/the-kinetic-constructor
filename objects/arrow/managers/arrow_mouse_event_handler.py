from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *

from utilities.TypeChecking.TypeChecking import TYPE_CHECKING


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowMouseEventHandler:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def handle_mouse_press(self, event) -> None:
        self.arrow.pictograph.mouse_event_handler.clear_selections()
        self.arrow.pictograph.selected_arrow = self.arrow
        self.arrow.setSelected(True)
        if hasattr(self.arrow, GHOST) and self.arrow.ghost:
            self.arrow.ghost.show()
        self.arrow.scene.updater.update_pictograph()



    def handle_mouse_release(self, event) -> None:
        self.arrow.scene.arrows[self.arrow.color] = self.arrow
        self.arrow.scene.updater.update_pictograph()
        self.arrow.ghost.hide()

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.arrow.setPos(new_pos)
