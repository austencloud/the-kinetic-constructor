from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class BaseWordLabel(QLabel):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.setText(thumbnail_box.base_word)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resize_base_word_label(self):
        font_size = self.thumbnail_box.width() // 20
        self.setFont(QFont("Georgia", font_size, QFont.Weight.DemiBold))
