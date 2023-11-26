from PyQt6.QtWidgets import (
    QVBoxLayout,
    QGraphicsScene,
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.props.staff import Staff
from widgets.graph_editor.propbox.propbox_view import PropBoxView
from settings.string_constants import (
    IN,
    NORTH,
    EAST,
    OUT,
    SOUTH,
    WEST,
    COLOR,
    RED,
    BLUE,
    LOCATION,
    LAYER,
    ORIENTATION,
    AXIS,
    VERTICAL,
    HORIZONTAL,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
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
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.graphboard = graphboard
        self.grid = Grid("resources/images/grid/grid.svg")
        self.grid_position = QPointF(0, 0)
        self.grid.setPos(self.grid_position)
        self.addItem(self.grid)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = PropBoxView(self)
        self.setSceneRect(0, 0, int(750), int(750))
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)
        self.init_propbox_staffs()
        # self.init_propbox_clubs()
        # self.init_propbox_buugeng()
        # self.init_propbox_fans()
        # self.init_propbox_triads()
        # self.init_propbox_hoops()

    def init_propbox_staffs(self) -> None:
        self.staff_config = {
            "n_layer1": {
                COLOR: RED,
                LOCATION: NORTH,
                LAYER: 2,
                AXIS: VERTICAL,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            "e_layer1": {
                COLOR: BLUE,
                LOCATION: EAST,
                LAYER: 2,
                AXIS: HORIZONTAL,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            "s_layer1": {
                COLOR: RED,
                LOCATION: SOUTH,
                LAYER: 2,
                AXIS: VERTICAL,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            "w_layer1": {
                COLOR: BLUE,
                LOCATION: WEST,
                LAYER: 2,
                AXIS: HORIZONTAL,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            # 'n_layer2': {COLOR: BLUE, LOCATION: NORTH, LAYER: 2},
            # 'e_layer2': {COLOR: RED, LOCATION: EAST, LAYER: 2},
            # 's_layer2': {COLOR: BLUE, LOCATION: SOUTH, LAYER: 2},
            # 'w_layer2': {COLOR: RED, LOCATION: WEST, LAYER: 2},
        }

        for key, attrs in self.staff_config.items():
            staff = Staff(self.main_widget, self.graphboard, attrs)
            staff.setTransformOriginPoint(QPointF(0, 0))
            staff.setPos(self.calculate_staff_position(key, staff))
            self.addItem(staff)
            staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

    def calculate_staff_position(self, key: str, staff: Staff) -> QPointF:
        location = self.staff_config[key][LOCATION]
        layer = self.staff_config[key][LAYER]
        orientation = self.staff_config[key][ORIENTATION]
        handpoint = self.grid.get_circle_coordinates(f"{location}_hand_point")

        staff_length = staff.boundingRect().width()
        staff_width = staff.boundingRect().height()

        # Adjust position based on layer and location
        if layer == 1 and orientation == IN:
            if location == NORTH:
                offset_x = staff_width / 2
                offset_y = -staff_length / 2
            elif location == SOUTH:
                offset_x = -staff_width / 2
                offset_y = staff_length / 2
            elif location == EAST:
                offset_x = staff_length / 2
                offset_y = staff_width / 2
            elif location == WEST:
                offset_x = -staff_length / 2
                offset_y = -staff_width / 2

        elif layer == 1 and orientation == OUT:
            if location == NORTH:
                offset_x = -staff_width / 2
                offset_y = staff_length / 2
            elif location == SOUTH:
                offset_x = staff_width / 2
                offset_y = -staff_length / 2
            elif location == EAST:
                offset_x = -staff_length / 2
                offset_y = -staff_width / 2
            elif location == WEST:
                offset_x = staff_length / 2
                offset_y = staff_width / 2

        elif layer == 2 and orientation == CLOCKWISE:
            if location == NORTH:
                offset_x = -staff_length / 2
                offset_y = -staff_width / 2
            elif location == SOUTH:
                offset_x = staff_length / 2
                offset_y = staff_width / 2
            elif location == EAST:
                offset_x = staff_width / 2
                offset_y = -staff_length / 2
            elif location == WEST:
                offset_x = -staff_width / 2
                offset_y = staff_length / 2

        elif layer == 2 and orientation == COUNTER_CLOCKWISE:
            if location == NORTH:
                offset_x = staff_length / 2
                offset_y = staff_width / 2
            elif location == SOUTH:
                offset_x = -staff_length / 2
                offset_y = -staff_width / 2
            elif location == EAST:
                offset_x = -staff_width / 2
                offset_y = staff_length / 2
            elif location == WEST:
                offset_x = staff_width / 2
                offset_y = -staff_length / 2

        return handpoint + QPointF(offset_x, offset_y)

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

        red_buugeng = Buugeng(
            self.main_widget, self.graphboard, red_propbox_buugeng_dict
        )
        blue_buugeng = Buugeng(
            self.main_widget, self.graphboard, blue_propbox_buugeng_dict
        )

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
