from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
import cv2

from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QFrame,
)


if TYPE_CHECKING:
    from widgets.sequence_recorder.SR_main_control_frame import (
        SR_MainControlFrame,
    )


class SR_VideoControlPanel(QFrame):
    def __init__(self, control_frame: "SR_MainControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.capture_frame = self.control_frame.sequence_recorder.capture_frame
        self._setup_outline()
        self._init_ui()

    def _setup_outline(self):
        self.setObjectName("video_control_frame")
        self.setStyleSheet("#video_control_frame { border: 1px solid black; }")

    def _init_ui(self) -> None:
        self._setup_controls()
        self._setup_layout()
        self._populate_webcam_selector()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for widget in self.video_controls:
            self.layout.addWidget(widget)

    def _setup_controls(self) -> None:
        self.webcam_selector = QComboBox()
        self.play_button = QPushButton("Capture Frame")
        self.record_button = QPushButton(
            "Record",
            clicked=self.capture_frame.video_display_frame.toggle_recording,
        )
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)
        self.video_controls = [
            self.webcam_selector,
            self.play_button,
            self.record_button,
            self.save_button,
        ]


    def resize_video_control_frame(self) -> None:
        width = self.capture_frame.video_display_frame.width()
        height = width // 4
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def _init_ui(self) -> None:
        self._setup_controls()
        self._setup_layout()
        self._populate_webcam_selector()

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

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for widget in self.video_controls:
            self.layout.addWidget(widget)

    def _setup_controls(self) -> None:
        self.webcam_selector = QComboBox()
        self.play_button = QPushButton("Capture Frame")
        self.record_button = QPushButton(
            "Record",
            clicked=self.capture_frame.video_display_frame.toggle_recording,
        )
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)
        self.video_controls = [
            self.webcam_selector,
            self.play_button,
            self.record_button,
            self.save_button,
        ]

    def _populate_webcam_selector(self) -> None:
        self.webcam_selector.clear()
        devices = self.detect_available_cameras()
        for index, name in devices.items():
            self.webcam_selector.addItem(name, index)

    def resize_video_control_frame(self) -> None:
        width = self.capture_frame.video_display_frame.width()
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

