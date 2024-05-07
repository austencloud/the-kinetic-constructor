from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class VariationNumberLabel(QLabel):
    def __init__(self, parent: Union["ThumbnailBox", "DictionaryPreviewArea"]):
        super().__init__(parent)
        if len(parent.thumbnails) > 1:
            self.setText(f"Variation {parent.current_index + 1}")
        else:
            self.hide()
        self.parent: Union["ThumbnailBox", "DictionaryPreviewArea"] = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial", 14, QFont.Weight.Bold))

    def update_index(self, index):
        if len(self.parent.thumbnails) > 1:
            self.setText(f"Variation {index + 1}")
        else:
            self.hide()
