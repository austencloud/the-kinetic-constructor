from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_auto_builder_frame import BaseAutoBuilderFrame


class LengthAdjusterWidget(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.length = 8
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self._create_length_adjuster()

    def _create_length_adjuster(self):
        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrement_length)

        self.length_label = QLabel(str(self.length))
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_label.setFixedWidth(40)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increment_length)

        self.layout.addWidget(self.minus_button)
        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.plus_button)

    def _increment_length(self):
        if self.length < 32:
            self.length += 1
            self.length_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)

    def _decrement_length(self):
        if self.length > 4:
            self.length -= 1
            self.length_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)

    def set_length(self, length):
        """Set the initial length when loading settings."""
        self.length = length
        self.length_label.setText(str(self.length))
