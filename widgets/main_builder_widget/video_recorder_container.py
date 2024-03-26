from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize, Qt

from widgets.main_builder_widget.sequence_recorder_widget import VideoRecorderWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class VideoRecorderContainer(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.layout = QVBoxLayout(self)
        self.sequence_recorder_widget = VideoRecorderWidget(self)
        self.layout.addWidget(self.sequence_recorder_widget)
        self.setLayout(self.layout)

        # This policy allows the widget to expand and fill available space.
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
