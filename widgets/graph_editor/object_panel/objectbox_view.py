from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.objectbox import ObjectBox


class ObjectBoxView(QGraphicsView):
    def __init__(self, objectbox: "ObjectBox") -> None:
        super().__init__()
        self.setMinimumSize(
            int(objectbox.main_window.height() * 1 / 6),
            int(objectbox.main_window.height() * 1 / 6),
        )
        self.setScene(objectbox)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.objectbox = objectbox

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
