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

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class PropBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.view = PropBoxView(self)
        self.view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        self.setSceneRect(
            0, 0, int(450), int(450)
        )
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)
        self.view.setFrameStyle(QFrame.Shape.NoFrame)
        self.scale = GRAPHBOARD_SCALE * 0.75
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.Shape.NoFrame)
        main_widget.propbox = self

    def init_propbox_staffs(self, propbox) -> None:
        self.propbox_staff_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_staff = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_staff = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_staff = Staff(propbox, red_propbox_staff)
        blue_staff = Staff(propbox, blue_propbox_staff)

        red_staff.setPos(self.propbox_staff_locations[EAST])
        blue_staff.setPos(self.propbox_staff_locations[NORTH])

        self.addItem(red_staff)
        self.addItem(blue_staff)

        red_staff.show()
        blue_staff.show()

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
