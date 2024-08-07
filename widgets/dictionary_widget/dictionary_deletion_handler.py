import os
import shutil
import time
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea


class DictionaryDeletionHandler:
    def __init__(self, preview_area: "DictionaryPreviewArea"):
        self.dictionary_widget = preview_area.dictionary_widget
        self.preview_area = preview_area

    def delete_variation(self, current_thumbnail):
        if not current_thumbnail:
            QMessageBox.warning(
                self.preview_area, "No Selection", "Please select a variation first."
            )
            return

        reply = QMessageBox.question(
            self.preview_area,
            "Delete Variation",
            "Are you sure you want to delete this variation?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Ensure the file is writable
                os.chmod(current_thumbnail, 0o777)
                os.remove(current_thumbnail)  # Remove the image file
                self.preview_area.thumbnails.remove(current_thumbnail)
                self.preview_area.update_thumbnails(self.preview_area.thumbnails)
                QMessageBox.information(
                    self.preview_area, "Deleted", "Variation deleted successfully."
                )
                self.preview_area.dictionary_widget.browser.sorter.sort_and_display_thumbnails()
            except Exception as e:
                QMessageBox.critical(
                    self.preview_area, "Error", f"Could not delete variation: {e}"
                )

    def delete_word(self, base_word):
        if not base_word:
            QMessageBox.warning(
                self.preview_area, "No Selection", "Please select a word first."
            )
            return

        reply = QMessageBox.question(
            self.preview_area,
            "Delete Word",
            f"Are you sure you want to delete all variations of '{base_word}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            base_path = os.path.join(
                self.dictionary_widget.main_widget.top_builder_widget.sequence_widget.add_to_dictionary_manager.dictionary_dir,
                base_word,
            )
            try:
                self.ensure_writable(base_path)
                self.refresh_ui()  # Attempt to refresh the UI to release any locks
                self.retry_delete(base_path)
                self.preview_area.update_thumbnails([])
                QMessageBox.information(
                    self.preview_area,
                    "Deleted",
                    f"Word '{base_word}' deleted successfully.",
                )
            except PermissionError as e:
                QMessageBox.critical(
                    self.preview_area,
                    "Permission Error",
                    f"Could not delete word: {e}\nEnsure you have the necessary permissions.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self.preview_area, "Error", f"Could not delete word: {e}"
                )

    def ensure_writable(self, path):
        """
        Ensure all files and directories in the given path are writable.
        """
        for root, dirs, files in os.walk(path):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    print(f"Setting writable permission for file: {file_path}")
                    os.chmod(file_path, 0o777)  # Ensure file is writable
                except Exception as e:
                    print(f"Failed to set writable permission for file: {file_path}. Error: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    print(f"Setting writable permission for directory: {dir_path}")
                    os.chmod(dir_path, 0o777)  # Ensure directory is writable
                except Exception as e:
                    print(f"Failed to set writable permission for directory: {dir_path}. Error: {e}")

    def refresh_ui(self):
        """
        Refresh the UI to ensure that no files or directories are being used.
        """
        self.preview_area.update_thumbnails([])

    def retry_delete(self, path, retries=5, delay=1):
        """
        Attempt to delete the directory with a retry mechanism.
        """
        for i in range(retries):
            try:
                shutil.rmtree(path)
                print(f"Successfully deleted {path} on attempt {i + 1}")
                break
            except PermissionError:
                print(f"Attempt {i + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            raise PermissionError(f"Could not delete {path} after {retries} attempts.")
