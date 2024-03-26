from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QInputDialog,
    QFileDialog,
    QMessageBox,
    QHBoxLayout, QComboBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
import os


class VideoRecorderWidget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.video_frame_rate = 30
        # Initialize display size attributes to avoid AttributeError
        self.video_display_width = 640  # Default width, adjust as needed
        self.video_display_height = 480  # Default height, adjust as needed
        self.init_ui()
        # Delay webcam initialization to after UI setup
        self.capture = None
        self.record = False
        self.recording_frames = []

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Webcam selection dropdown
        self.webcam_selector = QComboBox()
        self.webcam_selector.addItems([f"Camera {i}" for i in range(5)])  # Example for up to 5 cameras, adjust as needed
        self.layout.addWidget(self.webcam_selector)
        self.webcam_selector.currentIndexChanged.connect(self.init_webcam)

        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.video_display)

        # Control buttons setup
        self.setup_control_buttons()

        # Speed Slider
        self.setup_speed_slider()

    def setup_control_buttons(self):
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
        self.layout.addLayout(self.control_layout)

    def setup_speed_slider(self):
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(4)
        self.speed_slider.setValue(1)
        self.speed_slider.valueChanged.connect(self.update_speed)
        self.layout.addWidget(self.speed_slider)

    def init_webcam(self, camera_index: int):
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(camera_index)
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_video_feed)
        self.update_timer_interval()

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
            self.video_display_width,  # Use the dynamically calculated width
            self.video_display_height,  # Use half of the container widget's height
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
            # Assuming 30 FPS for saved video
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
        # Adjusting frame rate based on speed selection
        speed = self.speed_slider.value()
        self.video_frame_rate = 30 * speed  # Adjusting frame rate
        self.update_timer_interval()

    def update_timer_interval(self):
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)

    def close_event(self, event):
        self.capture.release()

    def resizeEvent(self, event):
        # Dynamically calculate the size of the video_display
        container_height = self.height()
        container_width = self.width()

        # Set the video_display's height to half of the container widget's height
        # and calculate width respecting the original aspect ratio
        self.video_display_height = container_height // 2
        self.video_display_width = min(
            container_width, self.video_display_height * 16 // 9
        )  # Assuming 16:9 aspect ratio

        # Optionally, adjust the layout or widget properties if needed

        super().resizeEvent(event)  # Ensure the base class resize event is called
