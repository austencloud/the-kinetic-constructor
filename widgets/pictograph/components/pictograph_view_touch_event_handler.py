from typing import TYPE_CHECKING
from PyQt6.QtGui import QTouchEvent
from PyQt6.QtCore import QEvent, QPointF


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.codex.codex import Codex
    from widgets.pictograph.components.pictograph_view import PictographView


class PictographViewTouchEventHandler:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.codex = main_widget.main_tab_widget.codex

    def handle_touch_event(self, view: "PictographView", event: QTouchEvent):
        touch_points = event.points()
        if touch_points:
            point = touch_points[0]
            pos = point.position()
            global_pos = view.mapToGlobal(pos.toPoint())

            if self.is_touch_within_view(global_pos):
                if event.type() == QEvent.Type.TouchBegin:
                    self.set_gold_border()
                elif event.type() == QEvent.Type.TouchUpdate:
                    pass
                elif event.type() == QEvent.Type.TouchEnd:
                    view.mouse_event_handler.handle_mouse_press(event)

    def is_touch_within_view(self, view: "PictographView", global_pos: QPointF) -> bool:
        local_pos = view.mapFromGlobal(global_pos.toPoint())
        return view.rect().contains(local_pos)

    def set_gold_border(self, view: "PictographView"):
        view.pictograph.container.styled_border_overlay.set_gold_border()

    def find_view_under_touch(self, global_pos: QPointF) -> "PictographView":
        for section in self.codex.scroll_area.sections_manager.sections.values():
            for pictograph in section.pictographs.values():
                local_pos = pictograph.view.mapFromGlobal(global_pos.toPoint())
                if pictograph.view.rect().contains(local_pos):
                    return pictograph.view
        return None
