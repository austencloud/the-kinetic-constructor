from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import (
    STAFF_WIDTH,
    STAFF_LENGTH,
)
from settings.string_constants import (
    STAFF_ATTRIBUTES,
    COLOR,
    LOCATION,
    LAYER,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    HORIZONTAL,
    VERTICAL,
    STAFF_SVG_FILE_PATH,
    STAFF_DIR,
    RED,
    BLUE,
    COLOR_MAP,
    CLOCKWISE,
    RED_HEX,
    BLUE_HEX,
)
import logging


logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Staff(QGraphicsSvgItem):
    def __init__(self, graphboard, attributes):
        super().__init__()
        self._setup(graphboard, attributes)

    ### UPDATERS ###

    def _setup(self, graphboard, attributes):
        self.svg_file = STAFF_SVG_FILE_PATH
        self._setup_svg_renderer()
        self._setup_attributes(graphboard, attributes)
        self._setup_graphics_flags()

    def _setup_attributes(self, graphboard, attributes):
        self.arrow = None

        self.color = None
        self.location = None
        self.layer = None

        self.center = self.boundingRect().center()
        self.graphboard = graphboard

        if attributes:
            self.set_attributes_from_dict(attributes)
            self.update_appearance()
            self.update_axis(self.location)
            self.set_rotation_from_axis()

    def _setup_graphics_flags(self):
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def _setup_svg_renderer(self):
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)

    def update_position(self, event):
        offset = self.get_staff_center()
        new_pos = QPointF(
            event.scenePos().x() + offset.x(), event.scenePos().y() + offset.y()
        )
        self.setPos(new_pos)

    def update_staff_orientation(self, mouse_pos):
        # Find the closest handpoint and set axis and rotation
        closest_handpoint, closest_location = self.get_closest_handpoint(mouse_pos)
        self.update_axis(closest_location)
        self.update_appearance()

    def update_axis(self, location):
        if self.layer == 1:
            self.axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        self.setPos(self.graphboard.grid.handpoints[location])

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
            self.update_axis(self.location)
        else:
            logging.warning("Staff has no location")
        self.set_rotation_from_axis()

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self._setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_dict_attr_from_object(self):
        for attr in STAFF_ATTRIBUTES:
            self.attributes[attr] = getattr(self, attr)

    def set_attributes_from_dict(self, attributes):
        for attr in STAFF_ATTRIBUTES:
            value = attributes.get(attr)
            setattr(self, attr, value)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            LOCATION: attributes.get(LOCATION, None),
            LAYER: attributes.get(LAYER, None),
        }

    def update_attributes_from_arrow(self, arrow):
        new_dict = {
            COLOR: arrow.color,
            LOCATION: arrow.end_location,
            LAYER: 1,
        }
        self.attributes.update(new_dict)
        self.update_appearance()

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

    def get_svg_file(self):
        svg_file = f"{STAFF_DIR}staff.svg"
        return svg_file

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
