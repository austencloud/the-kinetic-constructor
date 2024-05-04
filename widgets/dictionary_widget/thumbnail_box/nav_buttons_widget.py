from typing import TYPE_CHECKING, Union
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal


class NavButtonsWidget(QWidget):

    def __init__(self, parent: Union["ThumbnailBox", "DictionaryPreviewArea"]):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.buttons: list[NavButton] = []
        self.current_index = 0
        self.item_count = 0  # Total number of items to navigate through
        self.parent: Union["ThumbnailBox", "DictionaryPreviewArea"] = parent
        self._setup_buttons()

    def _setup_buttons(self):
        button_texts = ["<", ">"]
        for text in button_texts:
            button = NavButton(text, self)
            button.clicked.connect(self.handle_button_click)
            button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            button.setStyleSheet("background-color: white;")
            self.layout.addWidget(button)
            self.buttons.append(button)

        self.setLayout(self.layout)

    def handle_button_click(self):
        self.item_count = self.parent.thumbnails_count()
        sender = self.sender()
        if sender.text() == "<":
            self.current_index = (self.current_index - 1) % self.item_count
        elif sender.text() == ">":
            self.current_index = (self.current_index + 1) % self.item_count

        self.parent.update_thumbnail(self.current_index)

    def update_item_count(self, count):
        self.item_count = count
        for button in self.buttons:
            button.setEnabled(count > 0)

    def enable_buttons(self, enable):
        for button in self.buttons:
            button.setEnabled(enable)


class NavButton(QPushButton):
    def __init__(self, text: str, parent: NavButtonsWidget):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))

    def enterEvent(self, event):
        self.setStyleSheet("background-color: lightgray;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: white;")
        self.setCursor(Qt.CursorShape.ArrowCursor)
