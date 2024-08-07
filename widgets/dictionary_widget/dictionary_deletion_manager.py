import os
import shutil
from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path
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
            self.dictionary_widget.preview_area.update_thumbnails()
            self.dictionary_widget.browser.scroll_widget.thumbnail_boxes_dict.pop(
                thumbnail_box.base_word
            )
        else:
            thumbnail_box.current_index = 0
            self.dictionary_widget.browser.sorter.sort_and_display_thumbnails()
            self.dictionary_widget.preview_area.update_thumbnails(
                thumbnail_box.thumbnails
            )
            thumbnail_box.update_thumbnails(thumbnail_box.thumbnails)
        QApplication.restoreOverrideCursor()

    def delete_word(self, base_word):
        base_path = os.path.join(get_images_and_data_path("dictionary"), base_word)
        for root, dirs, files in os.walk(base_path):
            for name in files:
                file_path = os.path.join(root, name)
                os.chmod(file_path, 0o777)
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.chmod(dir_path, 0o777)
        os.chmod(base_path, 0o777)
        shutil.rmtree(base_path)
        self.dictionary_widget.browser.sorter.sort_and_display_thumbnails()
