from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
    from widgets.graph_editor.graph_editor import GraphEditor


class ArrowBoxView(ObjectBoxView):
    def __init__(self, arrowbox: "ArrowBox", graph_editor: "GraphEditor") -> None:
        super().__init__(arrowbox, graph_editor)
        self.setScene(arrowbox)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.arrowbox = arrowbox
        self.scene_width = self.arrowbox.width()

        self.setFrameStyle(
            QFrame.Shape.Box | QFrame.Shadow.Plain
        )  # Add black line around the frame

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def leaveEvent(self, event) -> None:
        self.arrowbox.dim_all_arrows()
