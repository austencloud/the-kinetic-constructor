from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsItem
from settings.numerical_constants import (
    DEFAULT_GRAPHBOARD_HEIGHT,
    DEFAULT_GRAPHBOARD_WIDTH,
    PICTOGRAPH_SCALE,
)


class PictographImage(QGraphicsItem):
    def __init__(self, state, image: QImage, parent=None):
        super().__init__(parent)
        self.state = state
        self.image = image
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def paint(self, painter: QPainter, option, widget):
        scaled_image = self.image.scaled(
            int(DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE),
            int(DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        painter.drawImage(
            QRectF(0, 0, scaled_image.width(), scaled_image.height()), scaled_image
        )

    def boundingRect(self):
        return QRectF(
            0,
            0,
            DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE,
            DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE,
        )

    def mousePressEvent(self, event):
        event.accept()
