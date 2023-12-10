from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING

from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox
    from widgets.graph_editor.graph_editor import GraphEditor


class PropBoxView(ObjectBoxView):
    def __init__(self, propbox: "PropBox", graph_editor: "GraphEditor") -> None:
        super().__init__(propbox, graph_editor)

        self.setScene(propbox)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.propbox = propbox

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)