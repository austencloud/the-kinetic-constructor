from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class BeatView(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pictograph: "Pictograph" = None
        # Initialize buttons

    def set_pictograph(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.setScene(self.pictograph)
        self.update_pictograph_size()

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def update_pictograph_size(self) -> None:
        view_width = int(self.height() * 75 / 90)
        self.setMinimumWidth(view_width)
        if self.pictograph:
            self.view_scale = view_width / self.pictograph.width()
            self.resetTransform()
            self.scale(self.view_scale, self.view_scale)
