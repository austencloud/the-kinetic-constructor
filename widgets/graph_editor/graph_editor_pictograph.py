from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor_pictograph import GraphEditorPictograph


class GraphEditorPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)
        self.main_widget = graph_editor.main_widget
        self.graph_editor = graph_editor
        self.get.initiallize_getter()


class GraphEditorPictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", GE_pictograph: "GraphEditorPictograph"
    ) -> None:
        super().__init__(GE_pictograph)
        self.GE = GE
        self.main_widget = GE.main_widget
        self.setScene(GE_pictograph)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_GE_pictograph_view(self):
        self.setMinimumHeight(self.GE.height())
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
