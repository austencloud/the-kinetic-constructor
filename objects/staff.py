from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.graphical_object import GraphicalObject
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
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    RED_HEX,
    BLUE_HEX,
    NORTHEAST,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
    PRO,
    ANTI,
    STATIC,
)
import logging
import re

logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Staff(GraphicalObject):
    def __init__(self, graphboard, attributes):
        svg_file = STAFF_SVG_FILE_PATH
        super().__init__(svg_file, graphboard, attributes)
        self._setup_attributes(graphboard, attributes)

    ### SETUP ###

    def _setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard
        self.drag_offset = QPointF(0, 0)
        self.previous_location = None
        self.arrow = None
        self.ghost_staff = None
        self.color = None
        self.location = None
        self.layer = None
        if attributes:
            self.update(attributes)
        self.center = self.get_staff_center()

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setSelected(True)
        self.ghost_staff = self.graphboard.ghost_staffs[self.color]
        self.ghost_staff.update(self.attributes)
        self.graphboard.addItem(self.ghost_staff)
        self.ghost_staff.arrow = self.arrow
        self.graphboard.staffs.append(self.ghost_staff)
        self.graphboard.staffs.remove(self)
        self.graphboard.update()
        self.graphboard.staffs.append(self)
        for item in self.graphboard.items():
            if item != self:
                item.setSelected(False)

        self.previous_location = self.location

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.get_staff_center()
            self.set_drag_pos(new_pos)

            new_location = self.get_closest_location(event.scenePos())

            if new_location != self.previous_location and self.arrow:
                self.location = new_location
                self.attributes[LOCATION] = new_location
                self.update_axis()
                self.update_appearance()

                self.update_arrow_quadrant(new_location)
                self.attributes[LOCATION] = new_location
                self.ghost_staff.update(self.attributes)
                self.graphboard.staffs.remove(self)
                if self.arrow.motion_type == STATIC:
                    self.arrow.start_location = new_location
                    self.arrow.end_location = new_location
                self.graphboard.update()
                self.graphboard.staffs.append(self)
                new_pos = event.scenePos() - self.get_staff_center()
                self.set_drag_pos(new_pos)
                self.previous_location = new_location

    def set_drag_pos(self, new_pos):
        if self.axis == HORIZONTAL:
            self.setPos(new_pos)
        elif self.axis == VERTICAL:
            self.setPos(
                new_pos
                + QPointF(
                    -STAFF_LENGTH / 2 + STAFF_WIDTH / 2,
                    STAFF_WIDTH / 2 - STAFF_LENGTH / 2,
                )
            )

    def update_arrow_quadrant(self, new_location):
        quadrant_mapping = {
            ### ISO ###
            (NORTHEAST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (NORTHWEST, CLOCKWISE, PRO): {EAST: NORTHEAST, WEST: SOUTHWEST},
            (SOUTHWEST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (SOUTHEAST, CLOCKWISE, PRO): {WEST: SOUTHWEST, EAST: NORTHEAST},
            (NORTHEAST, COUNTER_CLOCKWISE, PRO): {WEST: NORTHWEST, EAST: SOUTHEAST},
            (NORTHWEST, COUNTER_CLOCKWISE, PRO): {SOUTH: SOUTHWEST, NORTH: NORTHEAST},
            (SOUTHWEST, COUNTER_CLOCKWISE, PRO): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (SOUTHEAST, COUNTER_CLOCKWISE, PRO): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            ### ANTI ###
            (NORTHEAST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (NORTHWEST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            (SOUTHWEST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (SOUTHEAST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            (NORTHEAST, COUNTER_CLOCKWISE, ANTI): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (NORTHWEST, COUNTER_CLOCKWISE, ANTI): {WEST: SOUTHWEST, EAST: NORTHEAST},
            (SOUTHWEST, COUNTER_CLOCKWISE, ANTI): {SOUTH: SOUTHEAST, NORTH: NORTHWEST},
            (SOUTHEAST, COUNTER_CLOCKWISE, ANTI): {EAST: NORTHEAST, WEST: SOUTHWEST},
        }

        current_quadrant = self.arrow.quadrant
        rotation_direction = self.arrow.rotation_direction
        motion_type = self.arrow.motion_type
        new_quadrant = quadrant_mapping.get(
            (current_quadrant, rotation_direction, motion_type), {}
        ).get(new_location)

        if new_quadrant:
            self.arrow.quadrant = new_quadrant
            start_location, end_location = self.arrow.get_start_end_locations(
                motion_type, rotation_direction, new_quadrant
            )
            self.arrow.start_location = start_location
            self.arrow.end_location = end_location
            self.arrow.update_appearance()

    def update_for_new_location(self, event, new_location):
        self.location = new_location
        self.attributes[LOCATION] = new_location

        self.ghost_staff.update(self.attributes)

        self.ghost_staff.set_attributes_from_dict(self.attributes)
        self.ghost_staff.update_appearance()
        self.arrow.set_attributes_from_staff(self)
        self.arrow.update_appearance()

        self.update_axis()
        self.update_appearance()

        self.ghost_staff.update(self.attributes)
        self.graphboard.staffs.remove(self)
        self.graphboard.update()
        self.graphboard.staffs.append(self)

    def mouseReleaseEvent(self, event):
        self.graphboard.removeItem(self.ghost_staff)
        self.graphboard.staffs.remove(self.ghost_staff)
        self.ghost_staff.arrow = None
        self.ghost_staff = None
        self.graphboard.update()
        self.finalize_staff_drop(event)

    def finalize_staff_drop(self, event):
        closest_handpoint = self.get_closest_handpoint(event.scenePos())
        new_location = self.get_closest_location(event.scenePos())

        self.attributes[LOCATION] = new_location
        self.location = new_location
        self.update_axis()
        self.update_appearance()
        self.setPos(closest_handpoint)

        if self.arrow:
            self.arrow.update_appearance()
        self.previous_location = new_location
        self.graphboard.update()

    ### UPDATERS ###

    def update_axis(self):
        if self.layer == 1:
            self.axis = VERTICAL if self.location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if self.location in [NORTH, SOUTH] else VERTICAL

    def update_rotation(self):
        if self.axis == VERTICAL:
            self.current_position = self.pos()
            self.setTransformOriginPoint(self.get_staff_center())
            self.setRotation(90)
        else:
            self.setRotation(0)

    def set_attributes_from_dict(self, attributes):
        self.color = attributes.get(COLOR, None)
        self.location = attributes.get(LOCATION, None)
        self.layer = attributes.get(LAYER, None)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            LOCATION: attributes.get(LOCATION, None),
            LAYER: attributes.get(LAYER, None),
        }
        self.update_axis()

    def set_transform_origin_to_center(self):
        self.center = self.get_staff_center()
        self.setTransformOriginPoint(self.center)

    def set_attributes_from_arrow(self, arrow):
        new_dict = {
            COLOR: arrow.color,
            LOCATION: arrow.end_location,
            LAYER: 1,
        }
        self.attributes.update(new_dict)
        self.color = arrow.color
        self.location = arrow.end_location
        self.update_axis()
        self.layer = 1
        self.update_appearance()

    ### GETTERS ###

    def get_rotation_angle(self):
        location_to_angle = self.get_location_to_angle()
        return location_to_angle

    def get_location_to_angle(self):
        if self.location == NORTH or self.location == SOUTH:
            return {
                NORTH: 90,
                SOUTH: 270,
            }.get(self.location, {})
        elif self.location == EAST or self.location == WEST:
            return {
                WEST: 0,
                EAST: 180,
            }.get(self.location, {})
        else:
            return {}

    def get_staff_center(self):
        if self.axis == VERTICAL:
            return QPointF((STAFF_WIDTH / 2), (STAFF_LENGTH / 2))
        elif self.axis == HORIZONTAL:
            return QPointF((STAFF_LENGTH / 2), (STAFF_WIDTH / 2))

    def get_closest_handpoint(self, mouse_pos):
        closest_distance = float("inf")
        closest_handpoint = None
        for point in self.graphboard.grid.handpoints.values():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_handpoint = point
        return closest_handpoint

    def get_closest_location(self, mouse_pos):
        closest_distance = float("inf")
        closest_location = None
        for location, point in self.graphboard.grid.handpoints.items():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_location = location
        return closest_location

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in STAFF_ATTRIBUTES}

    def get_svg_file(self):
        svg_file = f"{STAFF_DIR}staff.svg"
        return svg_file

    ### HELPERS ###

    def create_staff_dict_from_arrow(self, arrow):
        staff_dict = {COLOR: arrow.color, LOCATION: arrow.end_location, LAYER: 1}
        return staff_dict

    def swap_axis(self):
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.update_rotation()

    def set_svg_color(self, new_color):
        color_map = {RED: RED_HEX, BLUE: BLUE_HEX}
        new_hex_color = color_map.get(new_color)

        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode("utf-8")


class RedStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)


class BlueStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)
