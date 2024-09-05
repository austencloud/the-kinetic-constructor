from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
    QComboBox,
)
from typing import TYPE_CHECKING, cast

from .sequence_options_widget import SequenceOptionsWidget
from .freeform_sequence_auto_builder import FreeFormSequenceAutoBuilder
from .circular_sequence_auto_builder import CircularSequenceAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class AutoBuilderDialog(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.json_manager = self.sequence_widget.json_manager
        self.beat_frame = self.sequence_widget.beat_frame
        self.setWindowTitle("Auto Builder")
        self.setModal(True)
        self.freeform_builder = FreeFormSequenceAutoBuilder(self)
        self.circular_builder = CircularSequenceAutoBuilder(self)
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Initial selection buttons for Freeform and Circular sequences
        self.initial_selection_layout = QVBoxLayout()
        self.freeform_button = QPushButton("Freeform Sequence")
        self.circular_button = QPushButton("Circular Sequence")
        self.freeform_button.clicked.connect(self._show_freeform_options)
        self.circular_button.clicked.connect(self._show_circular_options)
        self.initial_selection_layout.addWidget(self.freeform_button)
        self.initial_selection_layout.addWidget(self.circular_button)
        layout.addLayout(self.initial_selection_layout)

        # Stacked widget to switch between different sequence options
        self.options_stack = QStackedWidget()

        # Freeform Sequence Options
        self.freeform_options_widget = SequenceOptionsWidget()
        self.options_stack.addWidget(self.freeform_options_widget)

        # Circular Sequence Options
        self.circular_options_widget = SequenceOptionsWidget()
        self.options_stack.addWidget(self.circular_options_widget)

        # Rotation Type Selection for Circular Builder
        self.rotation_type_combo = QComboBox()
        self.rotation_type_combo.addItem("Quartered", "quartered")
        self.rotation_type_combo.addItem("Halved", "halved")
        self.rotation_type_combo.setToolTip("Select the rotation type for the circular sequence")
        layout.addWidget(self.rotation_type_combo)

        layout.addWidget(self.options_stack)
        self.options_stack.setVisible(False)

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

    def _show_freeform_options(self):
        self.options_stack.setCurrentIndex(0)
        self.options_stack.setVisible(True)
        self.initial_selection_layout.setEnabled(False)

    def _show_circular_options(self):
        self.options_stack.setCurrentIndex(1)
        self.options_stack.setVisible(True)
        self.initial_selection_layout.setEnabled(False)

    def _load_settings(self):
        """Load the saved settings and apply them to the dialog UI elements."""
        settings = self.settings_manager.auto_builder

        sequence_length = settings.get_auto_builder_setting("sequence_length")
        turn_intensity = settings.get_auto_builder_setting("turn_intensity")
        max_turns = settings.get_auto_builder_setting("max_turns")
        sequence_level = settings.get_auto_builder_setting("sequence_level")

        # Load settings into freeform and circular options
        for widget in [self.freeform_options_widget, self.circular_options_widget]:
            widget.sequence_length_spinbox.setValue(sequence_length)
            widget.sequence_level_combo.setCurrentIndex(sequence_level - 1)
            widget.turn_settings_widget.turn_intensity_slider.setValue(turn_intensity)
            widget.turn_settings_widget.max_turns_spinbox.setValue(max_turns)
            widget._update_turn_settings_visibility()

    def _on_create_sequence(self):
        # Save the settings
        current_widget = cast(SequenceOptionsWidget, self.options_stack.currentWidget())

        self._update_settings(current_widget)

        # Extract the values to be passed to the builders
        sequence_length = current_widget.sequence_length_spinbox.value()
        turn_intensity = current_widget.turn_settings_widget.turn_intensity_slider.value()
        max_turns = current_widget.turn_settings_widget.max_turns_spinbox.value()
        sequence_level = current_widget.sequence_level_combo.currentIndex() + 1

        # Check if the circular builder is active
        if self.options_stack.currentIndex() == 1:
            # Circular Sequence Builder
            rotation_type = self.rotation_type_combo.currentData()  # Get rotation type for circular
            self.circular_builder.build_sequence(
                sequence_length, turn_intensity, sequence_level, max_turns, rotation_type
            )
        else:
            # Freeform Sequence Builder (no rotation_type)
            self.freeform_builder.build_sequence(
                sequence_length, turn_intensity, sequence_level, max_turns
            )

        self.accept()

    def _update_settings(self, current_widget: "SequenceOptionsWidget"):
        settings = self.settings_manager.auto_builder
        settings.set_auto_builder_setting(
            "sequence_length", current_widget.sequence_length_spinbox.value()
        )
        settings.set_auto_builder_setting(
            "turn_intensity",
            current_widget.turn_settings_widget.turn_intensity_slider.value(),
        )
        settings.set_auto_builder_setting(
            "max_turns", current_widget.turn_settings_widget.max_turns_spinbox.value(),
        )
        settings.set_auto_builder_setting(
            "sequence_level", current_widget.sequence_level_combo.currentIndex() + 1
        )
