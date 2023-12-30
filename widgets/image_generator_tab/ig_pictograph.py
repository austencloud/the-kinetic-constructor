from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_scroll import IGScrollArea


class IGPictograph(Pictograph):
    def __init__(self, main_widget, ig_scroll_area: "IGScrollArea"):
        super().__init__(main_widget, "ig_pictograph")
        self.view = IG_Pictograph_View(self)
        self.ig_scroll_area = ig_scroll_area


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
