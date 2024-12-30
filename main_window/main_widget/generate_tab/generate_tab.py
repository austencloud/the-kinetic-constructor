from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QStackedLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.freeform.custom_checkbox_widget import (
    CustomCheckBoxWidget,
)
from .customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import GenerateSequenceButton
from .circular.circular_sequence_generator_frame import CircularSequenceGeneratorFrame
from .freeform.freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = main_widget.main_window.settings_manager.global_settings
        self.overwrite_connected = False
        self.current_sequence_generator = "freeform"

        self._setup_spacers()
        self._setup_buttons()
        self._setup_components()
        self._connect_signals()
        self._setup_layout()

        self.freeform_generator_frame.show()

    def _setup_components(self):
        self.overwrite_checkbox = CustomCheckBoxWidget("Overwrite sequence")

        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.freeform_generator_frame = FreeformSequenceGeneratorFrame(self)
        self.circular_generator_frame = CircularSequenceGeneratorFrame(self)

    def _connect_signals(self):
        self.freeform_button.clicked.connect(self.freeform_generator_frame.show)
        self.circular_button.clicked.connect(self.circular_generator_frame.show)

    def _setup_layout(self):
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.freeform_generator_frame)
        self.stacked_layout.addWidget(self.circular_generator_frame)

        top_hbox = QHBoxLayout()
        top_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_hbox.addWidget(self.customize_sequence_label)

        generate_button_hbox = QHBoxLayout()
        generate_button_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        generate_button_hbox.addWidget(self.generate_sequence_button)

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.checkbox_layout.addWidget(self.overwrite_checkbox)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addLayout(top_hbox)
        self.layout.addItem(self.spacer_1)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.stacked_layout)
        self.layout.addItem(self.spacer_2)
        self.layout.addLayout(generate_button_hbox)
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addItem(self.spacer_3)
        self.setLayout(self.layout)

    def _setup_spacers(self):
        self.spacers: list[QSpacerItem] = []
        for _ in range(3):
            spacer = QSpacerItem(
                0,
                self.main_widget.height() // 20,
                QSizePolicy.Policy.Minimum,
            )
            self.spacers.append(spacer)
        self.spacer_1, self.spacer_2, self.spacer_3 = self.spacers


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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.freeform_generator_frame._resize_sequence_generator_frame()
        self.circular_generator_frame._resize_sequence_generator_frame()
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
        self._resize_spacers()
        self.overwrite_checkbox.label.setFont(QFont("Arial", self.height() // 50, 0))

    def _resize_spacers(self):
        for spacer in [self.spacer_1, self.spacer_2, self.spacer_3]:
            spacer.changeSize(0, self.main_widget.height() // 20)
