from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

class SequenceThumbnail(QGraphicsPixmapItem):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(image_path))
        # ... other initialization ...

    def mousePressEvent(self, event):
        if self._star_rect.contains(event.pos()):
            self.toggle_favorite()

    def toggle_favorite(self):
        # Add or remove from favorites
        # ...

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        # Draw the star icon at the top left corner
        if self.is_favorite:
            painter.drawPixmap(self._star_rect, self._star_pixmap)
