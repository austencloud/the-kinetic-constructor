# menu_bar_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont

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
        self.prop_type_selector = PropTypeSelector(self)
        self.grid_mode_selector = GridModeSelector(self)
        self.visibility_selector = VisibilitySelector(self)
        self.background_selector = BackgroundSelector(self)
        self.user_profile_selector = UserProfileSelector(self)

        # Create labels for selectors
        self.prop_type_label = QLabel("Prop:")
        self.grid_mode_label = QLabel("Grid:")
        self.visibility_label = QLabel("Visibility:")
        self.background_label = QLabel("Background:")
        self.user_profile_label = QLabel("User:")

        # List of sections: (label, selector)
        self.sections: list[tuple[QLabel, BaseSelector]] = [
            (self.prop_type_label, self.prop_type_selector),
            (self.grid_mode_label, self.grid_mode_selector),
            (self.visibility_label, self.visibility_selector),
            (self.background_label, self.background_selector),
            (self.user_profile_label, self.user_profile_selector),
        ]

        # Collect labels for font resizing
        self.labels = [label for label, _ in self.sections]
        self.separators: list[QFrame] = []
        # Set up layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        # self.layout.setContentsMargins(10, 10, 10, 10)

        self.layout.addStretch(1)

        # Add selectors with labels and separators
        for i, (label, selector) in enumerate(self.sections):
            self.add_section(label, selector)
            if i < len(self.sections) - 1:
                self.add_separator()

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def add_section(self, label: QLabel, selector: QWidget):
        section_layout = QHBoxLayout()
        section_layout.setSpacing(5)
        section_layout.addWidget(label)
        section_layout.addWidget(selector)
        section_layout.addStretch(1)  # Add stretch to push the selector to the left
        self.layout.addLayout(section_layout)

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        self.layout.addWidget(separator)
        self.separators.append(separator)


    def resize_menu_bar_widget(self):
        spacing = self.width() // 30
        self.layout.setSpacing(spacing)
        font_size = self.main_widget.height() // 75
        for label in self.labels:
            font = QFont("Arial", font_size)
            label.setFont(font)

        # Style selectors
        for _, selector in self.sections:
            selector.style_widget()

        for separator in self.separators:
            separator.setLineWidth(1)
        self.setMaximumWidth(self.main_widget.width())