from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)

from widgets.sequence_recorder.SR_beat_control_frame import (
    SR_BeatControlFrame,
)
from widgets.sequence_recorder.SR_video_control_frame import (
    SR_VideoControlFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder.sequence_recorder import (
        SequenceRecorder,
    )


class SR_MainControlFrame(QWidget):
    def __init__(self, sequence_recorder: "SequenceRecorder") -> None:
        super().__init__()
        self.sequence_recorder = sequence_recorder
        self.init_ui()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def init_ui(self) -> None:
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)

        self.video_control_frame = SR_VideoControlFrame(self)
        self.beat_control_frame = SR_BeatControlFrame(self)

        self.layout.addWidget(self.beat_control_frame)
        self.layout.addWidget(self.video_control_frame)

    def resize_control_frame(self) -> None:
        self.video_control_frame.resize_video_control_frame()
        self.beat_control_frame.resize_beat_control_frame()
