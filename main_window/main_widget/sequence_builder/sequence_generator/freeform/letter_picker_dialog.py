# letter_picker_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_builder.sequence_generator.widgets.letter_type_picker import (
    LetterTypePicker,
)


class LetterPickerDialog(QDialog):
    def __init__(self, sequence_generator_frame):
        super().__init__(sequence_generator_frame)
        self.setWindowTitle("Select Letter Types")

        self.main_layout = QVBoxLayout(self)

        # Directly instantiate the LetterTypePicker here
        self.letter_type_picker = LetterTypePicker(sequence_generator_frame)
        self.main_layout.addWidget(self.letter_type_picker)

        # Add dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(button_box)

    def get_selected_letter_types(self):
        return self.letter_type_picker.get_selected_letter_types()
