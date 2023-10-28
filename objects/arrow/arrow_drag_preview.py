from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QRectF

class ArrowDragPreview(QGraphicsItem):
    def __init__(self, pixmap):
        super().__init__()
        self.pixmap = pixmap

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.pixmap)

    def boundingRect(self):
        return QRectF(self.pixmap.rect())
