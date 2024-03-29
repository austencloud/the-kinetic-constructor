from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QFrame
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


class SR_CaptureFrame(QFrame):
    def __init__(self, sequence_recorder: "SequenceRecorder") -> None:
        super().__init__()
        self.main_widget = sequence_recorder.main_widget
        self.sequence_recorder = sequence_recorder
        self.sequence_beat_frame = SR_BeatFrame(self)
        self.video_display_frame = SR_VideoDisplayFrame(self)
        self._setup_layout()

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
        size = int(self.sequence_recorder.height() * 0.8)
        self.sequence_beat_frame.setFixedSize(size, size)
        self.sequence_beat_frame.resize_beat_frame()
        self.video_display_frame.resize_video_display_frame()
        self.setFixedSize(size * 2, size)


    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            # Apply recording visual feedback to the entire capture frame
            self.setStyleSheet("border: 3px solid red;")
            # Start recording both frames
            self.start_recording()
        else:
            self.setStyleSheet("")
            # Stop recording and process the videos
            self.stop_recording()

    def start_recording(self):
        # Placeholder for starting the recording logic
        pass

    def stop_recording(self):
        # Placeholder for stopping the recording logic and processing videos
        pass