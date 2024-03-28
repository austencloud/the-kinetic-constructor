from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from PyQt6.QtCore import QTimer
import cv2


from widgets.sequence_recorder_widget.recording_frame import RecordingFrame
from widgets.sequence_recorder_widget.sequence_recorder_beat_frame import (
    SequenceRecorderBeatFrame,
)
from widgets.sequence_recorder_widget.sequence_recorder_video_controls import (
    SequenceRecorderVideoControls,
)
from widgets.sequence_recorder_widget.sequence_recorder_video_display import (
    SequenceRecorderVideoDisplay,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget

        self.sequence_beat_frame = SequenceRecorderBeatFrame(self)
        self.video_display = SequenceRecorderVideoDisplay(self)
        self.video_controls = SequenceRecorderVideoControls()
        self.recording_frame = RecordingFrame(
            self.sequence_beat_frame, self.video_display
        )
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.addWidget(self.recording_frame)
        self.main_layout.addWidget(self.video_controls)

    def resize_sequence_recorder_widget(self) -> None:
        self.sequence_beat_frame.resize_beat_frame()
        self.video_display.resize_video_display()
