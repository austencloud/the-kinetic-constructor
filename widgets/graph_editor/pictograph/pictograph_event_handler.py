from PyQt6.QtGui import QTransform

from objects.letter_item import LetterItem
from objects.arrow import Arrow
from objects.grid import Grid
from objects.props.props import Staff
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent


class PictographEventHandler:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def handle_mouse_press(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = event.scenePos()
        items_at_pos = self.pictograph.items(scene_pos)

        arrows_at_pos = [item for item in items_at_pos if isinstance(item, Arrow)]

        closest_arrow = None
        min_distance = float("inf")
        for arrow in arrows_at_pos:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance

        if closest_arrow:
            self.pictograph.dragged_arrow = closest_arrow
            self.pictograph.dragged_arrow.mousePressEvent(event)
        else:
            clicked_item = self.pictograph.itemAt(scene_pos, QTransform())
            self.handle_non_arrow_click(clicked_item, event)

    def handle_non_arrow_click(self, clicked_item, event) -> None:
        if isinstance(clicked_item, Staff):
            self.pictograph.dragged_staff = clicked_item
            self.pictograph.dragged_staff.mousePressEvent(event)
        elif isinstance(clicked_item, LetterItem):
            clicked_item.setSelected(False)
            self.pictograph.clear_selections()
        elif not clicked_item or isinstance(clicked_item, Grid):
            self.pictograph.clear_selections()

    def handle_mouse_move(self, event) -> None:
        if self.pictograph.dragged_staff:
            self.pictograph.dragged_staff.mouseMoveEvent(event)
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseMoveEvent(event)

    def handle_mouse_release(self, event) -> None:
        if self.pictograph.dragged_staff:
            self.pictograph.dragged_staff.mouseReleaseEvent(event)
            self.pictograph.dragged_staff = None
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseReleaseEvent(event)
            self.pictograph.dragged_arrow = None

    def handle_context_menu(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = self.pictograph.view.mapToScene(event.pos().toPoint())
        items_at_pos = self.pictograph.items(scene_pos)

        clicked_item = None
        for item in items_at_pos:
            if isinstance(item, Arrow) or isinstance(item, Staff):
                clicked_item = item
                break

        if not clicked_item and items_at_pos:
            clicked_item = items_at_pos[0]

        event_pos = event.screenPos()
        self.pictograph.pictograph_menu_handler.create_master_menu(
            event_pos, clicked_item
        )
