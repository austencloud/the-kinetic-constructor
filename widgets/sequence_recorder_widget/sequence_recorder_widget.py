import math
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer
from .sequence_recorder_capture_frame import SequenceRecorderCaptureFrame
from .sequence_recorder_main_control_frame import SequenceRecorderMainControlFrame

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.capture_frame = SequenceRecorderCaptureFrame(self)
        self.video_control_frame = SequenceRecorderMainControlFrame(self)
        self._setup_layout()

        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(100)

    def animate_background(self) -> None:
        self.gradient_shift += 0.05
        self.color_shift += 1
        if self.color_shift > 360:
            self.color_shift = 0
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        for i in range(10):
            pos = i / 10
            hue = int((self.color_shift + pos * 100) % 360)
            color = QColor.fromHsv(hue, 255, 255, 150)
            adjusted_pos = pos + math.sin(self.gradient_shift + pos * math.pi) * 0.05
            clamped_pos = max(0, min(adjusted_pos, 1))
            gradient.setColorAt(clamped_pos, color)

        painter.fillRect(self.rect(), gradient)

    def _setup_layout(self) -> None:
        capture_layout_hbox = QHBoxLayout()
        capture_layout_hbox.addStretch(1)
        capture_layout_hbox.addWidget(self.capture_frame)
        capture_layout_hbox.addStretch(1)

        video_control_hbox = QHBoxLayout()
        video_control_hbox.addStretch(1)
        video_control_hbox.addWidget(self.video_control_frame)
        video_control_hbox.addStretch(1)

        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.addLayout(capture_layout_hbox)
        self.main_layout.addLayout(video_control_hbox)
        self.main_layout.addStretch(1)

    def resize_sequence_recorder_widget(self) -> None:
        self.capture_frame.resize_capture_frame()
        self.video_control_frame.resize_control_frame()
        self.capture_frame.sequence_beat_frame.populate_beat_frame_scenes_from_json()
