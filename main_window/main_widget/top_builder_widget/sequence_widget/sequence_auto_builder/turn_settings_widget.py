from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QSlider, QLabel
from PyQt6.QtCore import Qt


class TurnSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Turn Intensity:"))
        self.turn_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.turn_intensity_slider)

        layout.addWidget(QLabel("Max Number of Turns:"))
        self.max_turns_spinbox = QSpinBox()
        layout.addWidget(self.max_turns_spinbox)
