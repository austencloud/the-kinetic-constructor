from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogPreviewPanel(QFrame):
    def __init__(self, export_dialog: "ImageExportDialog", image=None):
        super().__init__(export_dialog)
        self.image = image
        self.export_dialog = export_dialog
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setScaledContents(False)  # Disable scaled contents

        self.json_handler = (
            export_dialog.main_widget.json_manager.current_sequence_json_handler
        )

        dialog_width = export_dialog.width()
        dialog_height = export_dialog.height()  # or some other proportion
        self.setMaximumSize(dialog_width, dialog_height)
        self.preview_panel_label = QLabel(self)
        self.preview_panel_label.setText("Preview:")
        self.preview_panel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_panel_label.setStyleSheet("font-size: 20px")
        self.layout.addWidget(self.preview_panel_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.preview_label)
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview_with_start_pos(
        self, include_start_pos: bool, sequence: list[dict]
    ):
        options = {
            "user_name": self.export_dialog.control_panel.user_combo_box.currentText(),
            "export_date": self.export_dialog.control_panel.add_date_field.text(),
        }
        self.image = self.export_dialog.export_manager.create_sequence_image(
            sequence, include_start_pos, options
        )
        self.preview_image = QPixmap.fromImage(self.image)
        self.update_preview()

    def update_preview(self):
        if self.preview_image:
            image_aspect_ratio = (
                self.preview_image.width() / self.preview_image.height()
            )
            image_width = int(self.width() * 0.9)
            image_height = int(image_width / image_aspect_ratio)

            if image_height > self.height():
                image_height = self.height()
                image_width = int(image_height * image_aspect_ratio)

            scaled_image = self.preview_image.scaled(
                image_width,
                image_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_image)
            self.preview_label.setFixedSize(scaled_image.size())
