import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from objects.arrow import Arrow
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt, QPointF
from objects.pictograph.position_engines.arrow_positioners.Type1_arrow_positioner import (
    Type1ArrowPositioner,
)

from objects.pictograph.position_engines.arrow_positioners.arrow_positioner import (
    ArrowPositioner,
)

if TYPE_CHECKING:
    from widgets.ig_tab.ig_scroll.ig_scroll import IGScrollArea


class IGPictograph(Pictograph):
    def __init__(self, main_widget, ig_scroll_area: "IGScrollArea"):
        super().__init__(main_widget, "ig_pictograph")
        self.view = IG_Pictograph_View(self)
        self.ig_scroll_area = ig_scroll_area
        self.selected_arrow = None  # New attribute for the selected arrow

    def handle_arrow_movement(self, key):
        if not self.selected_arrow:
            return

        adjustment_map = {
            Qt.Key.Key_W: QPointF(0, -5),
            Qt.Key.Key_A: QPointF(-5, 0),
            Qt.Key.Key_S: QPointF(0, 5),
            Qt.Key.Key_D: QPointF(5, 0),
        }
        adjustment = adjustment_map.get(key, QPointF(0, 0))
        self.selected_arrow.adjust_position(adjustment)
        self.update_arrow_adjustments_in_json()

    def update_arrow_adjustments_in_json(self):
        current_positioner = self.arrow_positioner.positioners.get(self.letter)
        if current_positioner:
            adjustments = current_positioner.load_adjustments()


class IG_Pictograph_View(QGraphicsView):
    def __init__(self, ig_pictograph: IGPictograph) -> None:
        super().__init__(ig_pictograph)
        self.ig_pictograph = ig_pictograph
        self.setScene(self.ig_pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_for_scroll_area(self) -> None:
        view_width = int(
            self.ig_pictograph.ig_scroll_area.width() / 4
        ) - self.ig_pictograph.ig_scroll_area.SPACING * (
            self.ig_pictograph.ig_scroll_area.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)

        self.view_scale = view_width / self.ig_pictograph.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.ig_pictograph.view_scale = self.view_scale

    def wheelEvent(self, event) -> None:
        self.ig_pictograph.ig_scroll_area.wheelEvent(event)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.ig_pictograph.handle_arrow_movement(event.key())
        else:
            super().keyPressEvent(event)
