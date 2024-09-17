from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class MaxTurnIntensityAdjuster(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.intensity = 0
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.intensity_label = QLabel("Max Turn Intensity:")
        self.intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.intensity_buttons_layout = QHBoxLayout()
        self.intensity_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_turn_intensity_adjuster()

        # Add the label and buttons layout to the main layout
        self.layout.addWidget(self.intensity_label)
        self.layout.addLayout(self.intensity_buttons_layout)

    def _create_turn_intensity_adjuster(self):
        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrease_intensity)

        self.intensity_value_label = QLabel(str(self.intensity))
        self.intensity_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intensity_value_label.setFixedWidth(40)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increase_intensity)

        self.intensity_buttons_layout.addWidget(self.minus_button)
        self.intensity_buttons_layout.addWidget(self.intensity_value_label)
        self.intensity_buttons_layout.addWidget(self.plus_button)

    def _increase_intensity(self):
        if self.intensity < 30:
            self.intensity += 1
            self.intensity_value_label.setText(str(self.intensity))
            self.auto_builder_frame._update_max_turn_intensity(self.intensity)

    def _decrease_intensity(self):
        if self.intensity > 0:
            self.intensity -= 1
            self.intensity_value_label.setText(str(self.intensity))
            self.auto_builder_frame._update_max_turn_intensity(self.intensity)

    def set_intensity(self, intensity):
        """Set the initial intensity when loading settings."""
        self.intensity = intensity
        self.intensity_value_label.setText(str(self.intensity))

    def resize_max_turn_intensity_adjuster(self):
        font_size = self.auto_builder_frame.auto_builder.main_widget.width() // 60
        self.minus_button.setStyleSheet(f"font-size: {font_size}px;")
        self.plus_button.setStyleSheet(f"font-size: {font_size}px;")
        self.intensity_label.setStyleSheet(f"font-size: {font_size}px;")

        self.minus_button.updateGeometry()
        self.plus_button.updateGeometry()
        self.intensity_label.updateGeometry()

        self.minus_button.repaint()
        self.plus_button.repaint()
        self.intensity_label.repaint()
