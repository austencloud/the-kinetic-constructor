from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.propbox.propbox import PropBox


class PropBoxView(QGraphicsView):
    def __init__(self, propbox: "PropBox") -> None:
        super().__init__()
        self.setFixedSize(
            int(propbox.main_window.height() * 1/6),
            int(propbox.main_window.height() * 1/6),
        )
        self.setScene(propbox)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.propbox = propbox

        self.setFrameStyle(
            QFrame.Shape.Box | QFrame.Shadow.Plain
        ) 
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)