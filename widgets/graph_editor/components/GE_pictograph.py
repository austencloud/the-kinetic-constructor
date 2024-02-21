from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_pictograph import GE_BlankPictograph


class GE_BlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)


class GE_PictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", blank_pictograph: "GE_BlankPictograph"
    ) -> None:
        super().__init__(blank_pictograph)
        self.GE = GE
        self.blank_pictograph = blank_pictograph
        self.main_widget = GE.main_widget
        self.setScene(blank_pictograph)

        # Set the frame shape to NoFrame
        self.setFrameShape(PictographView.Shape.Box)

    def resize_GE_pictograph_view(self):
        self.setMinimumHeight(self.GE.height())
        self.setMinimumWidth(self.GE.height())

        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.blank_pictograph)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())  # Use the viewport to draw over the content
        pen = QPen(Qt.GlobalColor.black, 0)  # Set the color and width of the border
        painter.setPen(pen)

        right_edge = self.viewport().width() - 1
        painter.drawLine(right_edge, 0, right_edge, self.viewport().height())

    def get_current_pictograph(self) -> Pictograph:
        return self.scene()