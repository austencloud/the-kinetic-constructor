from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor_widget.object_panel.objectbox import ObjectBox
    from widgets.graph_editor_widget.graph_editor import GraphEditor


class ObjectBoxView(QGraphicsView):
    def __init__(self, objectbox: "ObjectBox", graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.graph_editor = graph_editor
        self.setScene(objectbox)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.objectbox = objectbox

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setMinimumWidth(int(self.graph_editor.main_pictograph.view.height() / 2))
        self.setMaximumWidth(int(self.graph_editor.main_pictograph.view.height() / 2))
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
