from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_beat_frame import (
        SequenceRecorderBeatFrame,
    )
    from widgets.sequence_recorder_widget.sequence_recorder_video_display import (
        SequenceRecorderVideoDisplay,
    )


class RecordingFrame(QWidget):
    def __init__(
        self,
        sequence_beat_frame: "SequenceRecorderBeatFrame",
        video_display: "SequenceRecorderVideoDisplay",
    ) -> None:
        super().__init__()
        self.sequence_beat_frame = sequence_beat_frame
        self.video_display = video_display
        self.init_ui()
        # add black borders around edges
        self.setStyleSheet("border: 1px solid black;")

    def init_ui(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sequence_beat_frame, 1)
        self.layout.addWidget(self.video_display, 1)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def resize_recording_frame(self):
        parent_width = self.parentWidget().width()
        recording_frame_width = parent_width / 1.3

        width = int(recording_frame_width // 2)
        height = int(self.parentWidget().height() // 1.75)

        self.sequence_beat_frame.setFixedSize(height, height)
        self.sequence_beat_frame.resize_beat_frame()
        self.video_display.setFixedSize(height, height)
        self.video_display.resize_video_display()
