from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)

from widgets.sequence_recorder_widget.sequence_recorder_beat_control_frame import (
    SequenceRecorderBeatControlFrame,
)
from widgets.sequence_recorder_widget.sequence_recorder_video_control_frame import (
    SequenceRecorderVideoControlFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderMainControlFrame(QWidget):
    def __init__(self, sequence_recorder_widget: "SequenceRecorderWidget") -> None:
        super().__init__()
        self.sequence_recorder_widget = sequence_recorder_widget
        self.init_ui()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def init_ui(self) -> None:
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_control_frame = SequenceRecorderVideoControlFrame(self)
        self.beat_control_frame = SequenceRecorderBeatControlFrame(self)

        self.layout.addWidget(self.beat_control_frame)
        self.layout.addWidget(self.video_control_frame)

    def resize_control_frame(self) -> None:
        width = self.sequence_recorder_widget.capture_frame.width()
        self.setMaximumWidth(width)
        self.video_control_frame.resize_video_control_frame()
        self.beat_control_frame.resize_beat_control_frame()
