import os
import shutil
from typing import TYPE_CHECKING

from main_window.main_widget.browse_tab.delete_confirmation_dialog import DeleteConfirmationDialog
from main_window.main_widget.browse_tab.dictionary_browser.thumbnail_box.thumbnail_box import ThumbnailBox
from main_window.main_widget.browse_tab.variation_number_fixer import VariationNumberFixer
from utilities.path_helpers import get_images_and_data_path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog

if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class DictionaryDeletionHandler:
    def __init__(self, dictionary_widget: "BrowseTab"):
        self.dictionary_widget = dictionary_widget
        self.variation_number_fixer = VariationNumberFixer()

    def is_folder_empty(self, folder_path):
        return not any(os.scandir(folder_path))

    def delete_variation(self, thumbnail_box: "ThumbnailBox", index):
        dialog = DeleteConfirmationDialog(self.dictionary_widget)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            current_scroll_position = (
                self.dictionary_widget.browser.scroll_widget.scroll_area.verticalScrollBar().value()
            )
            file_path = thumbnail_box.thumbnails.pop(index)
            os.remove(file_path)
            if len(thumbnail_box.thumbnails) == 0:
                self.delete_word(thumbnail_box.word)
                self.dictionary_widget.preview_area.update_thumbnails()
                self.dictionary_widget.browser.scroll_widget.thumbnail_boxes.pop(
                    thumbnail_box.word
                )
            else:
                self.delete_empty_folders(get_images_and_data_path("dictionary"))
                thumbnail_box.current_index = 0
                self.dictionary_widget.browser.thumbnail_box_sorter.reload_currently_displayed_filtered_sequences()
                thumbnail_box.image_label.update_thumbnail(thumbnail_box.current_index)
                self.dictionary_widget.preview_area.update_thumbnails(
                    thumbnail_box.thumbnails
                )
                thumbnail_box.update_thumbnails(thumbnail_box.thumbnails)

            def restore_scroll_position():
                self.dictionary_widget.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(
                    current_scroll_position
                )
                QApplication.restoreOverrideCursor()

            QApplication.processEvents()
            QTimer.singleShot(0, restore_scroll_position)

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
        self.delete_empty_folders(get_images_and_data_path("dictionary"))
        self.variation_number_fixer.ensure_sequential_versions()
        self.dictionary_widget.browser.thumbnail_box_sorter.reload_currently_displayed_filtered_sequences()

    def delete_empty_folders(self, root_folder):
        for root, dirs, files in os.walk(root_folder, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if self.is_folder_empty(dir_path):
                    os.chmod(dir_path, 0o777)
                    shutil.rmtree(dir_path)
