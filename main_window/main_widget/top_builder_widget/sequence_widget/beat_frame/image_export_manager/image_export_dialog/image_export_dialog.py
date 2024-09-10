import os
import re
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
from .export_dialog_control_panel import ExportDialogControlPanel
from .export_dialog_preview_panel import ExportDialogPreviewPanel
from sequence_sharer import SequenceSharerDialog  # Import the SequenceSharerDialog

if TYPE_CHECKING:
    from ..image_export_manager import ImageExportManager


def sanitize_filename(filename):
    """Sanitize the filename by replacing invalid characters."""
    sanitized = re.sub(r"[^\w\-_.]", "_", filename)  # Replace invalid characters
    return sanitized


class ImageExportDialog(QDialog):
    def __init__(self, export_manager: "ImageExportManager", sequence: list[dict]):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.sequence = sequence
        self.main_widget = export_manager.main_widget
        self.settings_manager = export_manager.settings_manager
        self.setWindowTitle("Save Image")
        self.setModal(True)
        self._resize_image_export_dialog()
        self._setup_components()
        self._setup_layout()
        self.update_preview_based_on_options()

    def _setup_okay_cancel_buttons(self):
        self.ok_button = QPushButton("Save", self)
        self.ok_button.clicked.connect(self.control_panel.save_settings_and_accept)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.control_panel.export_dialog.reject)

        # Add a "Share" button
        self.share_button = QPushButton("Share", self)
        self.share_button.clicked.connect(self.open_sharer_dialog)  # Open share dialog

    def open_sharer_dialog(self):
        """Open the SequenceSharerDialog to send the current preview image via email."""
        word = self.sequence[0]["word"]
        preview_image_path = f"{word}.png"  # Temporary file for the preview image
        pixmap = self.preview_panel.preview_image
        sanitized_word = sanitize_filename(word)

        # Construct a full file path and ensure it's in a valid directory
        temp_image_path = os.path.join(os.getcwd(), f"{sanitized_word}.png")

        if not pixmap.save(temp_image_path):
            QMessageBox.critical(self, "Save Error", "Failed to save the preview image.")
            return

        # Ensure the file exists and isn't empty before continuing
        if not os.path.isfile(temp_image_path) or os.path.getsize(temp_image_path) == 0:
            QMessageBox.critical(self, "File Error", "File is invalid or empty.")
            return

        # Open the SequenceSharer dialog
        sharer_dialog = SequenceSharerDialog(self.main_widget, preview_image_path)
        sharer_dialog.exec()

        # Clean up the temporary image file after sending
        if os.path.exists(preview_image_path):
            os.remove(preview_image_path)

    def _resize_image_export_dialog(self):
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(main_width // 3, int(main_height // 1.5))

    def _setup_components(self):
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.control_panel = ExportDialogControlPanel(self)
        self._setup_okay_cancel_buttons()

    def _setup_layout(self):
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(
            self.share_button
        )  # Add the "Share" button to layout

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.preview_panel, 12)
        self.layout.addWidget(self.control_panel, 1)
        self.layout.addLayout(self.button_layout, 1)

    def update_export_setting_and_layout(self):
        new_value = self.control_panel.include_start_pos_check.isChecked()
        self.export_manager.include_start_pos = new_value
        self.export_manager.settings_manager.image_export.set_image_export_setting(
            "include_start_position", new_value
        )
        self.update_preview_based_on_options()

    def get_export_options(self):
        return {
            "include_start_position": self.control_panel.include_start_pos_check.isChecked(),
            "add_info": self.control_panel.add_info_check.isChecked(),
            "add_word": self.control_panel.add_word_check.isChecked(),
            "user_name": self.control_panel.user_combo_box.currentText(),
            "export_date": self.control_panel.add_date_field.text(),
            "open_directory": self.control_panel.open_directory_check.isChecked(),
            "notes": self.control_panel.notes_combo_box.currentText(),
            "add_difficulty_level": self.control_panel.include_difficulty_level_check.isChecked(),
            "add_beat_numbers": self.control_panel.add_beat_numbers_check.isChecked(),
        }

    def update_preview_based_on_options(self):
        include_start_pos = self.control_panel.include_start_pos_check.isChecked()
        options = self.get_export_options()
        self.preview_panel.update_preview_with_options(
            include_start_pos, self.sequence, options
        )

    def showEvent(self, event):
        super().showEvent(event)
        self.preview_panel.update_preview()
