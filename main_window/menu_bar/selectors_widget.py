from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from main_window.menu_bar.base_selector import BaseSelector
from .user_profile_selector import UserProfileSelector
from .background_selector.background_selector import BackgroundSelector
from .prop_type_selector import PropTypeSelector
from .visibility_selector import VisibilitySelector

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class SelectorsWidget(QWidget):
    """Holds the user profile, prop, background, and visibility selectors."""

    def __init__(self, menu_bar: "MenuBarWidget") -> None:
        super().__init__(menu_bar)
        self.main_widget = menu_bar.main_widget

        # Instantiate selectors
        self.user_profile_selector = UserProfileSelector(menu_bar)
        self.prop_type_selector = PropTypeSelector(menu_bar)
        self.background_selector = BackgroundSelector(menu_bar)
        self.visibility_selector = VisibilitySelector(menu_bar)

        # Create labels
        self.user_profile_label = QLabel("User:")
        self.prop_type_label = QLabel("Prop:")
        self.background_label = QLabel("Background:")
        self.visibility_label = QLabel("")

        # Pair them up for convenience
        self.sections: list[tuple[QLabel, BaseSelector]] = [
            (self.user_profile_label, self.user_profile_selector),
            (self.prop_type_label, self.prop_type_selector),
            (self.background_label, self.background_selector),
            (self.visibility_label, self.visibility_selector),
        ]

        # Root layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add each section
        for label, selector in self.sections:
            self._add_section(label, selector)

        self.setLayout(self.layout)

    def _add_section(self, label: QLabel, selector: QWidget):
        """Adds a single label + selector to the layout."""
        section_layout = QVBoxLayout()
        section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.setSpacing(2)
        section_layout.setContentsMargins(0, 0, 0, 0)

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.addWidget(label)
        section_layout.addWidget(selector)

        # optional vertical separator between sections or you can do horizontal
        # but let's keep it simple:
        container = QWidget()
        container.setLayout(section_layout)

        # Possibly add a vertical line after each?
        # For example:
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)
        self.layout.addWidget(container)

    def style_selectors(self):
        """Applies style to each selector if needed."""
        self.selector_font_size = self.main_widget.height() // 50

        for _, selector in self.sections:
            selector.style_widget()

        # style the labels too
        font_size = self.selector_font_size
        self.user_profile_label.font().setPointSize(font_size)
        self.background_label.font().setPointSize(font_size)
        self.visibility_label.font().setPointSize(font_size)
