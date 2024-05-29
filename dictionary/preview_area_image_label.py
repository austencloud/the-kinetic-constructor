from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent
from PyQt6.QtWidgets import QLabel, QApplication
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea


class PreviewAreaImageLabel(QLabel):
    def __init__(self, preview_area: "DictionaryPreviewArea"):
        super().__init__()
        self.preview_area = preview_area

        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.thumbnails = preview_area.thumbnails
        self.current_index = preview_area.current_index
        self.metadata_extractor = preview_area.main_widget.metadata_extractor
        self.browser = preview_area.dictionary_widget.browser
        self.is_selected = False

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
