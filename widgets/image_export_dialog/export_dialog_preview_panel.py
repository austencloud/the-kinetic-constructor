from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout
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

        dialog_width = export_dialog.width()
        dialog_height = export_dialog.height()  # or some other proportion
        self.setMaximumSize(dialog_width, dialog_height)
        self.layout.addWidget(self.preview_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview_with_start_pos(
        self,
        include_start_pos: bool,
        add_info: bool,
        sequence: list[dict],
        add_word: bool,
        include_difficulty_level: bool,
    ):
        options = {
            "include_start_pos": include_start_pos,
            "add_info": add_info,
            "user_name": self.export_dialog.control_panel.user_combo_box.currentText(),
            "export_date": self.export_dialog.control_panel.add_date_field.text(),
            "add_word": add_word,
            "notes": self.export_dialog.control_panel.notes_combo_box.currentText(),
            "add_difficulty_level": include_difficulty_level,
        }
        self.image = (
            self.export_dialog.export_manager.image_creator.create_sequence_image(
                sequence, include_start_pos, options
            )
        )
        self.preview_image = QPixmap.fromImage(self.image)
        self.update_preview()

    def update_preview(self):
        if self.preview_image:
            image_aspect_ratio = (
                self.preview_image.width() / self.preview_image.height()
            )
            image_width = int(self.width() * 0.95)
            image_height = int(image_width / image_aspect_ratio)

            if image_height > self.height():
                image_height = int(self.height() * 0.95)
                image_width = int(image_height * image_aspect_ratio)

            self.preview_label.setPixmap(
                self.preview_image.scaled(
                    image_width,
                    image_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.preview_label.setFixedSize(image_width, image_height)

    def update_preview_with_options(
        self, include_start_pos: bool, sequence: list[dict], options: dict
    ):
        self.image = (
            self.export_dialog.export_manager.image_creator.create_sequence_image(
                sequence, include_start_pos, options
            )
        )
        self.preview_image = QPixmap.fromImage(self.image)
        self.update_preview()
