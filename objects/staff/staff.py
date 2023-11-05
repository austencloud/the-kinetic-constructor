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
        self.view = scene.views()[0]
        self.handler = self.view.staff_handler
        self.initialize_dict_attributes(staff_dict)
        self.initialize_app_attributes()

    def initialize_dict_attributes(self, staff_dict):
        """Initialize attributes from the given dictionary."""
        self.attributes = self.handler.attributes
        self.attributes.update_attributes_from_dict(self, staff_dict)
        self.color = staff_dict.get(COLOR)
        self.location = staff_dict.get(LOCATION)
        self.layer = staff_dict.get(LAYER)
        self.set_axis(staff_dict)
        self.set_rotation_from_axis()

    def set_axis(self, staff_dict):
        """Set the axis based on the staff dictionary."""
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

    def initialize_app_attributes(self):
        """Initialize application-specific attributes."""
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setScale(self.view.view_scale)
        self.set_color(self.color)

    def get_staff_center(self, scale):
        if self.axis == VERTICAL:
            return QPointF((STAFF_WIDTH / 2) * scale, -(STAFF_LENGTH / 2) * scale)
        elif self.axis == HORIZONTAL:
            return QPointF(-(STAFF_LENGTH / 2) * scale, -(STAFF_WIDTH / 2) * scale)

    def update_appearance(self):
        self.set_color(self.color)
        self.set_axis_from_location(self.location)
        self.set_rotation_from_axis()

    def set_axis_from_location(self, location):
        if self.layer == 1:
            self.axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        self.setPos(self.handler.staff_xy_locations[location])

    def set_color(self, new_color):
        hex_color = COLOR_MAP.get(new_color, new_color)
        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read().replace(RED_HEX, hex_color).replace(BLUE_HEX, hex_color)
        self.renderer.load(svg_data.encode("utf-8"))

        if not self.renderer.isValid():
            print("Renderer is not valid. SVG data might be incorrect.")

        self.setSharedRenderer(self.renderer)  # Re-attach the renderer
        self.color = new_color
        self.scene.update()  # Force a redraw

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
            offset = self.get_staff_center(self.view.view_scale)
            x_offset, y_offset = offset.x(), offset.y()
            self.setPos(
                event.scenePos().x() + x_offset, event.scenePos().y() + y_offset
            )
        super().mouseMoveEvent(event)
