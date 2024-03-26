from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize, Qt

from widgets.main_tab_widget.sequence_recorder_widget import VideoRecorderWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class VideoRecorderContainer(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:

        super().__init__()
        self.main_widget = main_widget
        self.layout = QVBoxLayout(self)
        self.sequence_recorder_widget = VideoRecorderWidget(main_widget)
        self.layout.addWidget(self.sequence_recorder_widget)
        self.setLayout(self.layout)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resize_video_container(self) -> None:
        main_tab_widget_width = self.main_widget.main_builder_widget.width()
        self.setMinimumWidth(int(main_tab_widget_width))
        self.setMaximumWidth(int(main_tab_widget_width))
