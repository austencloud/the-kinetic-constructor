from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import DictionaryBrowser

class SectionHeader(QWidget):
    def __init__(self, title, dictionary_browser: "DictionaryBrowser"):
        super().__init__()
        layout = QVBoxLayout(self)
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        self.setLayout(layout)
        
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

    def resizeEvent(self, event):
        font_size = int(self.width() // 35)
        self.title_label.setStyleSheet(
            f"font-weight: bold; font-size: {font_size}px; color: #333;"
        )
        super().resizeEvent(event)
