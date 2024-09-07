from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from typing import TYPE_CHECKING

from .freeform_auto_builder_frame import FreeformAutoBuilderDialog
from .circular_auto_builder_frame import CircularAutoBuilderDialog

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class AutoBuilderSelectionDialog(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.setWindowTitle("Select Auto Builder")

        # Dynamic font size based on widget size
        self.button_font_size = int(self.sequence_widget.width() * 0.03)
        self.description_font_size = int(self.sequence_widget.width() * 0.015)

        self.description_labels: dict[str, QLabel] = {}

        self._setup_ui()
        self.resize_dialog()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Create a horizontal layout for the Freeform and Circular options
        button_layout = QHBoxLayout()

        # Calculate button sizes (square buttons)
        button_size = int(self.sequence_widget.width() * 0.3)

        # Create the Freeform and Circular buttons and layouts programmatically
        self.freeform_button, freeform_layout = self._create_option_button(
            "Freeform",
            "Randomly generated sequence",
            button_size,
            self.open_freeform_builder,
        )
        self.circular_button, circular_layout = self._create_option_button(
            "Circular",
            "Ends at starting position",
            button_size,
            self.open_circular_builder,
        )

        # Add the layouts to the button layout
        button_layout.addLayout(freeform_layout)
        button_layout.addLayout(circular_layout)

        self.buttons: dict[str, QPushButton] = {
            "freeform": self.freeform_button,
            "circular": self.circular_button,
        }

        # Add the button layout to the main layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _create_option_button(
        self, label: str, description: str, button_size: int, callback
    ):

        # Button setup
        button = QPushButton(label)
        button.setFixedSize(button_size, button_size)
        button.setFont(QFont("Arial", self.button_font_size))
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(callback)

        # Description setup
        description_label = QLabel(description)
        description_label.setFont(QFont("Arial", self.description_font_size))
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_labels[label.lower()] = description_label

        # Layout setup
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)

        return button, layout

    def open_freeform_builder(self):
        self.close()
        dialog = FreeformAutoBuilderDialog(self.sequence_widget)
        dialog.exec()
        self.accept()

    def open_circular_builder(self):
        self.close()
        dialog = CircularAutoBuilderDialog(self.sequence_widget)
        dialog.exec()
        self.accept()

    def resize_dialog(self):
        width, height = (
            int(self.sequence_widget.width() / 2),
            int(self.sequence_widget.height() / 3),
        )
        self.resize(width, height)

        button_font = QFont()
        button_font_size = width // 30
        button_font.setPointSize(button_font_size)

        for button in self.buttons.values():
            button.setFont(button_font)

        description_font = QFont()
        description_font_size = width // 45
        description_font.setPointSize(description_font_size)

        for label in self.description_labels.values():
            label.setFont(description_font)