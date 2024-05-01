from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from widgets.dictionary_widget.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionarySelectionHandler:
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        self.dictionary_widget = dictionary_widget
        self.currently_selected_thumbnail: ThumbnailImageLabel = None

    def update_selection(self, thumbnail_box) -> None:
        if self.currently_selected_thumbnail:
            self.currently_selected_thumbnail.set_selected(False)
        self.currently_selected_thumbnail: ThumbnailImageLabel = thumbnail_box
        self.currently_selected_thumbnail.set_selected(True)
        self.currently_selected_thumbnail.is_selected = True

    def thumbnail_clicked(
        self, thumbnail_box, thumbnail_pixmap: "QPixmap", metadata
    ) -> None:
        self.dictionary_widget.selected_sequence_dict = metadata
        self.dictionary_widget.preview_area.preview_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.dictionary_widget.preview_area.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.update_selection(thumbnail_box)
