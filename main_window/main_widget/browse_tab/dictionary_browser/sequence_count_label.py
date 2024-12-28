from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabSequenceCountLabel(QLabel):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__("")
        self.browse_tab = browse_tab
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_count(self, count: int):
        """Update the label with the count of displayed sequences."""
        self.setText(f"Sequences displayed: {count}")

    def resizeEvent(self, event):
        label = self.browse_tab.sequence_count_label
        font = label.font()
        font.setPointSize(self.browse_tab.main_widget.width() // 80)
        label.setFont(font)
