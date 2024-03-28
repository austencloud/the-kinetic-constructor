import math
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from .sequence_recorder_capture_frame import SequenceRecorderCaptureFrame
from .sequence_recorder_video_controls import SequenceRecorderVideoControlFrame

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.capture_frame = SequenceRecorderCaptureFrame(self)
        self.video_control_frame = SequenceRecorderVideoControlFrame(self)
        self._setup_layout()

        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(100)

    def animate_background(self):
        self.gradient_shift += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        for i in range(10):
            pos = i / 9
            brightness = int(
                (math.sin(self.gradient_shift + pos * 2 * math.pi) * 0.5 + 0.5) * 255
            )
            color = QColor.fromHsv(200, 150, brightness)
            gradient.setColorAt(pos, color)

        painter.fillRect(self.rect(), gradient)

    def _setup_layout(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.addWidget(self.capture_frame, 5)
        self.main_layout.addWidget(self.video_control_frame, 2)

    def resize_sequence_recorder_widget(self) -> None:
        self.capture_frame.resize_capture_frame()
        self.video_control_frame.resize_video_control_frame()
        self.capture_frame.sequence_beat_frame.populate_beat_frame_scenes_from_json()
