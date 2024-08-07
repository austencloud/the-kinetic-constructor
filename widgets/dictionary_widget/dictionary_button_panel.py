from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QMessageBox,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
import shutil  # Import shutil for directory removal
import os  # Import os for file operations
from widgets.dictionary_widget.temp_beat_frame import TempBeatFrame
from widgets.path_helpers.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea


class DictionaryButtonPanel(QWidget):
    delete_variation_button: QPushButton
    delete_word_button: QPushButton
    edit_sequence_button: QPushButton
    save_image_button: QPushButton

    def __init__(self, preview_area: "DictionaryPreviewArea"):
        super().__init__(preview_area)
        self.preview_area = preview_area
        self.dictionary_widget = preview_area.dictionary_widget

        self._setup_buttons()

    def _setup_buttons(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)

        # Define button data
        buttons_data = {
            "edit_sequence": {
                "icon": "edit.svg",
                "tooltip": "Edit Sequence",
                "action": self.edit_sequence,
            },
            "save_image": {
                "icon": "save_image.svg",
                "tooltip": "Save Image",
                "action": self.save_image,
            },
            "delete_variation": {
                "icon": "delete.svg",
                "tooltip": "Delete Variation",
                "action": self.delete_variation,
            },
            "delete_word": {
                "icon": "delete.svg",
                "tooltip": "Delete Word",
                "action": self.delete_word,
            },
        }

        # Create buttons based on the data defined
        for key, data in buttons_data.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_widget_icons/{data['icon']}"
            )
            button = QPushButton(QIcon(icon_path), "", self, toolTip=data["tooltip"])
            button.setToolTip(data["tooltip"])
            button.clicked.connect(data["action"])
            self.layout.addWidget(button)
            setattr(self, f"{key}_button", button)
            # set minimum size to be 1/10 of the dictionary widget width

            btn_size = int(self.dictionary_widget.width() // 10)
            icon_size = int(btn_size * 0.8)
            button.setMinimumSize(QSize(btn_size, btn_size))
            button.setMaximumSize(QSize(btn_size, btn_size))
            button.setIconSize(QSize(icon_size, icon_size))

    def edit_sequence(self):
        if not hasattr(self, "sequence_populator"):
            self.sequence_populator = self.dictionary_widget.sequence_populator
        if self.preview_area.sequence_json:
            self.preview_area.main_widget.setCurrentIndex(
                self.preview_area.main_widget.builder_tab_index
            )
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.sequence_populator.load_sequence_from_json(
                self.preview_area.sequence_json
            )
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def save_image(self):
        # Extract metadata from the current preview image
        current_thumbnail = self.preview_area.get_thumbnail_at_current_index()
        if not current_thumbnail:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )
            return

        metadata = self.preview_area.sequence_json
        if not metadata:
            QMessageBox.warning(
                self, "No Metadata", "No metadata found for the selected sequence."
            )
            return

        # Get the invisible beat frame and populate it with metadata
        self.beat_frame = TempBeatFrame(self.dictionary_widget)
        self.beat_frame.populate_beat_frame_from_json(metadata["sequence"])

        # Use the export manager associated with the beat frame to show the export dialog
        self.export_manager = self.beat_frame.export_manager
        self.export_manager.dialog_executor.exec_dialog(metadata["sequence"])

    def delete_variation(self):
        current_thumbnail = self.preview_area.get_thumbnail_at_current_index()
        if not current_thumbnail:
            QMessageBox.warning(
                self, "No Selection", "Please select a variation first."
            )
            return

        reply = QMessageBox.question(
            self,
            "Delete Variation",
            "Are you sure you want to delete this variation?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(current_thumbnail)  # Remove the image file
                self.preview_area.thumbnails.remove(current_thumbnail)
                self.preview_area.update_thumbnails(self.preview_area.thumbnails)
                QMessageBox.information(
                    self, "Deleted", "Variation deleted successfully."
                )
                #refresh the browser
                self.preview_area.dictionary_widget.browser.sorter.sort_and_display_thumbnails()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete variation: {e}")

    def delete_word(self):
        base_word = self.preview_area.base_word
        if not base_word:
            QMessageBox.warning(self, "No Selection", "Please select a word first.")
            return

        reply = QMessageBox.question(
            self,
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
                shutil.rmtree(base_path)  # Remove the entire word directory
                self.preview_area.update_thumbnails([])
                QMessageBox.information(
                    self, "Deleted", f"Word '{base_word}' deleted successfully."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete word: {e}")
