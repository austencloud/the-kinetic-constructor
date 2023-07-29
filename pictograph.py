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

    def boundingRect(self):
        # Return the bounding rectangle of the Pictograph
        return QRectF(0, 0, 375, 375)

    def mousePressEvent(self, event):
        # Emit the clicked signal when the Pictograph is clicked
        event.accept()

class Pictograph_Manager(QObject):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.pictographs = []

    def add_pictograph(self, pictograph: Pictograph):
        print("Adding pictograph")
        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.scene.beats):
            if i >= len(self.pictographs):
                # Set the position of the pictograph to the position of the section
                pictograph.setPos(section.pos())
                self.pictographs.append(pictograph)
                self.scene.addItem(pictograph)
                break
        print("Items in the scene:")
        for item in self.scene.items():
            print(item)