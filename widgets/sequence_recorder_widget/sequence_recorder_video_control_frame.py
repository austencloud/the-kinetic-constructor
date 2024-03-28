from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
import click
import cv2

from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QWidget,
)


if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_main_control_frame import (
        SequenceRecorderMainControlFrame,
    )


class SequenceRecorderVideoControlFrame(QWidget):
    def __init__(self, control_frame: "SequenceRecorderMainControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.init_ui()

    def init_ui(self) -> None:
        self._setup_controls()
        self._setup_layout()
        self.populate_webcam_selector()

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
            clicked=self.control_frame.sequence_recorder_widget.capture_frame.video_display_frame.toggle_recording,
        )
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)
        self.video_controls = [
            self.webcam_selector,
            self.play_button,
            self.record_button,
            self.save_button,
        ]

    def populate_webcam_selector(self) -> None:
        self.webcam_selector.clear()
        devices = self.detect_available_cameras()
        for index, name in devices.items():
            self.webcam_selector.addItem(name, index)

    def resize_video_control_frame(self) -> None:
        width = self.control_frame.sequence_recorder_widget.capture_frame.width() // 2
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
