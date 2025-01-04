from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerImageLabel(QLabel):
    placeholder_text = "Select a sequence to display it here."

    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__()
        self.sequence_viewer = sequence_viewer
        self.thumbnails = sequence_viewer.thumbnails
        self.current_index = sequence_viewer.current_index
        self.metadata_extractor = sequence_viewer.main_widget.metadata_extractor
        self.is_selected = False
        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)
        self.setText(self.placeholder_text)

    def update_thumbnail(self):
        self.thumbnails = self.sequence_viewer.thumbnails
        pixmap = QPixmap(self.thumbnails[self.sequence_viewer.current_index])
        self.set_pixmap_to_fit(pixmap)

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        current_index = self.sequence_viewer.current_index
        sequence_length = self.metadata_extractor.get_sequence_length(
            self.thumbnails[current_index]
        )
        
        target_width = self._get_target_width(sequence_length)

        scaled_pixmap = pixmap.scaledToWidth(
            target_width, Qt.TransformationMode.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)

    def _get_target_width(self, sequence_length):
        if sequence_length == 1:
            target_width = int(self.sequence_viewer.width() * 0.6)
        else:
            target_width = int(self.sequence_viewer.width() * 0.9)
        return target_width

    def show_placeholder(self):
        self.setText(self.placeholder_text)
        self.resize_placeholder()

    def resize_placeholder(self):
        min_height = int(max(self.sequence_viewer.height() / 5, 50))
        self.setMinimumHeight(min_height)
        placeholder_text_font_size = self.sequence_viewer.width() // 50
        global_settings = (
            self.sequence_viewer.browse_tab.main_widget.main_window.settings_manager.global_settings
        )
        font_color = self.sequence_viewer.browse_tab.main_widget.font_color_updater.get_font_color(
            global_settings.get_background_type()
        )
        self.setStyleSheet(
            f"font: {placeholder_text_font_size}pt Arial; font-weight: bold; color: {font_color};"
        )

    def scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = int(self.sequence_viewer.width() * 0.9)
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
        if new_height > self.sequence_viewer.height() * 0.7:
            new_height = int(self.sequence_viewer.height() * 0.7)
            label_width = int(new_height / aspect_ratio)

        scaled_pixmap = pixmap.scaled(
            label_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled_pixmap)
        self.setFixedHeight(new_height)

    def resizeEvent(self, event):
        if self.pixmap().width():
            self.update_thumbnail()
        else:
            self.resize_placeholder()
