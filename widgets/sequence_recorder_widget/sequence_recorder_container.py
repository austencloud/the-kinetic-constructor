from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize, Qt

from widgets.sequence_recorder_widget.sequence_recorder_widget import SequenceRecorderWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderContainer(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.layout = QVBoxLayout(self)
        self.sequence_recorder_widget = SequenceRecorderWidget(self.main_widget)
        self.layout.addWidget(self.sequence_recorder_widget)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
