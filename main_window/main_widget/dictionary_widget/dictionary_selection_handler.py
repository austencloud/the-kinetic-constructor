from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionarySelectionHandler:
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        self.dictionary_widget = dictionary_widget
        self.currently_selected_thumbnail: ThumbnailImageLabel = None

    def update_selection(self, thumbnail_image_label: "ThumbnailImageLabel") -> None:
        if self.currently_selected_thumbnail:
            self.currently_selected_thumbnail.set_selected(False)
        self.currently_selected_thumbnail: ThumbnailImageLabel = thumbnail_image_label
        self.currently_selected_thumbnail.set_selected(True)
        self.currently_selected_thumbnail.is_selected = True

    def thumbnail_clicked(
        self,
        image_label: "ThumbnailImageLabel",
        thumbnail_pixmap: "QPixmap",
        metadata,
        thumbnail_collection,
        thumbnail_index,
    ) -> None:
        self.dictionary_widget.selected_sequence_dict = metadata
        self.preview_area = self.dictionary_widget.preview_area
        self.preview_area.thumbnails = thumbnail_collection
        self.preview_area.image_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.preview_area.image_label.size() * 0.9,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.update_selection(image_label)
        self.preview_area.select_thumbnail(
            image_label.thumbnail_box,
            thumbnail_index,
            image_label.thumbnail_box.word,
        )
        self.preview_area.variation_number_label.update_index(thumbnail_index)
