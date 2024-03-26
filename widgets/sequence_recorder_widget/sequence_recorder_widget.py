from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QInputDialog,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QComboBox,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
import os


from widgets.sequence_recorder_widget.sequence_recorder_beat_frame import SequenceRecorderBeatFrame
from widgets.sequence_recorder_widget.sequence_recorder_video_controls import SequenceRecorderVideoControls
from widgets.sequence_recorder_widget.sequence_recorder_video_display import SequenceRecorderVideoDisplay
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.video_frame_rate = 30
        self.capture = None
        self.record = False
        self.recording_frames = []
        QTimer.singleShot(0, self.init_webcam)

        self.init_ui()

    def init_ui(self) -> None:
        self._setup_sequence_beat_frame()
        self.videoDisplay = SequenceRecorderVideoDisplay()
        self.videoControls = SequenceRecorderVideoControls()
        self.videoControls.webcam_selector.currentIndexChanged.connect(
            lambda: self.init_webcam(self.videoControls.webcam_selector.currentData())
        )
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        
        self.left_layout.addWidget(self.sequence_beat_frame)
        
        self.right_layout.addWidget(self.videoDisplay)
        self.right_layout.addWidget(self.videoControls)
        
        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 1)

    def _setup_sequence_beat_frame(self):
        self.sequence_beat_frame = SequenceRecorderBeatFrame(self.main_widget)

    def init_webcam(self, camera_index: int = 0):
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
        if not self.capture.isOpened():
            QMessageBox.warning(self, "Webcam Error", "Unable to access the webcam.")
            return
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_video_feed)
        self.update_timer_interval()
        self.video_timer.start()

    def update_video_feed(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.record:
                self.recording_frames.append(frame)
            self.videoDisplay.display_frame(frame)  # Use the display_frame method of VideoDisplay

    def update_timer_interval(self):
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)


    def close_event(self, event):
        self.capture.release()

    def get_aspect_ratio(self):
        return self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) / self.capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )

    def resize_sequence_recorder_widget(self):
        main_widget_size = self.main_widget.size()
        aspect_ratio = self.get_aspect_ratio()

        width = main_widget_size.width()
        height = int(width / aspect_ratio)

        if height > main_widget_size.height():
            height = main_widget_size.height()
            width = int(height * aspect_ratio)

        self.video_display_width = width
        self.video_display_height = height
        self.update_video_feed()
