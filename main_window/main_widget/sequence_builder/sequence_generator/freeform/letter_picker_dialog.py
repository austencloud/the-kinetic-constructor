from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QLabel,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.sequence_generator.widgets.custom_letter_type_button import CustomLetterTypeButton

if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame

class LetterPickerDialog(QDialog):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__(sequence_generator_frame)
        self.sequence_generator_frame = sequence_generator_frame
        self.sequence_generator_settings = self.sequence_generator_frame.sequence_generator_settings
        self.builder_type = self.sequence_generator_frame.builder_type

        self.setWindowTitle("Select Letter Types")

        self.main_layout = QVBoxLayout(self)

        # Title label
        self.title_label = QLabel("Select Letter Types")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Create letter type buttons
        self.buttons: dict[LetterType, CustomLetterTypeButton] = {}
        for letter_type in LetterType:
            letter_type_button = CustomLetterTypeButton(self, letter_type)
            self.buttons[letter_type] = letter_type_button

        # Layout buttons in two rows of three each
        row_layouts = [QHBoxLayout(), QHBoxLayout()]
        row_layouts[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        row_layouts[1].setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons_list = list(self.buttons.values())
        for i in range(3):
            row_layouts[0].addWidget(buttons_list[i])
            row_layouts[1].addWidget(buttons_list[i + 3])

        self.main_layout.addLayout(row_layouts[0])
        self.main_layout.addLayout(row_layouts[1])

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(button_box)

        # Connect signals
        for letter_type, btn in self.buttons.items():
            # btn.clicked already emitted by button, just connect once
            btn.clicked.connect(lambda lt=letter_type: self._on_button_clicked(lt))

        self.apply_settings()

    def apply_settings(self):
        saved_types = self.sequence_generator_settings.get_sequence_generator_setting(
            "selected_letter_types", self.builder_type
        )

        if saved_types is None:
            # Means all letters are used by default
            for btn in self.buttons.values():
                btn.is_checked = True
                btn.update_style()
        else:
            # Restore previous selections
            any_selected = False
            for letter_type, btn in self.buttons.items():
                is_selected = letter_type.description in saved_types
                btn.is_checked = is_selected
                btn.update_style()
                if is_selected:
                    any_selected = True
            # If none were selected (just in case), select all by default
            if not any_selected:
                for btn in self.buttons.values():
                    btn.is_checked = True
                    btn.update_style()

    def _on_button_clicked(self, letter_type: LetterType):
        # After toggling in mousePressEvent, verify at least one is selected
        selected_count = sum(b.is_checked for b in self.buttons.values())
        if selected_count == 0:
            # Revert the current button to checked if we ended up with no selection
            btn = self.buttons[letter_type]
            btn.is_checked = True
            btn.update_style()

        # Update settings
        selected_types = self.get_selected_letter_types()
        self.sequence_generator_settings.set_sequence_generator_setting(
            "selected_letter_types",
            [lt.description for lt in selected_types],
            self.builder_type,
        )

    def get_selected_letter_types(self):
        return [lt for lt, btn in self.buttons.items() if btn.is_checked]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = max(12, self.width() // 60)
        self.title_label.setStyleSheet(
            f"font-weight: bold; font-size: {font_size}px;"
        )
        for btn in self.buttons.values():
            btn.update_style()

    def get_font_size(self) -> int:
        return (
            self.sequence_generator_frame.sequence_generator_tab.main_widget.width()
            // 90
        )
