from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import (
    STAFF_WIDTH,
    STAFF_LENGTH,
)
from settings.string_constants import *
from objects.staff.staff_attributes import StaffAttributes
from objects.staff.staff_positioner import StaffPositioner
from objects.staff.staff_attributes import StaffAttributes
import logging



logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

""" 
staff_dict = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }
        
"""


class Staff(QGraphicsSvgItem):
    def __init__(self, scene, staff_dict):
        super().__init__()
        self.svg_file = STAFF_SVG_PATH
        self.scene = scene
        self.arrow = None
        self.setup_managers()
        self.set_dict_attributes(staff_dict)
        self.set_app_attributes()
        self.main_widget = scene.main_widget

    def setup_managers(self):
        self.positioner = StaffPositioner(self, self.scene)
        self.attributes = StaffAttributes(self)

    def set_dict_attributes(self, staff_dict):
        self.attributes.update_attributes_from_dict(self, staff_dict)
        self.color = staff_dict.get(COLOR)
        self.location = staff_dict.get(LOCATION)
        self.layer = staff_dict.get(LAYER)
        self.set_axis(staff_dict)
        self.set_rotation_from_axis()

    def set_axis(self, staff_dict):
        axis_switch = {
            1: {HORIZONTAL: [WEST, EAST], VERTICAL: [NORTH, SOUTH]},
            2: {HORIZONTAL: [NORTH, SOUTH], VERTICAL: [WEST, EAST]},
        }
        try:
            self.axis = next(
                axis
                for axis, locations in axis_switch.get(self.layer, {}).items()
                if staff_dict.get(LOCATION) in locations
            )
        except StopIteration:
            self.axis = HORIZONTAL

    def set_app_attributes(self):
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.set_color(self.color)

    def get_staff_center(self):
        if self.axis == VERTICAL:
            return QPointF((STAFF_WIDTH / 2), -(STAFF_LENGTH / 2))
        elif self.axis == HORIZONTAL:
            return QPointF(-(STAFF_LENGTH / 2), -(STAFF_WIDTH / 2))

    def update_appearance(self):
        self.set_color(self.color)
        if self.location:
            self.set_axis_from_location(self.location)
        else:
            logging.warning("Staff has no location")
        self.set_rotation_from_axis()

    def set_axis_from_location(self, location):
        if self.layer == 1:
            self.axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        self.setPos(self.scene.grid.handpoints[location])

    def set_color(self, new_color):
        hex_color = COLOR_MAP.get(new_color, new_color)
        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read().replace(RED_HEX, hex_color).replace(BLUE_HEX, hex_color)
        self.renderer.load(svg_data.encode("utf-8"))

        self.setSharedRenderer(self.renderer)  # Re-attach the renderer
        self.color = new_color

    def swap_axis(self):
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.set_rotation_from_axis()

    def set_rotation_from_axis(self):
        if self.axis == VERTICAL:
            self.current_position = self.pos()
            self.setRotation(90)
        else:
            self.setRotation(0)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            offset = self.get_staff_center(self.scene.scale)
            x_offset, y_offset = offset.x(), offset.y()
            self.setPos(
                event.scenePos().x() + x_offset, event.scenePos().y() + y_offset
            )
        super().mouseMoveEvent(event)
