from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class FreeformAutoBuilderDialog(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.auto_builder_settings = (
            self.sequence_widget.main_widget.main_window.settings_manager.auto_builder
        )
        self.freeform_builder = FreeFormAutoBuilder(self)
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Sequence Length
        layout.addWidget(QLabel("Sequence Length (beats):"))
        self.sequence_length_spinbox = QSpinBox()
        self.sequence_length_spinbox.valueChanged.connect(
            self._handle_sequence_length_change
        )
        layout.addWidget(self.sequence_length_spinbox)

        # Sequence Level
        layout.addWidget(QLabel("Select Sequence Level:"))
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItems(
            ["Level 1: Radial", "Level 2: Radial with Turns", "Level 3: Non-Radial"]
        )
        self.sequence_level_combo.currentIndexChanged.connect(
            self._handle_sequence_level_change
        )
        layout.addWidget(self.sequence_level_combo)

        # Turn Intensity
        layout.addWidget(QLabel("Turn Intensity:"))
        self.turn_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        # connect it to a new function which updates the settings
        self.turn_intensity_slider.valueChanged.connect(
            self._handle_turn_intensity_change
        )
        layout.addWidget(self.turn_intensity_slider)

        # Max Number of Turns
        layout.addWidget(QLabel("Max Number of Turns:"))
        self.max_turns_spinbox = QSpinBox()
        self.max_turns_spinbox.valueChanged.connect(self._handle_max_turns_change)
        layout.addWidget(self.max_turns_spinbox)

        # Buttons to create or cancel the sequence
        self.create_button = QPushButton("Create Sequence")
        self.create_button.clicked.connect(self._on_create_sequence)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _update_turn_settings_visibility(self):
        level = self.sequence_level_combo.currentIndex() + 1
        if level == 1:
            self.turn_intensity_slider.setVisible(False)
            self.max_turns_spinbox.setVisible(False)
        else:
            self.turn_intensity_slider.setVisible(True)
            self.max_turns_spinbox.setVisible(True)
            if level == 2:
                self.turn_intensity_slider.setRange(0, 3)
            elif level == 3:
                self.turn_intensity_slider.setRange(0, 6)

    def _load_settings(self):
        """Load the saved settings for the Freeform builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings("freeform")

        self.sequence_length_spinbox.setValue(settings["sequence_length"])
        self.sequence_level_combo.setCurrentIndex(settings["sequence_level"] - 1)
        self.turn_intensity_slider.setValue(settings["turn_intensity"])
        self.max_turns_spinbox.setValue(settings["max_turns"])
        self._update_turn_settings_visibility()

    def _handle_sequence_length_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", self.sequence_length_spinbox.value(), "freeform"
        )

    def _handle_sequence_level_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentIndex() + 1, "freeform"
        )
        self._update_turn_settings_visibility()

    def _handle_max_turns_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turns", self.max_turns_spinbox.value(), "freeform"
        )

    def _handle_turn_intensity_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "turn_intensity", self.turn_intensity_slider.value(), "freeform"
        )

    def _on_create_sequence(self):
        # Extract values
        sequence_length = self.sequence_length_spinbox.value()
        turn_intensity = self.turn_intensity_slider.value()
        max_turns = self.max_turns_spinbox.value()
        sequence_level = self.sequence_level_combo.currentIndex() + 1

        # Build the sequence
        self.freeform_builder.build_sequence(
            sequence_length, turn_intensity, sequence_level, max_turns
        )

        self.accept()
