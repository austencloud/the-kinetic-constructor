from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from main_window.menu_bar_widget.base_selector import BaseSelector
from .user_profile_selector import UserProfileSelector
from .background_selector.background_selector import BackgroundSelector
from .prop_type_selector import PropTypeSelector
from .grid_mode_selector import GridModeSelector
from .visibility_selector import VisibilitySelector

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_window import MainWindow


class MenuBarWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

        # Initialize selectors
        self.user_profile_selector = UserProfileSelector(self)
        self.prop_type_selector = PropTypeSelector(self)
        self.grid_mode_selector = GridModeSelector(self)
        self.background_selector = BackgroundSelector(self)
        self.visibility_selector = VisibilitySelector(self)

        # Create labels for selectors
        self.user_profile_label = QLabel("User:")
        self.prop_type_label = QLabel("Prop:")
        self.grid_mode_label = QLabel("Grid:")
        self.background_label = QLabel("Background:")
        self.visibility_label = QLabel("")

        self.sections: list[tuple[QLabel, BaseSelector]] = [
            (self.user_profile_label, self.user_profile_selector),
            (self.prop_type_label, self.prop_type_selector),
            (self.grid_mode_label, self.grid_mode_selector),
            (self.background_label, self.background_selector),
            (self.visibility_label, self.visibility_selector),
        ]
        # set all the labels to be centered horizontally
        for label in self.sections:
            label[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels = [label for label, _ in self.sections]
        self.separators: list[QFrame] = []
        self.layout: QHBoxLayout = QHBoxLayout(self)

        self.layout.addStretch(1)

        # Add selectors with labels and separators
        for i, (label, selector) in enumerate(self.sections):
            self.add_section(label, selector)
            if i < len(self.sections) - 1:
                self.add_separator()

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def add_section(self, label: QLabel, selector: QWidget):
        section_layout = QVBoxLayout()
        section_layout.setSpacing(2)  # Minimal vertical spacing
        section_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no extra vertical padding
        section_layout.addWidget(label)
        section_layout.addWidget(selector)
        self.layout.addLayout(section_layout)

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        self.layout.addWidget(separator)
        self.separators.append(separator)

    def resize_menu_bar_widget(self):
        self.menu_bar_font_size = self.main_widget.width() // 120
        spacing = self.width() // 30  # Horizontal spacing between sections
        self.layout.setSpacing(spacing)
        font_size = self.main_widget.width() // 145
        for label in self.labels:
            font = QFont("Georgia", font_size)
            label.setFont(font)

        # Style selectors
        for _, selector in self.sections:
            selector.style_widget()

        for separator in self.separators:
            separator.setLineWidth(1)
        self.setMaximumWidth(self.main_widget.width())
