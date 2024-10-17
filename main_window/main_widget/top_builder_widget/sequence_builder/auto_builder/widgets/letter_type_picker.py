from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from Enums.letters import LetterType
from .custom_letter_type_button import CustomLetterTypeButton

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


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
        return self.auto_builder_frame.sequence_generator_tab.main_widget.width() // 70

    def _setup_layout(self):
        """Set up the HBox layout for all letter types."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        hbox_layout = QHBoxLayout()
        hbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_layout.addStretch(2)

        for label in self.buttons.values():
            hbox_layout.addWidget(label)
            hbox_layout.addStretch(1)

        hbox_layout.addStretch(1)
        layout.addLayout(hbox_layout)
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
        self.auto_builder_settings.set_auto_builder_setting(
            "selected_letter_types",
            [lt.description for lt in selected_types],
            self.auto_builder_frame.builder_type,
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
        saved_types = self.auto_builder_settings.get_auto_builder_setting(
            "selected_letter_types", self.auto_builder_frame.builder_type
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
