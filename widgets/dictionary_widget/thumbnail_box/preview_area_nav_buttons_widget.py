from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class PreviewAreaNavButtonsWidget(QWidget):
    def __init__(self, preview_area: "DictionaryPreviewArea"):
        super().__init__(preview_area)
        self.preview_area = preview_area
        self.current_index = preview_area.current_index
        self._setup_buttons()
        self.enable_buttons(False)

    def _setup_buttons(self):
        self.layout = QHBoxLayout(self)
        self.buttons = []
        button_texts = ["<", ">"]
        for text in button_texts:
            button = PreviewAreaNavButton(text, self)
            self.layout.addWidget(button)
            self.buttons.append(button)
        self.setLayout(self.layout)

    def handle_button_click(self):
        if not self.preview_area.thumbnails:
            return
        sender = self.sender()
        if sender.text() == "<":
            self.current_index = (self.preview_area.current_index - 1) % len(
                self.preview_area.thumbnails
            )
        elif sender.text() == ">":
            self.current_index = (self.preview_area.current_index + 1) % len(
                self.preview_area.thumbnails
            )

        self.preview_area.update_preview(self.current_index)
        box_nav_buttons_widget = (
            self.preview_area.current_thumbnail_box.nav_buttons_widget
        )
        box_nav_buttons_widget.current_index = self.current_index
        box_nav_buttons_widget.update_thumbnail()

    def enable_buttons(self, enable):
        for button in self.buttons:
            button.setEnabled(enable)


class PreviewAreaNavButton(QPushButton):
    def __init__(self, text: str, parent: PreviewAreaNavButtonsWidget):
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
