from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.objectbox import ObjectBox
    from widgets.graph_editor.graph_editor import GraphEditor


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
        objectbox_size = self.graph_editor.height() / 2
        self.setMaximumSize(int(objectbox_size), int(objectbox_size))
        self.setMinimumSize(int(objectbox_size), int(objectbox_size))