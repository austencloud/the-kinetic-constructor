from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from widgets.sequence_recorder.SR_beat_frame import (
    SR_BeatFrame,
)
from widgets.sequence_recorder.SR_video_display_frame import (
    SR_VideoDisplayFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder.sequence_recorder import (
        SequenceRecorder,
    )


class SR_CaptureFrame(QWidget):
    def __init__(self, sequence_recorder: "SequenceRecorder") -> None:
        super().__init__()
        self.main_widget = sequence_recorder.main_widget
        self.sequence_recorder = sequence_recorder
        self.sequence_beat_frame = SR_BeatFrame(self)
        self.video_display_frame = SR_VideoDisplayFrame(self)
        self._setup_layout()
        # self.setStyleSheet("border: 1px solid black;")

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
        self.video_display_frame.resize_video_display_frame()
        self.setFixedSize(size * 2, size)
