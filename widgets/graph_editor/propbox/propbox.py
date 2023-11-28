from PyQt6.QtWidgets import (
    QVBoxLayout,
    QGraphicsScene,
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.props.prop import Prop
from objects.props.staff import Staff
from widgets.graph_editor.propbox.propbox_drag import PropBoxDrag
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

from typing import TYPE_CHECKING, Dict, List
from objects.grid import Grid

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
from objects.props.club import Club
from objects.props.buugeng import Buugeng
from objects.props.fan import Fan
from objects.props.triad import Triad
from objects.props.hoop import Hoop


class PropBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", pictograph: "Pictograph") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.pictograph = pictograph
        self.grid = Grid("resources/images/grid/grid.svg")
        self.grid_position = QPointF(0, 0)
        self.grid.setPos(self.grid_position)
        self.addItem(self.grid)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = PropBoxView(self)
        self.setSceneRect(0, 0, int(750), int(750))
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)
        # self.init_propbox_clubs()
        # self.init_propbox_buugeng()
        # self.init_propbox_fans()
        # self.init_propbox_triads()
        # self.init_propbox_hoops()

        self.props: List[Prop] = []
        self.staffs: List[Staff] = []
        self.clubs: List[Club] = []
        self.buugeng: List[Buugeng] = []
        self.fans: List[Fan] = []
        self.triads: List[Triad] = []
        self.hoops: List[Hoop] = []

        self.populate_staffs()

    def populate_staffs(self) -> None:
        initial_staff_attribute_collection: List[Dict] = [
            {
                COLOR: RED,
                LOCATION: NORTH,
                LAYER: 1,
                ORIENTATION: OUT,
            },
            {
                COLOR: BLUE,
                LOCATION: EAST,
                LAYER: 1,
                ORIENTATION: OUT,
            },
            {
                COLOR: RED,
                LOCATION: SOUTH,
                LAYER: 1,
                ORIENTATION: OUT,
            },
            {
                COLOR: BLUE,
                LOCATION: WEST,
                LAYER: 1,
                ORIENTATION: OUT,
            },
            {
                COLOR: RED,
                LOCATION: NORTH,
                LAYER: 2,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            {
                COLOR: BLUE,
                LOCATION: EAST,
                LAYER: 2,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            {
                COLOR: RED,
                LOCATION: SOUTH,
                LAYER: 2,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
            {
                COLOR: BLUE,
                LOCATION: WEST,
                LAYER: 2,
                ORIENTATION: COUNTER_CLOCKWISE,
            },
        ]

        for attributes in initial_staff_attribute_collection:
            staff = Staff(self.main_widget, self.pictograph, attributes)
            staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
            staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)

            handpoint = self.grid.get_circle_coordinates(f"{staff.location}_hand_point")
            staff_length = staff.boundingRect().width()
            staff_width = staff.boundingRect().height()
            offset_x = -staff_length / 2
            offset_y = -staff_width / 2
            staff_position = handpoint + QPointF(offset_x, offset_y)

            staff.update_appearance()
            staff.setTransformOriginPoint(staff.boundingRect().center())
            staff.setPos(staff_position)

            self.addItem(staff)
            self.staffs.append(staff)

        self.staffs = self.props

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

        red_club = Club(self.main_widget, self.pictograph, red_propbox_club_dict)
        blue_club = Club(self.main_widget, self.pictograph, blue_propbox_club_dict)

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
            self.main_widget, self.pictograph, red_propbox_buugeng_dict
        )
        blue_buugeng = Buugeng(
            self.main_widget, self.pictograph, blue_propbox_buugeng_dict
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

        red_fan = Fan(self.main_widget, self.pictograph, red_propbox_fan_dict)
        blue_fan = Fan(self.main_widget, self.pictograph, blue_propbox_fan_dict)

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

        red_triad = Triad(self.main_widget, self.pictograph, red_propbox_triad_dict)
        blue_triad = Triad(self.main_widget, self.pictograph, blue_propbox_triad_dict)

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

        red_hoop = Hoop(self.main_widget, self.pictograph, red_propbox_hoop_dict)
        blue_hoop = Hoop(self.main_widget, self.pictograph, blue_propbox_hoop_dict)

        red_hoop.setPos(hoop_locations[EAST])
        blue_hoop.setPos(hoop_locations[NORTH])

        self.addItem(red_hoop)
        self.addItem(blue_hoop)

        red_hoop.show()
        blue_hoop.show()

        red_hoop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_hoop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        # Find the closest arrow to the cursor position
        closest_prop = None
        min_distance = float("inf")
        for prop in self.props:
            prop_center = prop.sceneBoundingRect().center()
            distance = (scene_pos - prop_center).manhattanLength()
            if distance < min_distance:
                closest_prop = prop
                min_distance = distance

        # Proceed only if the closest prop is found
        if closest_prop:
            self.target_prop = closest_prop
            if not self.propbox_drag:
                pictograph = self.main_widget.graph_editor.pictograph
                self.propbox_drag = PropBoxDrag(self.main_window, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.propbox_drag.match_target_arrow(self.target_arrow)
                self.propbox_drag.start_drag(event_pos)
        else:
            # If no closest arrow is found, ignore the event
            self.target_arrow = None
            event.ignore()
