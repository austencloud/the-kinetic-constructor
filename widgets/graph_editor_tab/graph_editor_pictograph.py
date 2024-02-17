from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_pictograph import GraphEditorPictograph


class GraphEditorPictograph(Pictograph):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.graph_editor = graph_editor
        self.get.initiallize_getter()


class GraphEditorPictographView(PictographView):
    def __init__(self, graph_editor: "GraphEditor"):
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.add_black_borders()

    def add_black_borders(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
