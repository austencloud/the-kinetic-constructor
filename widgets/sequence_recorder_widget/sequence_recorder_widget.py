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
        self.video_frame_rate = 30
        self.capture = None
        self.record = False
        self.recording_frames = []

        self.sequence_beat_frame = SequenceRecorderBeatFrame(self.main_widget)
        self.video_display = SequenceRecorderVideoDisplay()
        self.video_controls = SequenceRecorderVideoControls()
        self.recording_frame = RecordingFrame(
            self.sequence_beat_frame, self.video_display
        )
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.addWidget(self.recording_frame)
        self.main_layout.addWidget(self.video_controls)

    def _setup_sequence_beat_frame(self) -> None:
        self.sequence_beat_frame = SequenceRecorderBeatFrame(self.main_widget)

    def init_webcam(self) -> None:
        if self.capture is not None and self.capture.isOpened():
            return

        available_cameras = self.find_available_cameras()
        if available_cameras:
            self.capture = cv2.VideoCapture(available_cameras[0], cv2.CAP_MSMF)
            if not self.capture.isOpened():
                QMessageBox.warning(
                    self, "Webcam Error", "Unable to access the webcam."
                )
                return
            self.video_timer = QTimer(self)
            self.video_timer.timeout.connect(self.update_video_feed)
            self.update_timer_interval()
            self.video_timer.start()
        else:
            QMessageBox.warning(self, "Webcam Error", "No available webcams found.")

    def find_available_cameras(self):
        available_cameras = []
        for i in range(1):
            cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def update_video_feed(self) -> None:
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.record:
                self.recording_frames.append(frame)
            self.video_display.display_frame(frame)

    def update_timer_interval(self) -> None:
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)

    def close_event(self, event) -> None:
        self.capture.release()

    def get_aspect_ratio(self) -> float:
        return self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) / self.capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )

    def resize_sequence_recorder_widget(self) -> None:
        recording_frame_size = self.recording_frame.size()
        aspect_ratio = self.get_aspect_ratio()

        width = self.recording_frame.width()
        height = int(width / aspect_ratio)

        if height > recording_frame_size.height():
            height = recording_frame_size.height()
            width = int(height * aspect_ratio)

        self.video_display_width = width // 2
        self.video_display_height = height

        self.update_video_feed()
        self.sequence_beat_frame.resize_beat_frame()
