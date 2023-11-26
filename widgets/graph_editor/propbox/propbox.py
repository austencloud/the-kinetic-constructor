from PyQt6.QtWidgets import (
    QVBoxLayout,
    QGraphicsScene,
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.props.staff import Staff
from widgets.graph_editor.propbox.propbox_view import PropBoxView
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
from objects.props.club import Club
from objects.props.buugeng import Buugeng
from objects.props.fan import Fan
from objects.props.triad import Triad
from objects.props.hoop import Hoop


class PropBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graphboard:"GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.graphboard = graphboard
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = PropBoxView(self)
        self.setSceneRect(0, 0, int(650), int(650))
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)
        self.init_propbox_staffs()
        # self.init_propbox_clubs()
        # self.init_propbox_buugeng()
        # self.init_propbox_fans()
        # self.init_propbox_triads()
        # self.init_propbox_hoops()
        

    def init_propbox_staffs(self) -> None:
        red_propbox_staff_dict = {
            COLOR: RED,
            LOCATION: NORTH,
            LAYER: 1,
        }
        blue_propbox_staff_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_staff = Staff(self.main_widget, self.graphboard, red_propbox_staff_dict)
        blue_staff = Staff(self.main_widget, self.graphboard, blue_propbox_staff_dict)
        
        red_staff.setTransformOriginPoint(red_staff.boundingRect().center())
        blue_staff.setTransformOriginPoint(blue_staff.boundingRect().center())

        red_staff.setPos(QPointF(0, 0))
        # blue_staff.setPos(QPointF(75, 25))

        self.addItem(red_staff)
        # self.addItem(blue_staff)

        red_staff.show()
        blue_staff.show()

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

    def init_propbox_clubs(self) -> None:
        club_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_club_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_club_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_club = Club(self.main_widget, self.graphboard, red_propbox_club_dict)
        blue_club = Club(self.main_widget, self.graphboard, blue_propbox_club_dict)

        red_club.setPos(club_locations[EAST])
        blue_club.setPos(club_locations[NORTH])

        self.addItem(red_club)
        self.addItem(blue_club)

        red_club.show()
        blue_club.show()

        red_club.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_club.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        
    def init_propbox_buugeng(self) -> None:
        buugeng_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_buugeng_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_buugeng_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_buugeng = Buugeng(self.main_widget, self.graphboard, red_propbox_buugeng_dict)
        blue_buugeng = Buugeng(self.main_widget, self.graphboard, blue_propbox_buugeng_dict)

        red_buugeng.setPos(buugeng_locations[EAST])
        blue_buugeng.setPos(buugeng_locations[NORTH])

        self.addItem(red_buugeng)
        self.addItem(blue_buugeng)

        red_buugeng.show()
        blue_buugeng.show()

        red_buugeng.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_buugeng.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        
    def init_propbox_fans(self) -> None:
        fan_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_fan_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_fan_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_fan = Fan(self.main_widget, self.graphboard, red_propbox_fan_dict)
        blue_fan = Fan(self.main_widget, self.graphboard, blue_propbox_fan_dict)

        red_fan.setPos(fan_locations[EAST])
        blue_fan.setPos(fan_locations[NORTH])

        self.addItem(red_fan)
        self.addItem(blue_fan)

        red_fan.show()
        blue_fan.show()

        red_fan.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_fan.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

    def init_propbox_triads(self) -> None:
        triad_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_triad_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_triad_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_triad = Triad(self.main_widget, self.graphboard, red_propbox_triad_dict)
        blue_triad = Triad(self.main_widget, self.graphboard, blue_propbox_triad_dict)

        red_triad.setPos(triad_locations[EAST])
        blue_triad.setPos(triad_locations[NORTH])

        self.addItem(red_triad)
        self.addItem(blue_triad)

        red_triad.show()
        blue_triad.show()

        red_triad.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_triad.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        
    def init_propbox_hoops(self) -> None:
        hoop_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_hoop_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_hoop_dict = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        red_hoop = Hoop(self.main_widget, self.graphboard, red_propbox_hoop_dict)
        blue_hoop = Hoop(self.main_widget, self.graphboard, blue_propbox_hoop_dict)

        red_hoop.setPos(hoop_locations[EAST])
        blue_hoop.setPos(hoop_locations[NORTH])

        self.addItem(red_hoop)
        self.addItem(blue_hoop)

        red_hoop.show()
        blue_hoop.show()

        red_hoop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_hoop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        
