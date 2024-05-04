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
        self.preview_image = preview_image

        # Calculate initial size based on main widget
        main_width = main_widget.width()
        main_height = main_widget.height()
        self.resize(
            main_width // 2, main_height // 2
        )  # Set initial size to 50% of main widget

        # Layout setup
        self.layout: QHBoxLayout = QHBoxLayout(self)
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
        # Call the parent method to handle standard operations
        super().resizeEvent(event)
        # Update child components to adjust to the new size
        self.preview_panel.update_preview(self.width(), self.height())
        # self.button_panel.adjust_size(self.width(), self.height())
