from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.view: "BeatView" = None


class BeatView(QGraphicsView):
    original_style: str

    def __init__(self, beat_frame: "BeatFrame") -> None:
        super().__init__(beat_frame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.beat: "Beat" = None
        self.is_filled = False

    def set_pictograph(self, new_beat: "Beat") -> None:
        self.beat = new_beat
        new_beat.view = self
        self.setScene(self.beat)
        view_width = self.height()
        self.view_scale = view_width / self.beat.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button
