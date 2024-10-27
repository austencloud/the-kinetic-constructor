# cue_box.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from .timestamp import Timestamp
from .cue_label import CueLabel

if TYPE_CHECKING:
    from .cue_frame import CueFrame


class CueBox(QWidget):
    def __init__(
        self, cue_frame: "CueFrame", timestamp_text: str, cue_label_text: str = ""
    ):
        super().__init__(cue_frame)
        self.cue_frame = cue_frame

        # Create timestamp and cue label
        self.timestamp = Timestamp(self, timestamp_text)
        self.cue_label = CueLabel(self, cue_label_text)

        # Setup layout
        self.layout:QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.timestamp, 1)
        self.layout.addWidget(self.cue_label, 3)

        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Apply styles
        self.setObjectName("cue_box")
        self.setStyleSheet("#cue_box {border-top: 1px solid black;}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.timestamp.resize_timestamp()
        self.cue_label.resize_lyric_label()
