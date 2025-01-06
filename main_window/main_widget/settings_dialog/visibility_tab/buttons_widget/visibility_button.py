from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(QPushButton):
    def __init__(
        self, name: str, visibility_checkbox_widget: "VisibilityButtonsWidget"
    ):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_checkbox_widget = visibility_checkbox_widget
        self.toggler = self.visibility_checkbox_widget.toggler
        self.name = name

        # Custom properties for hover and toggle states
        self.is_hovered = False
        self.is_toggled = False
        self._connect_signals()

        # Initial styles
        self._apply_styles()

    def _connect_signals(self):
        # Connect toggler to interact with visibility settings
        self.clicked.connect(self._toggle_state)

    def _toggle_state(self):
        """Handle button toggle state."""
        self.is_toggled = not self.is_toggled
        self._apply_styles()

        # Trigger visibility toggler
        if self.name in self.visibility_checkbox_widget.glyph_names:
            self.toggler.toggle_glyph_visibility(self.name, self.is_toggled)
        else:
            self.toggler.toggle_non_radial_points(self.is_toggled)

    def _apply_styles(self):
        """Apply styles based on hover and toggle states."""
        style = ""
        if self.is_toggled:
            style = (
                "background-color: #4CAF50; color: white; "
                "border: 2px solid #388E3C; border-radius: 5px;"
            )
        elif self.is_hovered:
            style = (
                "background-color: #E0E0E0; color: black; "
                "border: 2px solid #9E9E9E; border-radius: 5px;"
            )
        else:
            style = (
                "background-color: #F5F5F5; color: black; "
                "border: 1px solid #9E9E9E; border-radius: 5px;"
            )

        if self.styleSheet() != style:
            self.setStyleSheet(style)
        QApplication.processEvents()

    def enterEvent(self, event):
        """Mouse enters the button area."""
        self.is_hovered = True
        self._apply_styles()

    def leaveEvent(self, event):
        """Mouse leaves the button area."""
        self.is_hovered = False
        self._apply_styles()

    def sizeHint(self) -> QSize:
        """Provide a consistent size hint for all buttons."""
        return QSize(150, 40)
