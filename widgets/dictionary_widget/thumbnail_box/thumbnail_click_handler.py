from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt



if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class ThumbnailClickHandler:
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        self.dictionary_widget = dictionary_widget

    def thumbnail_clicked(self, thumbnail_box, thumbnail_pixmap: "QPixmap", metadata):
        self.dictionary_widget.selected_sequence_dict = metadata
        self.dictionary_widget.preview_area.preview_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.dictionary_widget.preview_area.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.dictionary_widget.selection_handler.update_selection(thumbnail_box)
