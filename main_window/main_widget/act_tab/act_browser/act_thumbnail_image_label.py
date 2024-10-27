from PIL import Image
import json
from PyQt6.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, QEvent
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QDrag
from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING

from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_browser.act_browser import ActThumbnailBox


class ActThumbnailImageLabel(ThumbnailImageLabel):
    def __init__(self, thumbnail_box: "ActThumbnailBox"):
        super().__init__(thumbnail_box)

    def eventFilter(self, obj, event: QEvent):
        """Override hover behavior for ActBrowser to use an open-hand cursor."""
        if obj == self and event.type() == QEvent.Type.Enter:
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            self.setStyleSheet("border: 3px solid gold;")
            return True
        elif obj == self and event.type() == QEvent.Type.Leave:
            self.setStyleSheet(
                "border: 3px solid black;"
                if not self.is_selected
                else "border: 3px solid blue;"
            )
            return True

        return super().eventFilter(obj, event)

    def extract_metadata(self, image_path):
        """Extract metadata from an image file using PIL."""
        try:
            with Image.open(image_path) as img:
                metadata = img.info.get("metadata")
                return json.loads(metadata) if metadata else {}
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}

    def mousePressEvent(self, event: QMouseEvent):
        """Override click behavior to initiate drag-and-drop."""
        if event.button() == Qt.MouseButton.LeftButton and self.thumbnails:
            # Retrieve metadata from the file
            self.dragging_metadata = self.metadata_extractor.extract_metadata_from_file(
                self.thumbnails[self.thumbnail_box.current_index]
            )

            if self.dragging_metadata:
                # Start the drag-and-drop process and add dummy QMimeData
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText("dummy")  # Dummy content to satisfy QDrag requirements
                drag.setMimeData(mime_data)
                
                # Start the drag operation
                drag.exec(Qt.DropAction.CopyAction)
            else:
                print("No metadata available for this thumbnail.")
