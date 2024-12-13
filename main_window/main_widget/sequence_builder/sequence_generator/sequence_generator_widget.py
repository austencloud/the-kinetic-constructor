from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QStackedLayout,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_builder.sequence_generator.base_classes.customize_your_sequence_label import (
    CustomizeSequenceLabel,
)
from main_window.main_widget.sequence_builder.sequence_generator.generate_sequence_button import (
    GenerateSequenceButton,
)
from .circular.circular_sequence_generator_frame import CircularSequenceGeneratorFrame
from .freeform.freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QStackedLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_builder.sequence_generator.base_classes.customize_your_sequence_label import (
    CustomizeSequenceLabel,
)
from .circular.circular_sequence_generator_frame import CircularSequenceGeneratorFrame
from .freeform.freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceGeneratorWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = main_widget.main_window.settings_manager.global_settings
        self.overwrite_connected = False

        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self._setup_spacers()
        self._setup_buttons()
        self._setup_checkbox()

        self.freeform_builder_frame = FreeformSequenceGeneratorFrame(self)
        self.circular_builder_frame = CircularSequenceGeneratorFrame(self)
        self.freeform_button.clicked.connect(self.freeform_builder_frame.show)
        self.circular_button.clicked.connect(self.circular_builder_frame.show)

        self._setup_layout()

        self.current_sequence_generator = "freeform"
        self.freeform_builder_frame.show()

    def _setup_layout(self):
        # Set up stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.freeform_builder_frame)
        self.stacked_layout.addWidget(self.circular_builder_frame)

        # Set up main layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)
        alignment = Qt.AlignmentFlag.AlignCenter

        # Add widgets to layout
        self.layout.addWidget(self.customize_sequence_label, alignment=alignment)
        self.layout.addItem(self.spacer_1)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.stacked_layout)
        self.layout.addItem(self.spacer_2)
        self.layout.addWidget(self.generate_sequence_button, alignment=alignment)
        self.layout.addLayout(self.checkbox_layout)

    def _setup_spacers(self):
        self.spacer_1 = QSpacerItem(
            0, self.main_widget.height() // 20, QSizePolicy.Policy.Minimum
        )
        self.spacer_2 = QSpacerItem(
            0, self.main_widget.height() // 20, QSizePolicy.Policy.Minimum
        )

    def _setup_checkbox(self):
        self.overwrite_checkbox = QCheckBox("Overwrite sequence")
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.checkbox_layout.addWidget(self.overwrite_checkbox)

    def _setup_buttons(self):
        """Set up Freeform and Circular buttons and add them to the layout."""
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.freeform_button = QPushButton("Freeform")
        self.circular_button = QPushButton("Circular")

        for button in [self.freeform_button, self.circular_button]:
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button_layout.addWidget(button)

        self.buttons = {
            "freeform": self.freeform_button,
            "circular": self.circular_button,
        }
        self.generate_sequence_button = GenerateSequenceButton(self)
        self.generate_sequence_button.clicked.connect(self.dummy_function)

    def dummy_function(self):
        """Placeholder function to ensure there's always a connected slot."""

    def update_button_styles(self):
        """Apply active and inactive styles across all main buttons."""
        font_size = self.main_widget.width() // 75
        active_style = "background-color: lightblue; font-weight: bold;"
        inactive_style = "background-color: none; font-weight: normal;"

        for key, button in self.buttons.items():
            style = (
                active_style
                if self.current_sequence_generator == key
                else inactive_style
            )
            button.setStyleSheet(f"{style} font-size: {font_size}px; padding: 8px;")

    def resize_sequence_generator(self) -> None:
        """Resize handler for the auto builder UI."""
        self.freeform_builder_frame._resize_sequence_generator_frame()
        self.circular_builder_frame._resize_sequence_generator_frame()
        self.customize_sequence_label.resize_customize_sequence_label()
        self.generate_sequence_button.resize_generate_sequence_button()

        # Update button sizes
        for button in self.buttons.values():
            button.setMinimumHeight(self.main_widget.height() // 16)
            button.setFixedWidth(self.main_widget.width() // 10)

        self.update_button_styles()

        font = self.overwrite_checkbox.font()
        font.setPointSize(self.main_widget.height() // 65)
        self.overwrite_checkbox.setFont(font)

        self.spacer_1.changeSize(0, self.main_widget.height() // 20)
        self.spacer_2.changeSize(0, self.main_widget.height() // 20)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sequence_generator()
