from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QSlider,
    QWidget,
    QVBoxLayout,
    QFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder.SR_main_control_frame import (
        SR_MainControlFrame,
    )


class SR_BeatControlFrame(QFrame):
    def __init__(self, control_frame: "SR_MainControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.sequence_recorder = self.control_frame.sequence_recorder
        self.capture_frame = self.sequence_recorder.capture_frame
        self.beat_frame = self.capture_frame.sequence_beat_frame
        self.selection_manager = self.beat_frame.selection_manager
        self.init_ui()
        self.setStyleSheet("border: 1px solid black;")

    def init_ui(self) -> None:
        self._setup_bpm_slider()
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.bpm_slider)  # Add the frame to the layout

    def _setup_bpm_slider(self) -> None:
        self.bpm_slider = QSlider(
            Qt.Orientation.Horizontal
        )  # Set the frame as the parent of the slider
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(180)
        self.bpm_slider.valueChanged.connect(self.adjust_bpm)

    def adjust_bpm(self, bpm):
        self.selection_manager.set_bpm(bpm)

    def resize_beat_control_frame(self) -> None:
        width = self.beat_frame.width()
        height = width // 4
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
