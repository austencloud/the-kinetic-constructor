from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

class VariationNumberLabel(QLabel):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(f"Variation {thumbnail_box.current_index + 1}")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial", 14, QFont.Weight.Bold))
