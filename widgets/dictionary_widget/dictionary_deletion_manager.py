import os
import shutil
from typing import TYPE_CHECKING
from path_helpers import get_images_and_data_path
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryDeletionManager:
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        self.dictionary_widget = dictionary_widget

    def delete_variation(self, thumbnail_box: "ThumbnailBox", index):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        file_path = thumbnail_box.thumbnails.pop(index)
        os.remove(file_path)
        if len(thumbnail_box.thumbnails) == 0:
            self.delete_word(thumbnail_box.base_word)
            self.dictionary_widget.preview_area.reset_preview_area()
            self.dictionary_widget.browser.scroll_widget.thumbnail_boxes_dict.pop(
                thumbnail_box.base_word
            )
        else:
            # update the thumbnail box.thumbnails to reflect the current state after deleting the file
            thumbnail_box.current_index = 0
                        
            self.dictionary_widget.browser.scroll_widget.sort_and_display_thumbnails()
            self.dictionary_widget.preview_area.reset_preview_area()
        QApplication.restoreOverrideCursor()

    def delete_word(self, base_word):
        base_path = os.path.join(get_images_and_data_path("dictionary"), base_word)
        shutil.rmtree(base_path)
        self.dictionary_widget.browser.scroll_widget.sort_and_display_thumbnails()

    def confirm_delete_word(self):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete all variations of {self.dictionary_widget.preview_area.base_word}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_word(self.dictionary_widget.preview_area.base_word)

    def confirm_delete_variation(self):
        preview_area = self.dictionary_widget.preview_area
        if not preview_area.current_thumbnail_box:
            QMessageBox.warning(
                preview_area, "No Selection", "Please select a variation first."
            )
            return
        reply = QMessageBox.question(
            preview_area,
            "Confirm Deletion",
            f"Are you sure you want to delete this variation of {preview_area.base_word}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_variation(
                preview_area.current_thumbnail_box,
                preview_area.current_index,
            )
