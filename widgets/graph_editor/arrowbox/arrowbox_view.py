from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.arrowbox.arrowbox import ArrowBox


class ArrowBoxView(QGraphicsView):
    def __init__(self, arrowbox: "ArrowBox") -> None:
        super().__init__(arrowbox)
        self.setFixedSize(
            int(arrowbox.main_window.height() * 1 / 6),
            int(arrowbox.main_window.height() * 1 / 6),
        )
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

