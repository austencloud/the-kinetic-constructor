from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_image_label import (
        ThumbnailImageWidget,
    )
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class BrowseTabSelectionHandler:
    def __init__(self, dictionary_widget: "BrowseTab") -> None:
        self.browse_tab = dictionary_widget
        self.currently_selected_thumbnail: ThumbnailImageWidget = None

    def update_selection(self, thumbnail_image_label: "ThumbnailImageWidget") -> None:
        if self.currently_selected_thumbnail:
            self.currently_selected_thumbnail.set_selected(False)
        self.currently_selected_thumbnail: ThumbnailImageWidget = thumbnail_image_label
        self.currently_selected_thumbnail.set_selected(True)
        self.currently_selected_thumbnail.is_selected = True

    def thumbnail_clicked(
        self,
        image_label: "ThumbnailImageWidget",
        thumbnail_pixmap: "QPixmap",
        metadata,
        thumbnail_collection,
        thumbnail_index,
    ) -> None:
        self.browse_tab.sequence_picker.selected_sequence_dict = metadata
        self.sequence_viewer = self.browse_tab.sequence_viewer
        self.sequence_viewer.thumbnails = thumbnail_collection
        self.sequence_viewer.image_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.sequence_viewer.image_label.size() * 0.9,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.update_selection(image_label)
        self.sequence_viewer.select_thumbnail(
            image_label.thumbnail_box,
            thumbnail_index,
            image_label.thumbnail_box.word,
        )
        self.sequence_viewer.variation_number_label.update_index(thumbnail_index)
