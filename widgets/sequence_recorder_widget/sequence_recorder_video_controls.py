from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QSlider,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
import cv2


class SequenceRecorderVideoControls(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout: QHBoxLayout = QHBoxLayout(self)
        self.beat_control_layout: QVBoxLayout = QVBoxLayout()
        self.recording_control_layout: QVBoxLayout = QVBoxLayout()
        self.recording_control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.webcam_selector = QComboBox()
        self.populate_webcam_selector()

        self.play_button = QPushButton("Capture Frame")
        self.record_button = QPushButton("Record")
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)

        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setMinimum(60)  # Example BPM range
        self.bpm_slider.setMaximum(180)
        self.beat_control_layout.addWidget(self.bpm_slider)

        for widget in [
            self.webcam_selector,
            self.play_button,
            self.record_button,
            self.save_button,
        ]:
            self.recording_control_layout.addWidget(widget)

        self.main_layout.addLayout(self.beat_control_layout, 1)
        self.main_layout.addLayout(self.recording_control_layout, 1)

    def populate_webcam_selector(self):
        self.webcam_selector.clear()
        devices = self.detect_available_cameras()
        for index, name in devices.items():
            self.webcam_selector.addItem(name, index)

    @staticmethod
    def detect_available_cameras():
        max_tested = 2
        devices = {}
        for index in range(max_tested):
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                devices[index] = f"Camera {index}"
                cap.release()
        return devices
