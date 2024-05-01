from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class NavigationButtonsWidget(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.thumbnails = thumbnail_box.thumbnails
        self.current_index = thumbnail_box.current_index
        self.thumbnail_label = thumbnail_box.thumbnail_image_label
        self.variation_number_label = thumbnail_box.variation_number_label
        self._setup_layout()
        self._setup_buttons()


    def _setup_buttons(self):
        button_texts = ["<", ">"]
        for text in button_texts:
            button = QPushButton(text)
            button.clicked.connect(self.handle_button_click)
            button.setStyleSheet("background-color: white;")
            button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
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

        self.thumbnail_label.current_index = self.current_index
        self.thumbnail_label.update_thumbnail()
        self.variation_number_label.setText(f"Variation {self.current_index + 1}")
        self.thumbnail_box.browser.dictionary_widget.preview_area.update_preview(
            self.thumbnails[self.current_index]
        )
