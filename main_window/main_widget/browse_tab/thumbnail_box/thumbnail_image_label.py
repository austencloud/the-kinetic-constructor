from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import (
        ThumbnailBox,
    )


class ThumbnailImageLabel(QLabel):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box

        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.target_width = 0
        self.thumbnails = thumbnail_box.thumbnails
        self.metadata_extractor = thumbnail_box.main_widget.metadata_extractor
        self.is_selected = False
        self.index = None
        self.pixmap: QPixmap = None
        self.setScaledContents(False)

    def update_thumbnail(self, index):
        if self.thumbnails and 0 <= index < len(self.thumbnails):
            if index != self.index:
                self.index = index
                self.pixmap = QPixmap(self.thumbnails[index])
                self.set_pixmap_to_fit(self.pixmap)
            else:
                self.set_pixmap_to_fit(self.pixmap)
        else:
            self.setText("No image available")

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        sequence_length = self.metadata_extractor.get_sequence_length(
            self.thumbnail_box.thumbnails[self.thumbnail_box.current_index]
        )
        if sequence_length == 1:
            target_width = int(self.thumbnail_box.width() * 0.6) - int(
                self.thumbnail_box.margin * 2
            )
        else:
            target_width = self.thumbnail_box.width() - int(
                self.thumbnail_box.margin * 2
            )
        if target_width == self.target_width:
            return
        self.target_width = target_width
        scaled_pixmap = pixmap.scaledToWidth(
            target_width, Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        pass

    def mousePressEvent(self, event: "QMouseEvent"):
        if self.thumbnails:
            metadata = self.metadata_extractor.extract_metadata_from_file(
                self.thumbnails[0]
            )
            self.thumbnail_box.browse_tab.selection_handler.thumbnail_clicked(
                self,
                QPixmap(self.thumbnails[self.thumbnail_box.current_index]),
                metadata,
                self.thumbnails,
                self.thumbnail_box.current_index,
            )
        else:
            self.thumbnail_box.browse_tab.deletion_handler.delete_variation(
                self.thumbnail_box, self.thumbnail_box.current_index
            )

    def set_selected(self, selected: bool):
        self.is_selected = selected
        if selected:
            self.setStyleSheet("border: 3px solid blue;")
        else:
            self.setStyleSheet("border: 3px solid black;")

    def eventFilter(self, obj, event: QEvent):
        if obj == self and event.type() == QEvent.Type.Enter:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.setStyleSheet("border: 3px solid gold;")
        elif obj == self and event.type() == QEvent.Type.Leave:
            self.setStyleSheet(
                "border: 3px solid black;"
                if not self.is_selected
                else "border: 3px solid blue;"
            )
        return super().eventFilter(obj, event)
