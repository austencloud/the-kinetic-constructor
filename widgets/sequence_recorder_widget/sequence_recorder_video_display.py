from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
import cv2

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )


class SequenceRecorderVideoDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_display.setFont(QFont("Arial", 12))
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_display)
        self.setLayout(layout)

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
