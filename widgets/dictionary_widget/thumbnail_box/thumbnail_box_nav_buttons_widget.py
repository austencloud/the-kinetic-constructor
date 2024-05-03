from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class ThumbnailBoxNavButtonsWidget(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.thumbnails = thumbnail_box.thumbnails
        self.current_index = thumbnail_box.current_index
        self.thumbnail_label = thumbnail_box.image_label
        self.variation_number_label = thumbnail_box.variation_number_label
        self._setup_layout()
        self._setup_buttons()

    def _setup_buttons(self):
        button_texts = ["<", ">"]
        for text in button_texts:
            button = NavButton(text, self)
            self.layout.addWidget(button)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self.layout)

    def handle_button_click(self):
        sender = self.sender()
        if sender.text() == "<":
            self.current_index = (self.current_index - 1) % len(self.thumbnails)
        elif sender.text() == ">":
            self.current_index = (self.current_index + 1) % len(self.thumbnails)

        self.update_thumbnail()

        if (
            self.thumbnail_box.image_label
            == self.thumbnail_box.browser.dictionary_widget.selection_handler.currently_selected_thumbnail
        ):
            preview_area = self.thumbnail_box.browser.dictionary_widget.preview_area
            preview_area.variation_number_label.setText(
                f"Variation {self.current_index + 1}"
            )
            preview_area.current_index = self.current_index
            preview_area.update_preview(
                self.current_index
            )

    def update_thumbnail(self):
        self.thumbnail_label.current_index = self.current_index
        self.thumbnail_label.update_thumbnail()
        self.variation_number_label.setText(f"Variation {self.current_index + 1}")


class NavButton(QPushButton):
    def __init__(self, text: str, parent: ThumbnailBoxNavButtonsWidget):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))

    # add a mouse hover event to change the background color of the button and set cursor to pointing hand
    def enterEvent(self, event):
        self.setStyleSheet("background-color: lightgray;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # add a mouse leave event to change the background color of the button back to white

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: white;")
        self.setCursor(Qt.CursorShape.ArrowCursor)
