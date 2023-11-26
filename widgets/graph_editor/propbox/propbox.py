from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QGraphicsScene,
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.staff import Staff
from widgets.graph_editor.propbox.propbox_view import PropBoxView
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import (
    NORTH,
    EAST,
    SOUTH,
    WEST,
    COLOR,
    RED,
    BLUE,
    LOCATION,
    LAYER,
)

from typing import TYPE_CHECKING
from objects.grid import Grid
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graphboard.graphboard import GraphBoard

class PropBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graphboard:"GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.graphboard = graphboard
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = PropBoxView(self)
        self.grid = Grid("resources/images/grid/grid_simple.svg")
        self.setSceneRect(0, 0, int(750), int(750))
        self.addItem(self.grid)
        self.grid.setPos(0, 0)        
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)
        self.init_propbox_staffs(self)

    def init_propbox_staffs(self, propbox) -> None:
        self.propbox_staff_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_staff_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_staff_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_staff = Staff(self.main_widget, self.graphboard, red_propbox_staff_dict)
        blue_staff = Staff(self.main_widget, self.graphboard, blue_propbox_staff_dict)

        red_staff.setPos(self.propbox_staff_locations[EAST])
        blue_staff.setPos(self.propbox_staff_locations[NORTH])

        self.addItem(red_staff)
        self.addItem(blue_staff)

        red_staff.show()
        blue_staff.show()

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
