from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QSpinBox,
)
from typing import TYPE_CHECKING

from .circular_auto_builder import CircularAutoBuilder
from .sequence_options_widget import SequenceOptionsWidget

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
        self.circular_builder = CircularAutoBuilder(self)
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Circular Sequence Options
        self.options_widget = SequenceOptionsWidget()
        layout.addWidget(self.options_widget)

        # Rotation Type Selection for Circular Builder
        self.rotation_type_combo = QComboBox()
        self.rotation_type_combo.addItem("Quartered", "quartered")
        self.rotation_type_combo.addItem("Halved", "halved")
        self.rotation_type_combo.currentIndexChanged.connect(
            self._restrict_sequence_length_options
        )
        layout.addWidget(self.rotation_type_combo)

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

    def _restrict_sequence_length_options(self):
        rotation_type = self.rotation_type_combo.currentData()
        sequence_length_spinbox: QSpinBox = self.options_widget.sequence_length_spinbox

        # Set allowable lengths based on rotation type
        if rotation_type == "quartered":
            sequence_length_spinbox.setRange(4, 32)
            sequence_length_spinbox.setSingleStep(4)
        elif rotation_type == "halved":
            sequence_length_spinbox.setRange(2, 32)
            sequence_length_spinbox.setSingleStep(2)

    def _load_settings(self):
        """Load the saved settings and apply them to the dialog UI elements."""
        settings = self.settings_manager.auto_builder

        sequence_length = settings.get_auto_builder_setting("sequence_length")
        turn_intensity = settings.get_auto_builder_setting("turn_intensity")
        max_turns = settings.get_auto_builder_setting("max_turns")
        sequence_level = settings.get_auto_builder_setting("sequence_level")

        self.options_widget.sequence_length_spinbox.setValue(sequence_length)
        self.options_widget.sequence_level_combo.setCurrentIndex(sequence_level - 1)
        self.options_widget.turn_settings_widget.turn_intensity_slider.setValue(
            turn_intensity
        )
        self.options_widget.turn_settings_widget.max_turns_spinbox.setValue(max_turns)
        self._restrict_sequence_length_options()

    def _on_create_sequence(self):
        # Extract values from the options widget
        sequence_length = self.options_widget.sequence_length_spinbox.value()
        turn_intensity = (
            self.options_widget.turn_settings_widget.turn_intensity_slider.value()
        )
        max_turns = self.options_widget.turn_settings_widget.max_turns_spinbox.value()
        sequence_level = self.options_widget.sequence_level_combo.currentIndex() + 1
        rotation_type = self.rotation_type_combo.currentData()

        # Circular Sequence Builder
        self.circular_builder.build_sequence(
            sequence_length, turn_intensity, sequence_level, max_turns, rotation_type
        )

        self.accept()
