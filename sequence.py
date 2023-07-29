from PyQt5.QtWidgets import QGraphicsScene

class SequenceConstructor(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pictographs = []

    def add_pictograph(self, pictograph):
        self.pictographs.append(pictograph)
        self.addItem(pictograph)

    def clear(self):
        for pictograph in self.pictographs:
            self.removeItem(pictograph)
        self.pictographs.clear()
