from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt


class RecordingFrame(QWidget):
    def __init__(self, sequence_beat_frame: QWidget, video_display: QWidget):
        super().__init__()
        self.sequence_beat_frame = sequence_beat_frame
        self.video_display = video_display
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(layout, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sequence_beat_frame, 1)
        layout.addWidget(self.video_display, 1)

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
