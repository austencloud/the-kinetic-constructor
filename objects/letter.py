from PyQt6.QtSvgWidgets import QGraphicsSvgItem

class Letter(QGraphicsSvgItem):
    def __init__(self, graphboard):
        self.graphboard = graphboard
        super().__init__()
        