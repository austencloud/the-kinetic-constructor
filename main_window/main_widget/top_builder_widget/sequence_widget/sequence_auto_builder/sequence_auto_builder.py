from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QSlider, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .freeform_sequence_auto_builder import FreeFormSequenceAutoBuilder
from .circular_sequence_auto_builder import CircularSequenceAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import SequenceWidget

class SequenceAutoBuilder(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.setWindowTitle("Auto Builder")
        self.setModal(True)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Sequence Type Selector
        layout.addWidget(QLabel("Select Sequence Type:"))
        self.sequence_type_combo = QComboBox()
        self.sequence_type_combo.addItems(["Random Freeform", "Circular (Strict Rotational)"])
        layout.addWidget(self.sequence_type_combo)

        # Sequence Length
        layout.addWidget(QLabel("Sequence Length (beats):"))
        self.sequence_length_spinbox = QSpinBox()
        self.sequence_length_spinbox.setRange(1, 32)
        self.sequence_length_spinbox.setValue(16)
        layout.addWidget(self.sequence_length_spinbox)

        # Turn Intensity
        layout.addWidget(QLabel("Turn Intensity:"))
        self.turn_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_intensity_slider.setRange(0, 100)
        self.turn_intensity_slider.setValue(50)
        layout.addWidget(self.turn_intensity_slider)

        # Sequence Level Selector
        layout.addWidget(QLabel("Select Sequence Level:"))
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItems(["Level 1: Radial", "Level 2: Radial with Turns", "Level 3: Non-Radial"])
        layout.addWidget(self.sequence_level_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create Sequence")
        self.create_button.clicked.connect(self._on_create_sequence)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def _on_create_sequence(self):
        sequence_type = self.sequence_type_combo.currentText()
        sequence_length = self.sequence_length_spinbox.value()
        turn_intensity = self.turn_intensity_slider.value()
        sequence_level = self.sequence_level_combo.currentIndex() + 1

        if sequence_type == "Random Freeform":
            builder = FreeFormSequenceAutoBuilder(self.sequence_widget, sequence_length, turn_intensity, sequence_level)
        elif sequence_type == "Circular (Strict Rotational)":
            builder = CircularSequenceAutoBuilder(self.sequence_widget, sequence_length, turn_intensity, sequence_level)

        builder.build_sequence()
        self.accept()
