from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QMessageBox
import cv2


if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderVideoDisplay(QWidget):
    def __init__(self, sequence_recorder_widget: "SequenceRecorderWidget"):
        super().__init__()
        self.sequence_recorder_widget = sequence_recorder_widget
        self.init_ui()

    def init_ui(self):
        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_display.setFont(QFont("Arial", 12))
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_display)
        self.setLayout(layout)
        self.capture = None
        self.record = False
        self.recording_frames = []
        self.video_frame_rate = 30

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

    def update_timer_interval(self) -> None:
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)

    def close_event(self, event) -> None:
        self.capture.release()

    def update_video_feed(self) -> None:
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.record:
                self.recording_frames.append(frame)
            self.display_frame(frame)

    def display_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_Qt_format = QImage(
            rgb_image.data,
            rgb_image.shape[1],
            rgb_image.shape[0],
            QImage.Format.Format_RGB888,
        )
        p = QPixmap.fromImage(convert_to_Qt_format)
        self.video_display.setPixmap(
            p.scaled(
                self.video_display.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def get_aspect_ratio(self) -> float:
        return self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) / self.capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )

    def resize_video_display(self):
        recording_frame_size = self.sequence_recorder_widget.recording_frame.size()
        aspect_ratio = self.get_aspect_ratio()

        width = self.sequence_recorder_widget.recording_frame.width()
        height = int(width / aspect_ratio)

        if height > recording_frame_size.height():
            height = recording_frame_size.height()
            width = int(height * aspect_ratio)

        self.video_display_width = width // 2
        self.video_display_height = height

        self.update_video_feed()
