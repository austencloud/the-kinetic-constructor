from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from main_window.main_widget.build_tab.sequence_generator.freeform.custom_checkbox_widget import (
    CustomCheckBoxWidget,
)

from .base_classes.customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import GenerateSequenceButton
from .circular.circular_sequence_generator_frame import CircularSequenceGeneratorFrame
from .freeform.freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame

if TYPE_CHECKING:
    from main_window.main_widget.build_tab.build_tab import BuildTab


class SequenceGenerator(QWidget):
    def __init__(self, build_tab: "BuildTab"):
        super().__init__(build_tab)
        self.build_tab = build_tab
        self.main_widget = build_tab.main_widget
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.overwrite_connected = False
        self.current_sequence_generator = "freeform"

        self.internal_stacked_widget = QStackedWidget(self)

        self._setup_spacers()
        self._setup_buttons()
        self._setup_checkbox()
        self._setup_components()
        self._connect_signals()
        self._setup_layout()

        self.internal_stacked_widget.addWidget(self.freeform_generator_frame)
        self.internal_stacked_widget.addWidget(self.circular_generator_frame)
        self.generate_sequence_button.clicked.connect(self.dummy_function)

    def _setup_components(self):
        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.freeform_generator_frame = FreeformSequenceGeneratorFrame(self)
        self.circular_generator_frame = CircularSequenceGeneratorFrame(self)

    def _connect_signals(self):
        self.freeform_button.clicked.connect(self.show_freeform)
        self.circular_button.clicked.connect(self.show_circular)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.layout.addWidget(
            self.customize_sequence_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addItem(self.spacer_1)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.internal_stacked_widget)
        self.layout.addItem(self.spacer_2)
        self.layout.addWidget(
            self.generate_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addItem(self.spacer_3)

    def _setup_spacers(self):
        self.spacer_1 = QSpacerItem(
            0,
            self.main_widget.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed,
        )
        self.spacer_2 = QSpacerItem(
            0,
            self.main_widget.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed,
        )
        self.spacer_3 = QSpacerItem(
            0,
            self.main_widget.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed,
        )

    def _setup_checkbox(self):
        self.overwrite_checkbox = CustomCheckBoxWidget("Overwrite sequence")
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

    def dummy_function(self):
        """Placeholder function to ensure there's always a connected slot."""

    def show_freeform(self):
        """Display the FreeformSequenceGeneratorFrame with fade animation."""
        if self.current_sequence_generator == "freeform":
            return  # Already showing
        self.current_sequence_generator = "freeform"
        self.update_button_styles()
        self._fade_transition(to_index=0)

    def show_circular(self):
        """Display the CircularSequenceGeneratorFrame with fade animation."""
        if self.current_sequence_generator == "circular":
            return  # Already showing
        self.current_sequence_generator = "circular"
        self.update_button_styles()
        self._fade_transition(to_index=1)

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

    def _fade_transition(self, to_index: int):
        """Handle fade-out and fade-in animations when switching sequence generators."""
        self.opacity_effect = QGraphicsOpacityEffect(self.internal_stacked_widget)
        self.internal_stacked_widget.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(200)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(lambda: self._switch_internal_content(to_index))
        self.fade_out.start()

    def _switch_internal_content(self, to_index: int):
        """Switch the internal content and start fade-in."""
        self.internal_stacked_widget.setCurrentIndex(to_index)

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(200)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.freeform_generator_frame._resize_sequence_generator_frame()
        self.circular_generator_frame._resize_sequence_generator_frame()
        self.customize_sequence_label.resize_customize_sequence_label()
        self.generate_sequence_button.resize_generate_sequence_button()

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
            spacer.changeSize(
                0,
                self.main_widget.height() // 20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Fixed,
            )

