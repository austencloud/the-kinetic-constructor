from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize

# Import the new classes
from .social_media_widget import SocialMediaWidget
from .selectors_widget import SelectorsWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MenuBarWidget(QWidget):
    """Minimal manager that instantiates and positions social media + selectors."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        # Layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)

        # Create sub-widgets
        self.social_media_widget = SocialMediaWidget(self)
        self.selectors_widget = SelectorsWidget(self)

        # Add them to the layout
        self.layout.addStretch(1)
        self.layout.addWidget(self.social_media_widget)
        self.layout.addWidget(self.selectors_widget)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        """Resizes the menu bar and delegates to sub-widgets."""
        # For example, we can do spacing or style updates here

        # Optionally, call something on the sub-widgets
        self.social_media_widget.resize_social_media_buttons()
        self.selectors_widget.style_selectors()
