from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QWidget, QApplication
from PyQt6.QtGui import QFont, QIcon
from typing import TYPE_CHECKING
import os

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class WordLabel(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.setContentsMargins(0, 0, 0, 0)

        # Set up the label and favorite button
        self.word_label = QLabel(thumbnail_box.word)
        self.favorite_button = QPushButton()
        self.favorite_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.favorite_button.setFlat(True)  # Remove button border

        # Load icons
        icons_path = get_images_and_data_path("images/icons")
        self.star_icon_empty = QIcon(os.path.join(icons_path, "star_outline.png"))
        self.star_icon_filled = QIcon(os.path.join(icons_path, "star_filled.png"))

        # Connect the button click event
        self.favorite_button.clicked.connect(self.toggle_favorite_status)

        # Layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(1)
        self.layout.addWidget(self.word_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.favorite_button)

        self.setLayout(self.layout)
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resize_base_word_label(self):
        font_size = self.thumbnail_box.width() // 18
        font = QFont("Georgia", font_size, QFont.Weight.DemiBold)
        self.word_label.setFont(font)
        icon_size = QSize(font_size + 10, font_size + 10)
        self.favorite_button.setIconSize(icon_size)

    def update_favorite_icon(self, is_favorite: bool):
        if is_favorite:
            self.favorite_button.setIcon(self.star_icon_filled)
        else:
            self.favorite_button.setIcon(self.star_icon_empty)
        QApplication.processEvents()

    def toggle_favorite_status(self):
        self.thumbnail_box.toggle_favorite_status()
