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

        # Main layout containing all widgets
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Top label and buttons
        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.layout.addWidget(
            self.customize_sequence_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # self.layout.addStretch(1)
        # create a spacer item below the label
        self.spacer_1 = QSpacerItem(
            0, self.main_widget.height() // 20, QSizePolicy.Policy.Minimum
        )
        self.layout.addItem(self.spacer_1)

        self._setup_buttons()

        self.stacked_layout = QStackedLayout()
        self.freeform_builder_frame = FreeformSequenceGeneratorFrame(self)
        self.circular_builder_frame = CircularSequenceGeneratorFrame(self)
        self.stacked_layout.addWidget(self.freeform_builder_frame)
        self.stacked_layout.addWidget(self.circular_builder_frame)
        self.layout.addLayout(self.stacked_layout)

        self.spacer_2 = QSpacerItem(
            0, self.main_widget.height() // 20, QSizePolicy.Policy.Minimum
        )
        self.layout.addItem(self.spacer_2)
        self.layout.addWidget(
            self.generate_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.overwrite_checkbox = QCheckBox("Overwrite sequence")

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch(1)
        checkbox_layout.addWidget(self.overwrite_checkbox)
        checkbox_layout.addStretch(1)
        self.layout.addLayout(checkbox_layout)
        self.current_sequence_generator = "freeform"
        self.show_freeform_frame()

    def _setup_buttons(self):
        """Set up Freeform and Circular buttons and add them to the layout."""
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.freeform_button = QPushButton("Freeform")
        self.circular_button = QPushButton("Circular")

        self.freeform_button.clicked.connect(self.show_freeform_frame)
        self.circular_button.clicked.connect(self.show_circular_frame)

        for button in [self.freeform_button, self.circular_button]:
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button_layout.addWidget(button)
        self.layout.addLayout(self.button_layout)

        self.buttons = {
            "freeform": self.freeform_button,
            "circular": self.circular_button,
        }
        self.generate_sequence_button = GenerateSequenceButton(self)
        self.generate_sequence_button.clicked.connect(self.dummy_function)

    def dummy_function(self):
        """Placeholder function to ensure there's always a connected slot."""

    def show_freeform_frame(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.freeform_builder_frame)
        self.current_sequence_generator = "freeform"
        self.update_button_styles()

        if self.overwrite_connected:
            try:
                self.overwrite_checkbox.stateChanged.disconnect()
            except TypeError:
                pass
            self.overwrite_connected = False

        overwrite_value = self.main_widget.settings_manager.builder_settings.sequence_generator.get_sequence_generator_setting(
            "overwrite_sequence", self.current_sequence_generator
        )

        if isinstance(overwrite_value, bool):
            overwrite_bool = overwrite_value
        elif isinstance(overwrite_value, str):
            overwrite_bool = overwrite_value.lower() == "true"
        else:
            overwrite_bool = False

        self.overwrite_checkbox.setChecked(overwrite_bool)

        self.overwrite_checkbox.stateChanged.connect(
            lambda state: self.main_widget.settings_manager.builder_settings.sequence_generator.set_sequence_generator_setting(
                "overwrite_sequence",
                state == 2,
                self.current_sequence_generator,
            )
        )
        self.overwrite_connected = True

        self.generate_sequence_button.clicked.disconnect()
        self.generate_sequence_button.clicked.connect(
            lambda: self.freeform_builder_frame.on_create_sequence(
                self.overwrite_checkbox.isChecked()
            )
        )

    def show_circular_frame(self):
        """Display Circular frame by setting it in the stacked layout."""
        self.stacked_layout.setCurrentWidget(self.circular_builder_frame)
        self.current_sequence_generator = "circular"
        self.update_button_styles()

        if self.overwrite_connected:
            try:
                self.overwrite_checkbox.stateChanged.disconnect()
            except TypeError:
                pass
            self.overwrite_connected = False

        overwrite_value = self.main_widget.settings_manager.builder_settings.sequence_generator.get_sequence_generator_setting(
            "overwrite_sequence", self.current_sequence_generator
        )

        if isinstance(overwrite_value, bool):
            overwrite_bool = overwrite_value
        elif isinstance(overwrite_value, str):
            overwrite_bool = overwrite_value.lower() == "true"
        else:
            overwrite_bool = False

        self.overwrite_checkbox.setChecked(overwrite_bool)

        self.overwrite_checkbox.stateChanged.connect(
            lambda state: self.main_widget.settings_manager.builder_settings.sequence_generator.set_sequence_generator_setting(
                "overwrite_sequence",
                state == 2,
                self.current_sequence_generator,
            )
        )
        self.overwrite_connected = True

        self.generate_sequence_button.clicked.disconnect()
        self.generate_sequence_button.clicked.connect(
            lambda: self.circular_builder_frame.on_create_sequence(
                self.overwrite_checkbox.isChecked()
            )
        )

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
        font.setPointSize(self.main_widget.height() // 85)
        self.overwrite_checkbox.setFont(font)

        self.spacer_1.changeSize(0, self.main_widget.height() // 20)
        self.spacer_2.changeSize(0, self.main_widget.height() // 20)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sequence_generator()
