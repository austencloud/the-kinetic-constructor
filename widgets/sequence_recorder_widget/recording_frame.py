from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt


class RecordingFrame(QWidget):
    def __init__(self, sequence_beat_frame: QWidget, video_display: QWidget):
        super().__init__()
        self.sequence_beat_frame = sequence_beat_frame
        self.video_display = video_display
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setAlignment(layout, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sequence_beat_frame)
        layout.addWidget(self.video_display)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
