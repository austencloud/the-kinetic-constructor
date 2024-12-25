from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.thumbnail_box.thumbnail_box import ThumbnailBox
    from main_window.main_widget.browse_tab.dictionary_preview_area import DictionaryPreviewArea




class VariationNumberLabel(QLabel):
    def __init__(self, parent: Union["ThumbnailBox", "DictionaryPreviewArea"]):
        super().__init__(parent)
        if len(parent.thumbnails) > 1:
            self.setText(f"{parent.current_index + 1}/{len(parent.thumbnails)}")
        else:
            self.hide()
        self.parent: Union["ThumbnailBox", "DictionaryPreviewArea"] = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_index(self, index):
        if len(self.parent.thumbnails) > 1:
            self.setText(f"{index + 1}/{len(self.parent.thumbnails)}")
        else:
            self.hide()

    def clear(self) -> None:
        self.setText("")

    def resize_variation_number_label(self):
        font = self.font()
        font.setPointSize(self.parent.dictionary_widget.main_widget.width() // 100)
        font.setBold(True)
        self.setFont(font)
