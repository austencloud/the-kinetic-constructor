from typing import TYPE_CHECKING
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

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderVideoControlFrame(QWidget):
    def __init__(self, sequence_recorder_widget: "SequenceRecorderWidget") -> None:
        super().__init__()
        self.sequence_recorder_widget = sequence_recorder_widget
        self.init_ui()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def init_ui(self) -> None:
        self._setup_controls()
        self._setup_bpm_slider()
        self._setup_layout()
        self.populate_webcam_selector()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.video_control_layout: QHBoxLayout = QHBoxLayout()
        self.beat_control_layout: QVBoxLayout = QVBoxLayout()
        self.video_control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.beat_control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.beat_control_layout.addWidget(self.bpm_slider)
        for widget in self.video_controls:
            self.video_control_layout.addWidget(widget)

        self.layout.addLayout(self.beat_control_layout, 1)
        self.layout.addLayout(self.video_control_layout, 1)

    def _setup_controls(self) -> None:
        self.webcam_selector = QComboBox()
        self.play_button = QPushButton("Capture Frame")
        self.record_button = QPushButton("Record")
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)
        self.video_controls = [
            self.webcam_selector,
            self.play_button,
            self.record_button,
            self.save_button,
        ]

    def _setup_bpm_slider(self) -> None:
        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(180)

    def populate_webcam_selector(self) -> None:
        self.webcam_selector.clear()
        devices = self.detect_available_cameras()
        for index, name in devices.items():
            self.webcam_selector.addItem(name, index)

    @staticmethod
    def detect_available_cameras() -> dict[int, str]:
        max_tested = 2
        devices = {}
        for index in range(max_tested):
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                devices[index] = f"Camera {index}"
                cap.release()
        return devices

    def resize_video_control_frame(self) -> None:
        size = int(2 * (self.sequence_recorder_widget.height() // 1.75))
        self.setMaximumWidth(size)
