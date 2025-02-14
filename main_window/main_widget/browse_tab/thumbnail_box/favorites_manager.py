from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import (
        ThumbnailBox,
    )


class FavoritesManager:
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        self.thumbnail_box = thumbnail_box
        self.favorite_status = False  # Default favorite status
        self.load_favorite_status()

    def is_favorite(self) -> bool:
        return self.favorite_status

    def toggle_favorite_status(self):
        self.favorite_status = not self.favorite_status
        self.thumbnail_box.word_label.update_favorite_icon(self.favorite_status)
        QApplication.processEvents()
        self.save_favorite_status()

    def load_favorite_status(self):
        if self.thumbnail_box.state.thumbnails:
            first_thumbnail = self.thumbnail_box.state.thumbnails[0]
            self.favorite_status = (
                self.thumbnail_box.main_widget.metadata_extractor.get_favorite_status(
                    first_thumbnail
                )
            )

    def save_favorite_status(self):
        for thumbnail in self.thumbnail_box.state.thumbnails:
            self.thumbnail_box.main_widget.metadata_extractor.set_favorite_status(
                thumbnail, self.favorite_status
            )
