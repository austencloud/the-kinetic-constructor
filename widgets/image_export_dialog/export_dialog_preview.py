from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogPreviewPanel(QFrame):
    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__(export_dialog)
        self.export_dialog = export_dialog
        self.json_handler = (
            self.export_dialog.main_widget.json_manager.current_sequence_json_handler
        )
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.preview_label = QLabel(self)
        self.preview_label.setScaledContents(True)
        # self.update_preview(export_dialog.width(), export_dialog.height())

    def update_preview(self, parent_width, parent_height):
        dialog_width = parent_width // 2
        dialog_height = int(parent_height * 0.75)

        if self.preview_image.height() == 0:
            return  # Prevent division by zero

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
        pixmap = QPixmap.fromImage(scaled_image)
        self.preview_label.setPixmap(pixmap)

        self.preview_label.setFixedSize(image_width, image_height)
        self.setFixedSize(image_width, image_height)

    def update_preview_with_start_pos(self, include_start_pos: bool):
        # Re-draw image based on include_start_pos
        # You'll need to call something similar to _draw_beats here, but ensure it operates on a preview scale
        print("Updating preview to include start position:", include_start_pos)
        # Example to trigger redrawing, you'll need to adjust actual drawing logic
        sequence = self.json_handler.load_current_sequence_json()
        self.preview_image = self.export_dialog.export_manager.create_beat_frame_image(
            sequence, include_start_pos
        )
        self.update_preview(self.export_dialog.width(), self.export_dialog.height())
