from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_image_label import (
        ThumbnailImageLabel,
    )
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class BrowseTabSelectionManager:
    def __init__(self, dictionary_widget: "BrowseTab") -> None:
        self.browse_tab = dictionary_widget
        self.sequence_viewer = self.browse_tab.sequence_viewer
        self.current_thumbnail: ThumbnailImageLabel = None

    def thumbnail_clicked(
        self,
        image_label: "ThumbnailImageLabel",
        thumbnail_pixmap: "QPixmap",
        metadata: dict,
        thumbnail_collection: list[str],
        thumbnail_index: int,
    ) -> None:
        self.browse_tab.sequence_picker.selected_sequence_dict = metadata
        self.sequence_viewer.thumbnails = thumbnail_collection
        self.sequence_viewer.image_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.sequence_viewer.image_label.size() * 0.9,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        if self.current_thumbnail:
            self.current_thumbnail.set_selected(False)
        self.current_thumbnail: ThumbnailImageLabel = image_label
        self.current_thumbnail.set_selected(True)
        self.current_thumbnail.is_selected = True
        self.sequence_viewer.select_thumbnail(
            image_label.thumbnail_box,
            thumbnail_index,
            image_label.thumbnail_box.word,
        )
        self.sequence_viewer.variation_number_label.update_index(thumbnail_index)
