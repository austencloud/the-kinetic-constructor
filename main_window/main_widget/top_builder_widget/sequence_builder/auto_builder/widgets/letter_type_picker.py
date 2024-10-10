from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor
from matplotlib.pylab import f
from Enums.letters import LetterType
from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker_scroll_area.letter_type_text_painter import (
    LetterTypeTextPainter,
)

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_classes.base_auto_builder_frame import (
        BaseAutoBuilderFrame,
    )


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, letter_type_picker: "LetterTypePicker", letter_type: LetterType):
        super().__init__(letter_type_picker)
        self.letter_type = letter_type
        self.letter_type_picker = letter_type_picker
        self.is_checked = True  # Default state
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.setText(self._get_colored_text())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Apply initial styles
        self.setStyleSheet("padding: 10px; font-weight: bold; border-radius: 10px;")
        self.update_style()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _get_colored_text(self) -> str:
        """Use LetterTypeTextPainter to style the text."""
        styled_description = LetterTypeTextPainter.get_colored_text(
            self.letter_type.description
        )
        return f"<b>{self.letter_type.name}</b><br>{styled_description}"

    def mousePressEvent(self, event):
        """Toggle the check state and emit clicked signal."""
        self.is_checked = not self.is_checked
        self.update_style()
        self.clicked.emit()

    def update_style(self):
        """Update the visual style based on the checked state."""
        font_size = self.letter_type_picker.width() // 45
        if self.is_checked:
            self.setStyleSheet(
                "background-color: #00b3ff; "
                "color: white; "
                "padding: 10px; "
                "font-weight: bold; "
                "border-radius: 10px;"
                f"font-size: {font_size}px;"
            )
        else:
            self.setStyleSheet(
                "background-color: #f0f0f0; "
                "color: black; "
                "padding: 10px; "
                "font-weight: bold; "
                "border-radius: 10px;"
                f"font-size: {font_size}px;"
            )
        self.setText(self._get_colored_text())


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
        font_size = self.auto_builder_frame.auto_builder.sequence_builder.width() // 40

        self.title_label.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  font-size: {font_size}px;"
            f"  font-weight: bold;"
            f"}}"
        )

        self.labels: dict["LetterType", ClickableLabel] = {}
        for letter_type in LetterType:
            label = ClickableLabel(self, letter_type)
            self.labels[letter_type] = label

    def _setup_layout(self):
        """Set up the HBox layout for all letter types."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        hbox_layout = QHBoxLayout()
        hbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_layout.addStretch(1)
        
        for label in self.labels.values():
            hbox_layout.addWidget(label)
            hbox_layout.addStretch(1)

        layout.addLayout(hbox_layout)
        self.setLayout(layout)

    def _connect_signals(self):
        """Connect label click signals to update settings."""
        for letter_type, label in self.labels.items():
            label.clicked.connect(lambda lt=letter_type: self._on_label_clicked(lt))

    def _on_label_clicked(self, letter_type: LetterType):
        """Handle label click and toggle its state."""
        label = self.labels[letter_type]
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
        for letter_type, label in self.labels.items():
            if label.is_checked:
                selected_types.append(letter_type)
        return selected_types

    def apply_settings(self):
        """Apply saved settings to the labels."""
        saved_types = self.auto_builder_settings.get_auto_builder_setting(
            "selected_letter_types", self.auto_builder_frame.builder_type
        )

        if saved_types is None:
            for label in self.labels.values():
                label.is_checked = True
                label.update_style()
        else:
            for letter_type, label in self.labels.items():
                is_selected = letter_type.description in saved_types
                label.is_checked = is_selected
                label.update_style()

    def resize_letter_type_picker(self):
        """Adjust the size and style of the widget based on the parent size."""
        font_size = self.auto_builder_frame.auto_builder.sequence_builder.width() // 45
        self.title_label.setStyleSheet(f"font-weight: bold; font-size: {font_size}px;")
        for label in self.labels.values():
            label.update_style()
