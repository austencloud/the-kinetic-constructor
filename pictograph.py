from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QRectF, QObject
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import pyqtSignal

class Pictograph(QGraphicsItem):
    def __init__(self, state, image: QImage, parent=None):
        super().__init__(parent)
        self.state = state
        self.image = image
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        

    def paint(self, painter: QPainter, option, widget):
        print("Paint method called")
        # Render the QImage onto the Pictograph
        painter.drawImage(QRectF(0, 0, 375, 375), self.image)
        print("Pictograph painted")

    def boundingRect(self):
        # Return the bounding rectangle of the Pictograph
        return QRectF(0, 0, 375, 375)

    def mousePressEvent(self, event):
        # Emit the clicked signal when the Pictograph is clicked
        event.accept()

