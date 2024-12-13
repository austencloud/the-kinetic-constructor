# freeform_sequence_generator_frame.py

from PyQt6.QtWidgets import QCheckBox, QPushButton, QLabel, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.sequence_generator.freeform.freeform_sequence_generator import (
    FreeFormSequenceGenerator,
)

from .letter_picker_dialog import LetterPickerDialog
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame

if TYPE_CHECKING:
    from ..sequence_generator_widget import SequenceGeneratorWidget


class FreeformSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "SequenceGeneratorWidget") -> None:
        super().__init__(sequence_generator_tab, "freeform")
        self.builder = None  # or your builder logic
        self.builder = FreeFormSequenceGenerator(self)
        self.letter_picker_dialog = LetterPickerDialog(self)

        # Create UI components for letter picking mode
        self.letter_mode_checkbox = QCheckBox("Use All Letters")
        self.letter_mode_checkbox.setChecked(True)  # default: all letters
        self.letter_mode_checkbox.stateChanged.connect(self._on_letter_mode_changed)

        self.select_letters_button = QPushButton("Select Letters...")
        self.select_letters_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_letters_button.clicked.connect(self._show_letter_picker_dialog)
        self.select_letters_button.setVisible(False)  # hidden if all letters are used

        self.selected_letters_label = QLabel("All Letters")
        self.selected_letters_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add them to the layout
        self.layout.addWidget(self.letter_mode_checkbox)
        self.layout.addWidget(self.select_letters_button)
        self.layout.addWidget(self.selected_letters_label)
        self.layout.addStretch(1)

        self.apply_settings()

    def _on_letter_mode_changed(self, state):
        if self.letter_mode_checkbox.isChecked():
            self.select_letters_button.setVisible(False)
            self.selected_letters_label.setText("All Letters")
            self.sequence_generator_settings.set_sequence_generator_setting(
                "selected_letter_types", None, self.builder_type
            )
        else:
            self.select_letters_button.setVisible(True)
            chosen = self.sequence_generator_settings.get_sequence_generator_setting(
                "selected_letter_types", self.builder_type
            )
            if chosen is None or len(chosen) == 0:
                self.selected_letters_label.setText("No Letters Chosen")
            else:
                self.selected_letters_label.setText(", ".join(chosen))

    def _show_letter_picker_dialog(self):
        if self.letter_picker_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_types = self.letter_picker_dialog.get_selected_letter_types()
            self.sequence_generator_settings.set_sequence_generator_setting(
                "selected_letter_types",
                [lt.description for lt in selected_types],
                self.builder_type,
            )
            if selected_types:
                desc_list = [lt.description for lt in selected_types]
                self.selected_letters_label.setText(", ".join(desc_list))
            else:
                self.selected_letters_label.setText("No Letters Chosen")

    def apply_settings(self):
        super().apply_settings()
        selected_types = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "selected_letter_types", self.builder_type
            )
        )

        if selected_types is None:
            # Means all letters are used
            self.letter_mode_checkbox.setChecked(True)
            self.selected_letters_label.setText("All Letters")
        else:
            # Means specific letters mode
            self.letter_mode_checkbox.setChecked(False)
            if len(selected_types) > 0:
                self.selected_letters_label.setText(", ".join(selected_types))
            else:
                self.selected_letters_label.setText("No Letters Chosen")

    def on_create_sequence(self, overwrite_sequence: bool):
        """Trigger sequence creation for Freeform."""
        if overwrite_sequence:
            self.sequence_generator_tab.main_widget.sequence_widget.beat_frame.beat_deletion_manager.delete_all_beats()

        self.builder.build_sequence(
            int(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "sequence_length", self.builder_type
                )
            ),
            float(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
            int(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "sequence_level", self.builder_type
                )
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
                "continuous_rotation", self.builder_type
            ),
        )
        self.sequence_generator_tab.main_widget.manual_builder.option_picker.update_option_picker()

    def get_selected_letter_types(self) -> list["LetterType"]:
        """Return a list of selected letter types."""
        selected_types = []
        for (
            letter_type,
            label,
        ) in self.letter_picker_dialog.buttons.items():
            if label.is_checked:
                selected_types.append(letter_type)
        return selected_types

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # resize the checkbox text and the button text and the label text accroding to the height of the screen
        height = self.height()
        font_size = height // 30
        self.letter_mode_checkbox.setFont(QFont("Arial", font_size))
        self.select_letters_button.setFont(QFont("Arial", font_size))
        self.selected_letters_label.setFont(QFont("Arial", font_size))
        self.layout.setSpacing(height // 50)
