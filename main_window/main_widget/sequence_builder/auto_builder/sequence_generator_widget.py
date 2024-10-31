from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QStackedLayout,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_builder.auto_builder.base_classes.customize_your_sequence_label import (
    CustomizeSequenceLabel,
)
from .circular.circular_auto_builder_frame import CircularAutoBuilderFrame
from .freeform.freeform_auto_builder_frame import FreeformAutoBuilderFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceGeneratorWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        # Main layout containing buttons and stacked layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create top bar with Freeform and Circular buttons
        self.button_layout = QHBoxLayout()
        self.freeform_button = QPushButton("Freeform")
        self.circular_button = QPushButton("Circular")
        self.freeform_button.clicked.connect(self.show_freeform_frame)
        self.circular_button.clicked.connect(self.show_circular_frame)
        self.freeform_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.circular_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.customize_sequence_label = CustomizeSequenceLabel(self)

        self.layout.addWidget(
            self.customize_sequence_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addStretch(1)
        self.buttons: dict[str, QPushButton] = {
            "freeform": self.freeform_button,
            "circular": self.circular_button,
        }
        # Add buttons to layout
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.freeform_button)
        self.button_layout.addWidget(self.circular_button)
        self.layout.addLayout(self.button_layout)

        # Stacked layout for Freeform and Circular frames
        self.stacked_layout = QStackedLayout()
        self.freeform_builder_frame = FreeformAutoBuilderFrame(self)
        self.circular_builder_frame = CircularAutoBuilderFrame(self)
        self.stacked_layout.addWidget(self.freeform_builder_frame)
        self.stacked_layout.addWidget(self.circular_builder_frame)
        self.layout.addLayout(self.stacked_layout)
        self.create_sequence_button = QPushButton("Create Sequence")
        self.create_sequence_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.current_auto_builder = "freeform"
        self.show_freeform_frame()

    def show_freeform_frame(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.freeform_builder_frame)
        self.current_auto_builder = "freeform"
        self.update_button_styles()
        # disconnect the previous signal
        self.create_sequence_button.disconnect()
        self.create_sequence_button.clicked.connect(
            self.freeform_builder_frame.on_create_sequence
        )

    def show_circular_frame(self):
        """Display Circular frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.circular_builder_frame)
        self.current_auto_builder = "circular"
        self.update_button_styles()
        self.create_sequence_button.disconnect()
        self.create_sequence_button.clicked.connect(
            self.circular_builder_frame.on_create_sequence
        )

    def update_button_styles(self):
        """Update button styles to reflect the active frame."""
        active_style = "background-color: lightblue; font-weight: bold;"
        inactive_style = "background-color: none; font-weight: normal;"
        button_font_size = self.main_widget.width() // 75
        font_size = f"font-size: {button_font_size}px;"

        self.freeform_button.setStyleSheet(
            active_style + font_size
            if self.current_auto_builder == "freeform"
            else inactive_style + font_size
        )
        self.circular_button.setStyleSheet(
            active_style + font_size
            if self.current_auto_builder == "circular"
            else inactive_style + font_size
        )

    def load_last_used_auto_builder(self, builder_type: str):
        """Load the last used auto builder (Freeform or Circular)."""
        if builder_type == "freeform":
            self.show_freeform_frame()
        elif builder_type == "circular":
            self.show_circular_frame()

    def get_current_auto_builder_type(self) -> str:
        """Return the currently open auto builder type."""
        return self.current_auto_builder

    def resize_sequence_generator(self):
        """Resize handler for the auto builder UI."""

        self.freeform_builder_frame._resize_auto_builder_frame()
        self.circular_builder_frame._resize_auto_builder_frame()
        self.customize_sequence_label.resize_customize_sequence_label()  # Resize the label

        for button in self.buttons.values():
            button.setMinimumHeight(self.main_widget.height() // 16)
            button.setFixedWidth(self.main_widget.width() // 10)

        self.update_button_styles()
        font_size = self.main_widget.width() // 75
        self.create_sequence_button.setStyleSheet(f"font-size: {font_size}px;")
        self.create_sequence_button.updateGeometry()
        self.create_sequence_button.repaint()

        self.create_sequence_button.setFixedWidth(self.main_widget.width() // 4)
        self.create_sequence_button.setFixedHeight(self.main_widget.height() // 14)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sequence_generator()
