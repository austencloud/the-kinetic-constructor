from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog




from PyQt6.QtGui import QPixmap


class ExportDialogPreview(QFrame):
    def __init__(self, export_dialog: "ImageExportDialog", preview_image: QPixmap):
        super().__init__(export_dialog)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.export_dialog = export_dialog
        self.preview_label = QLabel(self)
        self.preview_label.setScaledContents(True)
        self.preview_image = preview_image
        self.update_preview(self.export_dialog.width(), self.export_dialog.height())

    def update_preview(self, parent_width, parent_height):
        dialog_width = parent_width // 2
        dialog_height = int(parent_height * 0.75)
        image_aspect_ratio = self.preview_image.width() / self.preview_image.height()
        image_width = dialog_width
        image_height = int(image_width / image_aspect_ratio)

        if image_height > dialog_height:
            image_height = dialog_height
            image_width = int(image_height * image_aspect_ratio)

        scaled_image = self.preview_image.scaled(
            image_width,
            image_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setPixmap(scaled_image)
        self.preview_label.setFixedSize(image_width, image_height)
        self.setFixedSize(image_width, image_height)
