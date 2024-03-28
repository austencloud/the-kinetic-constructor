from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from widgets.sequence_recorder_widget.sequence_recorder_beat_frame import (
    SequenceRecorderBeatFrame,
)
from widgets.sequence_recorder_widget.sequence_recorder_video_display_frame import (
    SequenceRecorderVideoDisplayFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderCaptureFrame(QWidget):
    def __init__(self, sequence_recorder_widget: "SequenceRecorderWidget") -> None:
        super().__init__()
        self.main_widget = sequence_recorder_widget.main_widget
        self.sequence_recorder_widget = sequence_recorder_widget
        self.sequence_beat_frame = SequenceRecorderBeatFrame(self)
        self.video_display_frame = SequenceRecorderVideoDisplayFrame(self)
        self._setup_layout()
        self.setStyleSheet("border: 1px solid black;")

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sequence_beat_frame, 1)
        self.layout.addWidget(self.video_display_frame, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def resize_capture_frame(self) -> None:
        size = int(self.parentWidget().height() // 1.75)
        self.sequence_beat_frame.setFixedSize(size, size)
        self.sequence_beat_frame.resize_beat_frame()
        self.video_display_frame.setFixedSize(size, size)
        self.video_display_frame.resize_video_display_frame()
