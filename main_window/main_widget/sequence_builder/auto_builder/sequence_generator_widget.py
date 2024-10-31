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
from main_window.main_widget.sequence_builder.auto_builder.generate_sequence_button import (
    GenerateSequenceButton,
)
from .circular.circular_auto_builder_frame import CircularAutoBuilderFrame
from .freeform.freeform_auto_builder_frame import FreeformAutoBuilderFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QStackedLayout
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
        self.global_settings = main_widget.main_window.settings_manager.global_settings

        # Main layout containing all widgets
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Top label and buttons
        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.layout.addWidget(
            self.customize_sequence_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addStretch(1)

        # Freeform and Circular buttons
        self._setup_buttons()

        # Stacked layout for Freeform and Circular frames
        self.stacked_layout = QStackedLayout()
        self.freeform_builder_frame = FreeformAutoBuilderFrame(self)
        self.circular_builder_frame = CircularAutoBuilderFrame(self)
        self.stacked_layout.addWidget(self.freeform_builder_frame)
        self.stacked_layout.addWidget(self.circular_builder_frame)
        self.layout.addLayout(self.stacked_layout)

        # Add the Create Sequence button
        self.generate_sequence_button = GenerateSequenceButton(self)
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.generate_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Default to showing Freeform frame
        self.current_auto_builder = "freeform"
        self.show_freeform_frame()

    def _setup_buttons(self):
        """Set up Freeform and Circular buttons and add them to the layout."""
        self.button_layout = QHBoxLayout()
        self.freeform_button = QPushButton("Freeform")
        self.circular_button = QPushButton("Circular")

        # Connect signals for frame switching
        self.freeform_button.clicked.connect(self.show_freeform_frame)
        self.circular_button.clicked.connect(self.show_circular_frame)

        # Apply the same cursor and add to the button layout
        for button in [self.freeform_button, self.circular_button]:
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button_layout.addWidget(button)

        self.layout.addLayout(self.button_layout)

        # Store buttons for easy style updates
        self.buttons = {
            "freeform": self.freeform_button,
            "circular": self.circular_button,
        }

    def show_freeform_frame(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.freeform_builder_frame)
        self.current_auto_builder = "freeform"
        self.update_button_styles()

        # Reconnect the create sequence button to Freeform's create function
        # self.generate_sequence_button.clicked.disconnect()
        self.generate_sequence_button.clicked.connect(
            self.freeform_builder_frame.on_create_sequence
        )

    def show_circular_frame(self):
        """Display Circular frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.circular_builder_frame)
        self.current_auto_builder = "circular"
        self.update_button_styles()

        # Reconnect the create sequence button to Circular's create function
        self.generate_sequence_button.clicked.disconnect()
        self.generate_sequence_button.clicked.connect(
            self.circular_builder_frame.on_create_sequence
        )

    def update_button_styles(self):
        """Apply active and inactive styles across all main buttons."""
        font_size = self.main_widget.width() // 75
        active_style = "background-color: lightblue; font-weight: bold;"
        inactive_style = "background-color: none; font-weight: normal;"

        # Update each button with active/inactive style
        for key, button in self.buttons.items():
            style = active_style if self.current_auto_builder == key else inactive_style
            button.setStyleSheet(f"{style} font-size: {font_size}px; padding: 8px;")

    def resize_sequence_generator(self):
        """Resize handler for the auto builder UI."""
        # Resize frames
        self.freeform_builder_frame._resize_auto_builder_frame()
        self.circular_builder_frame._resize_auto_builder_frame()
        self.customize_sequence_label.resize_customize_sequence_label()
        self.generate_sequence_button.resize_generate_sequence_button()
        
        # Update button sizes
        for button in self.buttons.values():
            button.setMinimumHeight(self.main_widget.height() // 16)
            button.setFixedWidth(self.main_widget.width() // 10)

        self.update_button_styles()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sequence_generator()
