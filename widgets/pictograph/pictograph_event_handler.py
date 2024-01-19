from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent


class PictographMouseEventHandler:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def handle_mouse_press(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = event.scenePos()
        items_at_pos = self.p.items(scene_pos)

        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)
        if arrow:
            self.p.selected_arrow = arrow
            self.p.dragged_arrow = arrow
            self.p.dragged_arrow.mousePressEvent(event)
        else:
            prop = next((item for item in items_at_pos if isinstance(item, Prop)), None)
            if prop:
                self.p.dragged_prop = prop
                self.p.dragged_prop.mousePressEvent(event)
            else:
                self.pictograph.clear_selections()

    def handle_mouse_move(self, event) -> None:
        if self.p.dragged_prop:
            self.p.dragged_prop.mouseMoveEvent(event)
        elif self.p.dragged_arrow:
            self.p.dragged_arrow.mouseMoveEvent(event)

    def handle_mouse_release(self, event) -> None:
        if self.p.dragged_prop:
            self.p.dragged_prop.mouseReleaseEvent(event)
            self.p.dragged_prop = None
        elif self.p.dragged_arrow:
            self.p.dragged_arrow.mouseReleaseEvent(event)
            self.p.dragged_arrow = None

    def clear_selections(self) -> None:
        for arrow in self.p.arrows.values():
            arrow.setSelected(False)
        for prop in self.p.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None
