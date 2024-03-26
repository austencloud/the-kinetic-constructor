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


from widgets.sequence_recorder_beat_frame import SequenceRecorderBeatFrame
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceRecorderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.video_frame_rate = 30
        self.video_display_width = 640
        self.video_display_height = 480
        self.init_ui()
        self.capture = None
        self.record = False
        self.recording_frames = []
        QTimer.singleShot(0, lambda: self.init_webcam(0))

    def init_ui(self) -> None:
        self._setup_webcam_selector()
        self._setup_video_display()
        self._setup_control_buttons()
        self._setup_speed_slider()
        self._setup_sequence_beat_frame()
        self._setup_layout()

    def _setup_webcam_selector(self):
        self.webcam_selector = QComboBox()
        self.available_cameras = self.detect_active_cameras()
        for cam_index, cam_name in self.available_cameras.items():
            self.webcam_selector.addItem(f"{cam_name} ({cam_index})", cam_index)
        self.webcam_selector.currentIndexChanged.connect(
            lambda: self.init_webcam(self.webcam_selector.currentData())
        )

    def detect_active_cameras(self, max_check=10):
        """Check the first 'max_check' indexes for available cameras."""
        available_cameras = {}
        for i in range(max_check):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                available_cameras[i] = f"Camera {i}"
                cap.release()
        return available_cameras

    def _setup_video_display(self) -> None:
        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.sequence_beat_frame)
        self.right_layout.addWidget(self.video_display)
        self.right_layout.addWidget(self.webcam_selector)
        self.right_layout.addLayout(self.control_layout)
        self.right_layout.addWidget(self.speed_slider)
        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 1)

    def _setup_sequence_beat_frame(self):
        self.sequence_beat_frame = SequenceRecorderBeatFrame(self.main_widget)

    def _setup_control_buttons(self):
        self.control_layout = QHBoxLayout()
        self.play_button = QPushButton("Capture Frame")
        self.play_button.clicked.connect(self.capture_frame)
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.toggle_recording)
        self.save_button = QPushButton("Save Video")
        self.save_button.clicked.connect(self.save_video)
        self.save_button.setEnabled(False)
        for button in [self.play_button, self.record_button, self.save_button]:
            self.control_layout.addWidget(button)

    def _setup_speed_slider(self):
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(4)
        self.speed_slider.setValue(1)
        self.speed_slider.valueChanged.connect(self.update_speed)

    def init_webcam(self, camera_index: int):
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
            self.display_frame(frame)

    def display_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
        )
        p = convert_to_Qt_format.scaled(
            self.video_display_width,
            self.video_display_height,
            Qt.AspectRatioMode.KeepAspectRatio,
        )
        self.video_display.setPixmap(QPixmap.fromImage(p))

    def capture_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.imwrite("captured_frame.jpg", frame)
            QMessageBox.information(
                self,
                "Frame Captured",
                'The current frame has been saved as "captured_frame.jpg".',
            )

    def toggle_recording(self):
        self.record = not self.record
        self.record_button.setText("Stop" if self.record else "Record")
        self.save_button.setEnabled(not self.record)
        if not self.record and self.recording_frames:
            QMessageBox.information(
                self,
                "Recording Stopped",
                "Recording has been stopped. You can now save the video.",
            )

    def save_video(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Video", "", "Video Files (*.avi)"
        )
        if filepath:
            height, width, layers = self.recording_frames[0].shape
            size = (width, height)
            out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*"DIVX"), 30, size)
            for frame in self.recording_frames:
                out.write(frame)
            out.release()
            self.recording_frames.clear()
            QMessageBox.information(
                self, "Video Saved", f'The video has been saved as "{filepath}".'
            )

    def update_speed(self):
        speed = self.speed_slider.value()
        self.video_frame_rate = 30 * speed  # Adjusting frame rate
        self.update_timer_interval()

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
