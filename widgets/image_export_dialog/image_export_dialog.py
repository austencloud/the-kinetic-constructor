from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.image_export_dialog.export_dialog_control_panel import ExportDialogControlPanel
from widgets.image_export_dialog.export_dialog_preview import ExportDialogPreviewPanel

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportDialog(QDialog):
    def __init__(self, export_manager: "SequenceImageExportManager", sequence: list[dict]):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.sequence = sequence
        self.main_widget = export_manager.main_widget
        self.setWindowTitle("Export Image Options")
        self.setModal(True)
        self._resize_the_dialog()
        self._setup_components()
        self._setup_layout()
        self.update_preview_based_on_options()

    def _resize_the_dialog(self):
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(main_width // 2, main_height // 2)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addLayout(self.preview_layout, 2)
        self.layout.addWidget(self.control_panel, 1)

    def _setup_components(self):
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.control_panel = ExportDialogControlPanel(self)

        self.preview_layout = QVBoxLayout()
        self.preview_layout.addWidget(self.preview_panel)

    def update_export_setting_and_layout(self):
        new_value = self.control_panel.include_start_pos_check.isChecked()
        self.export_manager.include_start_pos = new_value
        self.export_manager.settings_manager.set_image_export_setting(
            "include_start_position", new_value
        )
        self.update_preview_based_on_options()

    def update_preview_based_on_options(self):
        include_start_pos = self.control_panel.include_start_pos_check.isChecked()
        self.preview_panel.update_preview_with_start_pos(include_start_pos, self.sequence)

    def get_export_options(self):
        return {
            "include_start_pos": self.control_panel.include_start_pos_check.isChecked(),
            "user_name": self.control_panel.add_name_field.text(),
            "export_date": self.control_panel.add_date_field.text(),
        }

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.preview_panel.update_preview()
