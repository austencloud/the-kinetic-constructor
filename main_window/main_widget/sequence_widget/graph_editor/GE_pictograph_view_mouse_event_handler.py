from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph_view import (
        PictographView,
    )


class GE_PictographViewMouseEventHandler:
    def __init__(self, pictograph_view: "PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph

    def handle_mouse_press(self, event: "QMouseEvent") -> None:
        pictograph = self.pictograph_view.pictograph
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph.items(scene_pos)
        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)

        if arrow:
            if pictograph.selected_arrow == arrow:
                pictograph.selected_arrow.setSelected(False)
                pictograph.selected_arrow = None
            else:
                if pictograph.selected_arrow:
                    pictograph.selected_arrow.setSelected(False)
                pictograph.selected_arrow = arrow
                arrow.setSelected(True)
            pictograph.update()
        else:
            if pictograph.selected_arrow:
                pictograph.selected_arrow.setSelected(False)
                pictograph.selected_arrow = None
            pictograph.update()
        self.pictograph_view.repaint()
        

    def is_arrow_under_cursor(self, event: "QMouseEvent") -> bool:
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        return any(isinstance(item, Arrow) for item in items_at_pos)

    def clear_selections(self) -> None:
        for arrow in self.pictograph.arrows.values():
            arrow.setSelected(False)
        for prop in self.pictograph.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None
