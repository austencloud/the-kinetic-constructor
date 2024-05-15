from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.image_export_dialog.export_control_panel import ExportDialogControlPanel
from widgets.image_export_dialog.export_dialog_preview import ExportDialogPreviewPanel

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportDialog(QDialog):
    def __init__(self, export_manager: "SequenceImageExportManager"):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.main_widget = export_manager.main_widget
        self.setWindowTitle("Export Image Options")
        self.setModal(True)
        self._resize_the_dialog()
        self._setup_preview_panel()
        self._setup_control_panel(export_manager)
        self._setup_layout()
        self.update_preview_based_on_options()

    def _resize_the_dialog(self):
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(main_width // 2, main_height // 2)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addLayout(self.preview_layout, 1)
        self.layout.addWidget(self.control_panel, 1)

    def _setup_control_panel(self, export_manager: "SequenceImageExportManager"):
        self.control_panel = ExportDialogControlPanel(self)
        self.control_panel.optionChanged.connect(self.update_preview_based_on_options)
        self.control_panel.include_start_pos_check.setChecked(
            export_manager.include_start_pos
        )
        self.control_panel.include_start_pos_check.toggled.connect(
            self.update_export_setting_and_layout
        )

    def _setup_preview_panel(self):
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.preview_panel_label = QLabel(self)
        self.preview_panel_label.setText("Preview:")
        self.preview_panel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_panel_label.setStyleSheet("font-size: 20px")
        self.preview_layout = QVBoxLayout()
        self.preview_layout.addWidget(self.preview_panel_label)
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
        self.preview_panel.update_preview_with_start_pos(include_start_pos)

    def update_preview_based_on_options(self):
        include_start_pos = self.control_panel.include_start_pos_check.isChecked()
        self.preview_panel.update_preview_with_start_pos(include_start_pos)

    def get_export_options(self):
        return {
            "include_start_pos": self.control_panel.include_start_pos_check.isChecked(),
            "user_name": self.control_panel.add_name_field.text(),
            "export_date": self.control_panel.add_date_field.text(),
        }

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.preview_panel.update_preview()
