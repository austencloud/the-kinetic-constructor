from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.propbox.propbox import PropBox


class PropBoxView(QGraphicsView):
    def __init__(self, propbox: "PropBox") -> None:
        super().__init__()
        self.setFixedSize(
            int(propbox.main_window.height() * 1/3 / 2),
            int(propbox.main_window.height() * 1/3 / 2),
        )
        self.setScene(propbox)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None

        self.scale(0.2, 0.2)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)