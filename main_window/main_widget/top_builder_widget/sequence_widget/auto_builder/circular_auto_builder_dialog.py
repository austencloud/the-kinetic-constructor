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

from .circular_auto_builder import CircularAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class CircularAutoBuilderDialog(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.auto_builder_settings = (
            self.sequence_widget.main_widget.main_window.settings_manager.auto_builder
        )
        self.circular_builder = CircularAutoBuilder(self)
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

        # Rotation Type Selection for Circular Builder
        layout.addWidget(QLabel("Rotation Type:"))
        self.rotation_type_combo = QComboBox()
        self.rotation_type_combo.addItem("Quartered", "quartered")
        self.rotation_type_combo.addItem("Halved", "halved")
        self.rotation_type_combo.currentIndexChanged.connect(
            self._handle_rotation_type_change
        )
        layout.addWidget(self.rotation_type_combo)

        # Permutation options (for user to choose)
        layout.addWidget(QLabel("Permutation Options:"))
        self.permutation_type_combo = QComboBox()
        self.permutation_type_combo.addItem("Rotational", "rotational")
        self.permutation_type_combo.addItem("Mirrored", "mirrored")
        self.permutation_type_combo.currentIndexChanged.connect(
            self._handle_permutation_type_change
        )
        layout.addWidget(self.permutation_type_combo)

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

    def _handle_turn_intensity_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "turn_intensity", self.turn_intensity_slider.value(), "circular"
        )

    def _handle_max_turns_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turns", self.max_turns_spinbox.value(), "circular"
        )

    def _handle_sequence_length_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", self.sequence_length_spinbox.value(), "circular"
        )

    def _handle_sequence_level_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentIndex() + 1, "circular"
        )
        self._update_turn_settings_visibility()

    def _handle_rotation_type_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "rotation_type", self.rotation_type_combo.currentData(), "circular"
        )
        self._restrict_sequence_length_options()

    def _handle_permutation_type_change(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "permutation_type", self.permutation_type_combo.currentData(), "circular"
        )
        self._restrict_rotation_type_options()

    def _restrict_sequence_length_options(self):
        rotation_type = self.rotation_type_combo.currentData()
        if rotation_type == "quartered":
            self.sequence_length_spinbox.setRange(4, 32)
            self.sequence_length_spinbox.setSingleStep(4)
        elif rotation_type == "halved":
            self.sequence_length_spinbox.setRange(2, 32)
            self.sequence_length_spinbox.setSingleStep(2)

    def _restrict_rotation_type_options(self):
        # If the permutation type is mirrored, limit rotation type to halved
        if self.permutation_type_combo.currentData() == "mirrored":
            self.rotation_type_combo.setCurrentIndex(
                self.rotation_type_combo.findData("halved")
            )
            self.rotation_type_combo.setDisabled(True)
        else:
            self.rotation_type_combo.setDisabled(False)

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
        """Load the saved settings for the Circular builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings("circular")

        self.sequence_length_spinbox.setValue(settings["sequence_length"])
        self.sequence_level_combo.setCurrentIndex(settings["sequence_level"] - 1)
        self.turn_intensity_slider.setValue(settings["turn_intensity"])
        self.max_turns_spinbox.setValue(settings["max_turns"])
        self.rotation_type_combo.setCurrentIndex(
            self.rotation_type_combo.findData(settings["rotation_type"])
        )
        self.permutation_type_combo.setCurrentIndex(
            self.permutation_type_combo.findData(settings["permutation_type"])
        )
        self._update_turn_settings_visibility()
        self._restrict_sequence_length_options()
        self._restrict_rotation_type_options()

    def _on_create_sequence(self):
        # Extract values
        sequence_length = self.sequence_length_spinbox.value()
        turn_intensity = self.turn_intensity_slider.value()
        max_turns = self.max_turns_spinbox.value()
        sequence_level = self.sequence_level_combo.currentIndex() + 1
        rotation_type = self.rotation_type_combo.currentData()
        permutation_type = self.permutation_type_combo.currentData()

        # Build the sequence
        self.circular_builder.build_sequence(
            sequence_length,
            turn_intensity,
            sequence_level,
            max_turns,
            rotation_type,
            permutation_type,
        )

        self.accept()
