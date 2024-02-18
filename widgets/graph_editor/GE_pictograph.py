from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.GE_pictograph import GE_BlankPictograph


class GE_BlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)


class GE_PictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", blank_pictograph: "GE_BlankPictograph"
    ) -> None:
        super().__init__(blank_pictograph)
        self.GE = GE
        self.GE_pictograph = blank_pictograph
        self.main_widget = GE.main_widget
        self.setScene(blank_pictograph)

    def resize_GE_pictograph_view(self):
        self.setMinimumHeight(self.GE.height())
        self.setMinimumWidth(self.GE.height())
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.GE_pictograph)
