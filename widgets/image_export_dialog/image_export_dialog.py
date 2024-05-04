from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap

from widgets.image_export_dialog.export_control_panel import ExportDialogControlPanel
from widgets.image_export_dialog.export_dialog_preview import ExportDialogPreview

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap


class ImageExportDialog(QDialog):
    def __init__(self, main_widget: "MainWidget", preview_image: QPixmap):
        super().__init__(main_widget)
        self.setWindowTitle("Export Image Options")
        self.setModal(True)
        self.layout: QHBoxLayout = QHBoxLayout(self)

        # Components
        self.preview_panel = ExportDialogPreview(self, preview_image)
        self.button_panel = ExportDialogControlPanel(self)

        # Add components to layout
        self.layout.addWidget(self.preview_panel, 1)
        self.layout.addWidget(self.button_panel, 1)

    def get_export_options(self):
        return {
            "include_start_pos": self.button_panel.include_start_pos_check.isChecked(),
            "user_name": self.button_panel.add_name_field.text(),
            "export_date": self.button_panel.add_date_field.text(),
        }

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.preview_panel.update_preview(self.width(), self.height())
