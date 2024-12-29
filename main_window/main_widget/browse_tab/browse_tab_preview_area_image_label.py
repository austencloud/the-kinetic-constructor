from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab_preview_area import (
        BrowseTabPreviewArea,
    )


class BrowseTabPreviewAreaImageLabel(QLabel):
    def __init__(self, preview_area: "BrowseTabPreviewArea"):
        super().__init__()
        self.preview_area = preview_area
        self.thumbnails = preview_area.thumbnails
        self.current_index = preview_area.current_index
        self.metadata_extractor = preview_area.main_widget.metadata_extractor
        self.is_selected = False
        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)

    def update_thumbnail(self):
        self.thumbnails = self.preview_area.thumbnails
        if self.thumbnails:
            pixmap = QPixmap(self.thumbnails[self.preview_area.current_index])
            self.set_pixmap_to_fit(pixmap)
        else:
            self.setText("No image available")

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        current_index = self.preview_area.current_index
        sequence_length = self.metadata_extractor.get_sequence_length(
            self.thumbnails[current_index]
        )
        if sequence_length == 1:
            target_width = int(self.preview_area.width() * 0.6)
        else:
            target_width = int(self.preview_area.width() * 0.9)

        scaled_pixmap = pixmap.scaledToWidth(
            target_width, Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

    def show_placeholder(self):
        self.setText("Select a sequence to display it here.")
        self.style_placeholder()

    def style_placeholder(self):
        placeholder_text_font_size = self.preview_area.width() // 50
        global_settings = (
            self.preview_area.browse_tab.main_widget.main_window.settings_manager.global_settings
        )
        font_color = (
            self.preview_area.browse_tab.main_widget.font_color_updater.get_font_color(
                global_settings.get_background_type()
            )
        )
        self.setStyleSheet(
            f"font: {placeholder_text_font_size}pt Arial; font-weight: bold; color: {font_color};"
        )

    def scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = int(self.preview_area.width() * 0.9)
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
        if new_height > self.preview_area.height() * 0.7:
            new_height = int(self.preview_area.height() * 0.7)
            label_width = int(new_height / aspect_ratio)

        scaled_pixmap = pixmap.scaled(
            label_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled_pixmap)
        self.setMinimumHeight(new_height)

    def resizeEvent(self, event):
        min_height = int(max(self.preview_area.height() / 5, 50))
        self.setMinimumHeight(min_height)

        if self.pixmap().width():
            self.update_thumbnail()
        else:
            # resize the placeholder text
            self.style_placeholder()
