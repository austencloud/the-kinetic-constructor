from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt, QPointF
from settings import GRAPHBOARD_SCALE
from managers.staff_managers.propbox_staff_manager import PropboxStaffManager
from PyQt6.QtGui import QTransform
from objects.grid import Grid
class PropBoxView(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        self.main_window = main_widget.main_window
        self.staff_manager = PropboxStaffManager(main_widget)
        self.main_widget = main_widget
         
        self.propbox_scene = QGraphicsScene()
        self.propbox_frame = QFrame(self.main_window)
        self.setScene(self.propbox_scene)

        self.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.setSceneRect(0, 0, int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))

        self.propbox_layout = QVBoxLayout()
        self.propbox_frame.setLayout(self.propbox_layout)
        self.propbox_layout.addWidget(self)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)

        main_widget.propbox_view = self
        main_widget.propbox_scene = self.propbox_scene




