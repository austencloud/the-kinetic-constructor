from PyQt6.QtWidgets import QComboBox, QPushButton, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class SequenceRecorderVideoControls(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.layout = QVBoxLayout(self)

        self.webcam_selector = QComboBox()
        self.layout.addWidget(self.webcam_selector)

        self.play_button = QPushButton("Capture Frame")
        self.record_button = QPushButton("Record")
        self.save_button = QPushButton("Save Video")
        self.save_button.setEnabled(False)

        for button in [self.play_button, self.record_button, self.save_button]:
            self.layout.addWidget(button)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(4)
        self.speed_slider.setValue(1)
        self.layout.addWidget(self.speed_slider)
