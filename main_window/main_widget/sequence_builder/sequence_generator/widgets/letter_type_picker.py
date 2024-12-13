from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from Enums.letters import LetterType
from .custom_letter_type_button import CustomLetterTypeButton

if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class LetterTypePicker(QWidget):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__(sequence_generator_frame)
        self.sequence_generator_frame = sequence_generator_frame
        self.sequence_generator_settings = (
            self.sequence_generator_frame.sequence_generator_settings
        )

        # Initialize UI components
        self._setup_components()
        self._setup_layout()
        self._connect_signals()
        self.apply_settings()

    def _setup_components(self):
        """Initialize clickable labels for each letter type."""
        self.title_label = QLabel("Select Letter Types")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_size = self.get_font_size()

        self.title_label.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  font-size: {font_size}px;"
            f"  font-weight: bold;"
            f"}}"
        )

        self.buttons: dict["LetterType", CustomLetterTypeButton] = {}
        for letter_type in LetterType:
            letter_type_button = CustomLetterTypeButton(self, letter_type)
            self.buttons[letter_type] = letter_type_button

    def get_font_size(self) -> int:
        """Return the font size based on the parent widget's width."""
        return (
            self.sequence_generator_frame.sequence_generator_widget.main_widget.width()
            // 90
        )

    def _setup_layout(self):
        """Set up the layout for a two-row, three-column arrangement of letter type buttons."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Create two rows with three buttons each
        row_layouts = [QHBoxLayout(), QHBoxLayout()]
        row_layouts[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        row_layouts[1].setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add buttons to rows in a two-row, three-column format
        buttons = list(self.buttons.values())
        for i in range(3):
            row_layouts[0].addWidget(buttons[i])  # First three buttons in first row
            row_layouts[1].addWidget(buttons[i + 3])  # Next three buttons in second row

        # Add each row layout to the main layout
        layout.addLayout(row_layouts[0])
        layout.addLayout(row_layouts[1])

        self.setLayout(layout)

    def _connect_signals(self):
        """Connect label click signals to update settings."""
        for letter_type, label in self.buttons.items():
            label.clicked.connect(lambda lt=letter_type: self._on_label_clicked(lt))

    def _on_label_clicked(self, letter_type: LetterType):
        """Handle label click and toggle its state."""
        label = self.buttons[letter_type]
        label.update_style()

        selected_types = self.get_selected_letter_types()
        self.sequence_generator_settings.set_sequence_generator_setting(
            "selected_letter_types",
            [lt.description for lt in selected_types],
            self.sequence_generator_frame.builder_type,
        )

    def get_selected_letter_types(self) -> list["LetterType"]:
        """Return a list of selected letter types."""
        selected_types = []
        for letter_type, label in self.buttons.items():
            if label.is_checked:
                selected_types.append(letter_type)
        return selected_types

    def apply_settings(self):
        """Apply saved settings to the labels."""
        saved_types = self.sequence_generator_settings.get_sequence_generator_setting(
            "selected_letter_types", self.sequence_generator_frame.builder_type
        )

        if saved_types is None:
            for label in self.buttons.values():
                label.is_checked = True
                label.update_style()
        else:
            for letter_type, label in self.buttons.items():
                is_selected = letter_type.description in saved_types
                label.is_checked = is_selected
                label.update_style()

    def resizeEvent(self, event):
        """Adjust font sizes and button styles on resize."""
        font_size = self.get_font_size()
        self.title_label.setStyleSheet(f"font-weight: bold; font-size: {font_size}px;")
        for button in self.buttons.values():
            button.update_style()
