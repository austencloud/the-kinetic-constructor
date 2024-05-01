from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box

        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.mousePressEvent = self.thumbnail_clicked
        self.thumbnails = thumbnail_box.thumbnails
        self.current_index = thumbnail_box.current_index
        self.metadata_extractor = thumbnail_box.metadata_extractor
        self.browser = thumbnail_box.browser
        self.update_thumbnail()
        self.is_selected = False

    def update_thumbnail(self):
        pixmap = QPixmap(self.thumbnails[self.current_index])
        self.setPixmap(
            pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

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

    def thumbnail_clicked(self, event):
        metadata = self.metadata_extractor.extract_metadata_from_file(
            self.thumbnails[0]
        )
        self.browser.dictionary_widget.selection_handler.thumbnail_clicked(
            self,
            QPixmap(self.thumbnails[self.current_index]),
            metadata,
            self.thumbnails,
            self.current_index,
        )

    def set_selected(self, selected: bool):
        self.is_selected = selected
        if selected:
            self.setStyleSheet("border: 3px solid blue;")
        else:
            self.setStyleSheet("border: 3px solid black;")
