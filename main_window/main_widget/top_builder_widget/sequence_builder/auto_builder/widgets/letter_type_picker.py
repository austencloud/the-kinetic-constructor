from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from Enums.letters import LetterType

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_classes.base_auto_builder_frame import (
        BaseAutoBuilderFrame,
    )


class LetterTypePicker(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__(auto_builder_frame)
        self.auto_builder_frame = auto_builder_frame
        self.auto_builder_settings = self.auto_builder_frame.auto_builder_settings

        # Initialize UI components
        self._setup_components()
        self._setup_layout()
        self._connect_signals()
        self.apply_settings()

    def _setup_components(self):
        """Initialize checkboxes for each letter type."""
        self.title_label = QLabel("Select Letter Types")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.checkboxes: dict["LetterType", QCheckBox] = {}
        from Enums.letters import LetterType

        for letter_type in LetterType:
            checkbox = QCheckBox(letter_type.description)
            checkbox.setChecked(True)  # Default to all selected
            self.checkboxes[letter_type] = checkbox

    def _setup_layout(self):
        """Set up the layout for the widget."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for checkbox in self.checkboxes.values():
            checkboxes_layout.addWidget(checkbox)

        layout.addLayout(checkboxes_layout)
        self.setLayout(layout)

    def _connect_signals(self):
        """Connect checkbox signals to update settings."""
        for letter_type, checkbox in self.checkboxes.items():
            checkbox.stateChanged.connect(
                lambda state, lt=letter_type: self._on_checkbox_state_changed(lt, state)
            )

    def _on_checkbox_state_changed(self, letter_type, state):
        """Handle state change of checkboxes."""
        selected_types = self.get_selected_letter_types()
        self.auto_builder_settings.set_auto_builder_setting(
            "selected_letter_types",
            [lt.description for lt in selected_types],
            self.auto_builder_frame.builder_type,
        )

    def get_selected_letter_types(self) -> list["LetterType"]:
        """Return a list of selected letter types."""

        selected_types = []
        for letter_type, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected_types.append(letter_type)
        return selected_types

    def apply_settings(self):
        """Apply saved settings to the checkboxes."""
        saved_types = self.auto_builder_settings.get_auto_builder_setting(
            "selected_letter_types", self.auto_builder_frame.builder_type
        )

        if saved_types is None:
            # If no settings saved, default to all selected
            for checkbox in self.checkboxes.values():
                checkbox.setChecked(True)
        else:
            for letter_type, checkbox in self.checkboxes.items():
                checkbox.setChecked(letter_type.description in saved_types)

    def resize_letter_type_picker(self):
        """Adjust the size and style of the widget based on the parent size."""
        font_size = self.auto_builder_frame.auto_builder.sequence_builder.width() // 50
        self.title_label.setStyleSheet(f"font-weight: bold; font-size: {font_size}px;")
        for checkbox in self.checkboxes.values():
            checkbox.setStyleSheet(f"font-size: {font_size}px;")
