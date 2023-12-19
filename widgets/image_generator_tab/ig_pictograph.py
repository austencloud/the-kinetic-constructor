from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QScrollArea

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_scroll_area import IG_Scroll_Area


class IG_Pictograph(Pictograph):
    def __init__(self, main_widget, ig_scroll_area: "IG_Scroll_Area"):
        super().__init__(main_widget, "image_generator")
        self.view = IG_Pictograph_View(self)
        self.ig_scroll_area = ig_scroll_area


class IG_Pictograph_View(QGraphicsView):
    def __init__(self, ig_pictograph: IG_Pictograph) -> None:
        super().__init__(ig_pictograph)
        self.ig_pictograph = ig_pictograph

    def resize_pictograph(self) -> None:
        view_width = int(
            self.ig_pictograph.ig_scroll_area.width() / 4
        ) - self.ig_pictograph.ig_scroll_area.spacing * (
            self.ig_pictograph.ig_scroll_area.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(int(view_width * 90 / 75))
        self.setMaximumHeight(int(view_width * 90 / 75))

        self.view_scale = view_width / self.ig_pictograph.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
