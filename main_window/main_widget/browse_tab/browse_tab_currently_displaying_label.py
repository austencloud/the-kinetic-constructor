from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabCurrentlyDisplayingLabel(QLabel):
    def __init__(self, browse_tab: "BrowseTab") -> None:
        super().__init__(browse_tab)
        self.browse_tab = browse_tab
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_message(self, description):
        self.setText(f"Currently displaying {description}.")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.browse_tab.main_widget.width() // 65)
        self.setFont(font)
