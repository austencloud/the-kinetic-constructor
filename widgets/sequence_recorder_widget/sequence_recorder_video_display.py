from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QTimer, QSize
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
        self.fixed_aspect_ratio = 16 / 9  # Example: 16:9 aspect ratio
        self.init_ui()
        # Initialize with a preferred size that adheres to the aspect ratio
        self.preferred_width = 640  # Example size, adjust based on your UI requirements
        self.preferred_height = int(self.preferred_width / self.fixed_aspect_ratio)
        self.setFixedSize(self.preferred_width, self.preferred_height)

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
        self.video_frame_rate = 60

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
        # Convert the frame to an RGB image and scale it according to the fixed aspect ratio
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_Qt_format = QImage(
            rgb_image.data,
            rgb_image.shape[1],
            rgb_image.shape[0],
            QImage.Format.Format_RGB888,
        )
        p = QPixmap.fromImage(convert_to_Qt_format)
        # Scale pixmap to fit within the predefined size
        p = p.scaled(
            self.preferred_width, self.preferred_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.video_display.setPixmap(p)

    def calculate_scaled_size(self, current_size: QSize, max_size: QSize) -> QSize:
        """
        Calculate the size to scale an image to fit within maximum dimensions while maintaining aspect ratio.
        """
        aspect_ratio = current_size.width() / current_size.height()
        if (
            current_size.width() > max_size.width()
            or current_size.height() > max_size.height()
        ):
            if (max_size.width() / aspect_ratio) <= max_size.height():
                return QSize(max_size.width(), int(max_size.width() / aspect_ratio))
            else:
                return QSize(int(max_size.height() * aspect_ratio), max_size.height())
        return current_size

    def get_aspect_ratio(self) -> float:
        return self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) / self.capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )

    def resize_video_display(self):
        if not hasattr(self, "beat_frame"):
            self.beat_frame = (
                self.sequence_recorder_widget.recording_frame.sequence_beat_frame
            )

        self.max_display_width = self.beat_frame.width()
        self.max_display_height = self.beat_frame.height()

        self.update_video_feed()
