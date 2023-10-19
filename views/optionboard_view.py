from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from settings import GRAPHBOARD_HEIGHT
from PyQt6.QtWidgets import QGraphicsRectItem, QPushButton
from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QImage, QPainter, QColor
from objects.arrow import Arrow
from objects.staff import Staff
from objects.grid import Grid
from views.graphboard_view import Graphboard_View
from pictograph import Pictograph
from settings import DEFAULT_GRAPHBOARD_WIDTH, DEFAULT_GRAPHBOARD_HEIGHT, PICTOGRAPH_SCALE

class Optionboard_View(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        optionboard_scene = QGraphicsScene()
        optionboard_scene.setSceneRect(0, 0, main_widget.main_window.width(), 1 * GRAPHBOARD_HEIGHT * 2)
        self.setFixedSize(int(optionboard_scene.sceneRect().width()), int(optionboard_scene.sceneRect().height()))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.show()
        

