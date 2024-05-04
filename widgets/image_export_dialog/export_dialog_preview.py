from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogPreviewPanel(QFrame):
    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__(export_dialog)
        self.export_dialog = export_dialog
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Ensure alignment is centered
        self.preview_label.setScaledContents(True)
        self.json_handler = (
            export_dialog.main_widget.json_manager.current_sequence_json_handler
        )

        # Calculate and fix the size based on initial dialog dimensions
        dialog_width = export_dialog.width() // 2
        dialog_height = export_dialog.height()  # or some other proportion
        self.setFixedSize(dialog_width, dialog_height)

    def update_preview_with_start_pos(self, include_start_pos: bool):
        json_sequence = self.json_handler.load_current_sequence_json()
        sequence_image = self.export_dialog.export_manager.create_sequence_image(
            json_sequence, include_start_pos
        )
        self.preview_image = QPixmap.fromImage(sequence_image)
        self.update_preview()

    def update_preview(self):
        if self.preview_image:
            image_aspect_ratio = (
                self.preview_image.width() / self.preview_image.height()
            )
            image_width = self.width()
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
            # Center the label to ensure the pixmap is centered within the available space
            label_x = (self.width() - image_width) // 2
            label_y = (self.height() - image_height) // 2
            self.preview_label.setGeometry(label_x, label_y, image_width, image_height)
