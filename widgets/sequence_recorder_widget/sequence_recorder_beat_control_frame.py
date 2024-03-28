from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
import cv2

from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QSlider,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_control_frame import (
        SequenceRecorderControlFrame,
    )
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderBeatControlFrame(QWidget):
    def __init__(self, control_frame: "SequenceRecorderControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.init_ui()

    def init_ui(self) -> None:
        self._setup_bpm_slider()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bpm_slider)

    def _setup_bpm_slider(self) -> None:
        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(180)

    def resize_beat_control_frame(self) -> None:
        width = self.control_frame.sequence_recorder_widget.capture_frame.width() // 2
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
