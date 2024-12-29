from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabGoBackButton(QPushButton):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__("Back", cursor=Qt.CursorShape.PointingHandCursor)
        self.browse_tab = browse_tab

        self.hide()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.connect_button(
            lambda: self.browse_tab.layout_manager.switch_to_initial_filter_selection()
        )

    def connect_button(self, callback):
        """Connects the button's clicked signal to the provided callback."""
        self.clicked.connect(callback)

    def resizeEvent(self, event):
        """Repositions the button to the top left corner of the widget."""
        self.setFixedHeight(self.browse_tab.main_widget.height() // 40)
        self.setFixedWidth(self.browse_tab.main_widget.width() // 40)
        font = self.font()
        font.setPointSize(self.browse_tab.main_widget.width() // 100)
        self.setFont(font)
        super().resizeEvent(event)
