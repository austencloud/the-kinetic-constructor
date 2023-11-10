from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import (
    STAFF_WIDTH,
    STAFF_LENGTH,
)
from settings.string_constants import *
import logging


logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Staff(QGraphicsSvgItem):
    STAFF_ATTRIBUTES = [COLOR, LOCATION, LAYER]

    def __init__(self, graphboard, attributes):
        super().__init__()
        self.svg_file = STAFF_SVG_PATH
        self.scene = graphboard
        self.graphboard = graphboard
        self.arrow = None
        if attributes:
            self.update_object_attr_from_dict(attributes)
            self.update_axis(attributes)
            self.set_rotation_from_axis()
            self.update_app_attributes()

    ### UPDATERS ###

    def update_position(self, event):
        offset = self.get_staff_center()
        new_pos = QPointF(
            event.scenePos().x() + offset.x(), event.scenePos().y() + offset.y()
        )
        self.setPos(new_pos)

    def update_staff_orientation(self, mouse_pos):
        # Find the closest handpoint and set axis and rotation
        closest_handpoint, closest_location = self.get_closest_handpoint(mouse_pos)
        self.update_axis_from_location(closest_location)
        self.update_appearance()

    def update_axis_from_location(self, location):
        if self.layer == 1:
            self.axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        self.setPos(self.scene.grid.handpoints[location])

    def update_color(self, new_color):
        hex_color = COLOR_MAP.get(new_color, new_color)
        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read().replace(RED_HEX, hex_color).replace(BLUE_HEX, hex_color)
        self.renderer.load(svg_data.encode("utf-8"))

        self.setSharedRenderer(self.renderer)  # Re-attach the renderer
        self.color = new_color

    def update_appearance(self):
        self.update_color(self.color)
        if self.location:
            self.update_axis_from_location(self.location)
        else:
            logging.warning("Staff has no location")
        self.set_rotation_from_axis()

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self._setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_axis(self, dict):
        axis_switch = {
            1: {HORIZONTAL: [WEST, EAST], VERTICAL: [NORTH, SOUTH]},
            2: {HORIZONTAL: [NORTH, SOUTH], VERTICAL: [WEST, EAST]},
        }
        try:
            self.axis = next(
                axis
                for axis, locations in axis_switch.get(self.layer, {}).items()
                if dict.get(LOCATION) in locations
            )
        except StopIteration:
            self.axis = HORIZONTAL

    def update_dict_attr_from_object(self):
        for attr in self.STAFF_ATTRIBUTES:
            self.attributes[attr] = getattr(self, attr)

    def update_object_attr_from_dict(self, attributes):
        for attr in ARROW_ATTRIBUTES:
            value = attributes.get(attr)
            if attr == TURNS:
                value = int(value)
            setattr(self, attr, value)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            LOCATION: attributes.get(LOCATION, None),
            LAYER: attributes.get(LAYER, None),
        }

    def update_app_attributes(self):
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.update_color(self.color)

    def update_attributes_from_arrow(self, arrow):
        new_dict = {
            COLOR: arrow.color,
            LOCATION: arrow.end_location,
            LAYER: 1,
        }
        self.attributes.update(new_dict)
        self.update_appearance()

    def set_transform_origin_to_center(self):
        # Call this method after any changes that might affect the boundingRect.
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    ### GETTERS ###

    def get_staff_center(self):
        if self.axis == VERTICAL:
            return QPointF((STAFF_WIDTH / 2), -(STAFF_LENGTH / 2))
        elif self.axis == HORIZONTAL:
            return QPointF(-(STAFF_LENGTH / 2), -(STAFF_WIDTH / 2))

    def set_rotation_from_axis(self):
        if self.axis == VERTICAL:
            self.current_position = self.pos()
            self.setRotation(90)
        else:
            self.setRotation(0)

    def get_closest_handpoint(self, mouse_pos):
        closest_distance = float("inf")
        closest_handpoint = None
        closest_location = None
        for location, point in self.graphboard.handpoints.items():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_handpoint = point
                closest_location = location
        return closest_handpoint, closest_location

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in self.STAFF_ATTRIBUTES}

    ### MOUSE EVENTS ###
    
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            offset = self.get_staff_center()
            x_offset, y_offset = offset.x(), offset.y()
            self.setPos(
                event.scenePos().x() + x_offset, event.scenePos().y() + y_offset
            )
        super().mouseMoveEvent(event)

    ### HELPERS ###

    def create_staff_dict_from_arrow(self, arrow):
        staff_dict = {COLOR: arrow.color, LOCATION: arrow.end_location, LAYER: 1}
        return staff_dict

    def swap_axis(self):
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.set_rotation_from_axis()




class RedStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)
        self.update_color(RED)


class BlueStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)
        self.update_color(BLUE)
