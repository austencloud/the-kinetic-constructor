from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from typing import TYPE_CHECKING
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from widgets.pictograph.components.pictograph_view import PictographView


class PictographViewMouseEventHandler:
    def __init__(self, pictograph_view: "PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph

    def handle_mouse_press(self, event: "QMouseEvent") -> None:
        if self.pictograph.check.is_in_sequence_builder():
            self.pictograph.scroll_area.sequence_builder.option_click_handler.on_option_clicked(
                self.pictograph
            )
            return
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)
        
        if arrow:
            self.pictograph.selected_arrow = arrow
            arrow.setSelected(True)
            self.pictograph.update()
        else:
            prop = next((item for item in items_at_pos if isinstance(item, Prop)), None)
            if prop:
                self.pictograph.dragged_prop = prop
                self.pictograph.dragged_prop.mousePressEvent(event)
            else:
                self.clear_selections()

    def handle_mouse_move(self, event) -> None:
        if self.pictograph.dragged_prop:
            self.pictograph.dragged_prop.mouseMoveEvent(event)
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseMoveEvent(event)

    def handle_mouse_release(self, event) -> None:
        if self.pictograph.dragged_prop:
            self.pictograph.dragged_prop.mouseReleaseEvent(event)
            self.pictograph.dragged_prop = None
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseReleaseEvent(event)
            self.pictograph.dragged_arrow = None

    def clear_selections(self) -> None:
        for arrow in self.pictograph.arrows.values():
            arrow.setSelected(False)
        for prop in self.pictograph.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None
