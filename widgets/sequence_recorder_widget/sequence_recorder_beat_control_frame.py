from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QSlider,
    QWidget,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_main_control_frame import (
        SequenceRecorderMainControlFrame,
    )


class SequenceRecorderBeatControlFrame(QWidget):
    def __init__(self, control_frame: "SequenceRecorderMainControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.sequence_recorder_widget = self.control_frame.sequence_recorder_widget
        self.capture_frame = self.sequence_recorder_widget.capture_frame
        self.beat_frame = self.capture_frame.sequence_beat_frame
        self.selection_manager = self.beat_frame.selection_manager
        self.init_ui()

    def init_ui(self) -> None:
        self._setup_bpm_slider()
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bpm_slider)

    def _setup_bpm_slider(self) -> None:
        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(180)
        self.bpm_slider.valueChanged.connect(self.adjust_bpm)

    def adjust_bpm(self, bpm):
        self.selection_manager.set_bpm(bpm)

    def resize_beat_control_frame(self) -> None:
        width = self.control_frame.sequence_recorder_widget.capture_frame.width() // 2
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
