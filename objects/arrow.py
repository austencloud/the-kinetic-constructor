from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
import re
from settings.string_constants import (
    MOTION_TYPE,
    TURNS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    RED,
    BLUE,
    RED_HEX,
    BLUE_HEX,
    PRO,
    ANTI,
    STATIC,
    ROTATION_DIRECTION,
    QUADRANT,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    START_LOCATION,
    END_LOCATION,
    ARROW_ATTRIBUTES,
    ARROW_DIR,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    LOCATION,
    LAYER,
    NORTH,
    WEST,
    SOUTH,
    EAST,
)
from data.start_end_location_mapping import start_end_location_mapping
from collections import namedtuple

# Define a named tuple for clarity
Orientation = namedtuple(
    "Orientation", ["new_quadrant", "start_location", "end_location"]
)


class Arrow(QGraphicsSvgItem):
    def __init__(self, graphboard, attributes):
        super().__init__()
        if attributes:
            self.svg_file = self.get_svg_file(
                attributes.get(MOTION_TYPE), attributes.get(TURNS)
            )
            self._setup_svg_renderer(self.svg_file)
        self._setup(graphboard, attributes)

    ### SETUP ###
    
    def _setup(self, graphboard, attributes):
        self._setup_attributes(graphboard, attributes)
        self._setup_graphics_flags()

    def _setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard

        self.drag_offset = QPointF(0, 0)
        
        self.staff = None
        self.ghost_arrow = None
        
        self.is_mirrored = False
        
        self.color = None
        self.motion_type = None
        self.rotation_direction = None
        self.quadrant = None
        self.start_location = None
        self.end_location = None
        self.turns = None

        self.mirror_transform = (
            None
        )

        if attributes:
            self.set_attributes_from_dict(attributes)
            self.update_appearance()
        
        self.center = self.boundingRect().center()

    def _setup_graphics_flags(self):
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def _setup_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setSelected(True)
        self.ghost_arrow = self.graphboard.ghost_arrows[self.color]
        if self.mirror_transform:
            self.ghost_arrow.setTransform(self.mirror_transform)
        self.ghost_arrow.update(self)
        self.graphboard.addItem(self.ghost_arrow)
        self.ghost_arrow.staff = self.staff
        self.graphboard.arrows.append(self.ghost_arrow)
        self.graphboard.arrows.remove(self)
        self.graphboard.arrow_positioner.update()
        self.graphboard.arrows.append(self)
        for item in self.graphboard.items():
            if item != self:
                item.setSelected(False)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            scene_event_pos = self.mapToScene(event.pos())
            view_event_pos = self.graphboard.view.mapFromScene(scene_event_pos)
            new_pos = event.scenePos() - self.center
            self.setPos(new_pos)
            in_view = self.graphboard.view.rect().contains(view_event_pos)

            scene_pos = new_pos + self.center
            new_quadrant = self.graphboard.get_quadrant(scene_pos.x(), scene_pos.y())

            if self.quadrant != new_quadrant:
                if in_view:
                    self.update_for_new_quadrant(new_quadrant)

    def mouseReleaseEvent(self, event):
        self.graphboard.removeItem(self.ghost_arrow)
        self.graphboard.arrows.remove(self.ghost_arrow)
        self.ghost_arrow.staff = None
        self.ghost_arrow = None
        self.graphboard.arrow_positioner.update()

    ### UPDATERS ###

    def update(self, attributes):
        self.set_attributes_from_dict(attributes)
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()

    def update_appearance(self):
        self.update_color()
        self.update_rotation()

    def update_color(self):
        if self.motion_type is not STATIC:
            new_svg_data = self.set_svg_color(self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)

    def update_rotation(self):
        angle = self.get_rotation_angle()
        self.setRotation(angle)

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self._setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_for_new_quadrant(self, new_quadrant):
        self.quadrant = new_quadrant

        self.attributes[QUADRANT] = new_quadrant
        self.attributes[START_LOCATION] = self.start_location
        self.attributes[END_LOCATION] = self.end_location

        self.update_rotation()
        self.ghost_arrow.update(self)

        self.start_location, self.end_location = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        self.ghost_arrow.set_attributes_from_dict(self.attributes)
        self.ghost_arrow.update_appearance()
        self.staff.set_attributes_from_arrow(self)
        self.staff.update_appearance()

        self.update_appearance()

        self.ghost_arrow.update(self)
        self.graphboard.arrows.remove(self)
        self.graphboard.update()
        self.graphboard.arrows.append(self)

    def update_staff_during_drag(self):
        for staff in self.graphboard.staff_set.values():
            if staff.color == self.color:
                if staff not in self.graphboard.staffs:
                    self.graphboard.staffs.append(staff)

                staff.set_attributes_from_dict(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                staff.arrow = self.ghost_arrow
                
                if staff not in self.graphboard.items():
                    self.graphboard.addItem(staff)
                staff.show()
                staff.update_appearance()
                self.graphboard.update_staffs()

    def set_attributes_from_dict(self, attributes):
        for attr in ARROW_ATTRIBUTES:
            value = attributes.get(attr)
            if attr == TURNS:
                value = int(value)
            setattr(self, attr, value)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            MOTION_TYPE: attributes.get(MOTION_TYPE, None),
            ROTATION_DIRECTION: attributes.get(ROTATION_DIRECTION, None),
            QUADRANT: attributes.get(QUADRANT, None),
            START_LOCATION: attributes.get(START_LOCATION, None),
            END_LOCATION: attributes.get(END_LOCATION, None),
            TURNS: attributes.get(TURNS, None),
        }

    def set_attributes_from_staff(self, staff):
        orientation = self.calculate_new_orientation(self.quadrant, staff.location)
        self.quadrant = orientation["new_quadrant"]
        self.start_location = orientation["start_location"]
        self.end_location = orientation["end_location"]

        self.update_appearance()

    def calculate_new_orientation(self, current_quadrant, new_staff_location):
        orientation_map = {
            (NORTHEAST, SOUTH): {
                "new_quadrant": SOUTHEAST,
                "start_location": EAST,
                "end_location": SOUTH,
            },
            (NORTHEAST, WEST): {
                "new_quadrant": NORTHWEST,
                "start_location": NORTH,
                "end_location": WEST,
            },
            (SOUTHEAST, NORTH): {
                "new_quadrant": NORTHEAST,
                "start_location": EAST,
                "end_location": NORTH,
            },
            (SOUTHEAST, WEST): {
                "new_quadrant": SOUTHWEST,
                "start_location": SOUTH,
                "end_location": WEST,
            },
            (SOUTHWEST, NORTH): {
                "new_quadrant": NORTHWEST,
                "start_location": WEST,
                "end_location": NORTH,
            },
            (SOUTHWEST, EAST): {
                "new_quadrant": SOUTHEAST,
                "start_location": SOUTH,
                "end_location": EAST,
            },
            (NORTHWEST, SOUTH): {
                "new_quadrant": SOUTHWEST,
                "start_location": WEST,
                "end_location": SOUTH,
            },
            (NORTHWEST, EAST): {
                "new_quadrant": NORTHEAST,
                "start_location": NORTH,
                "end_location": EAST,
            },
        }

        # Use the mapping to find the new orientation
        return orientation_map.get(
            (current_quadrant, new_staff_location),
            {"new_quadrant": None, "start_location": None, "end_location": None},
        )

    def set_transform_origin_to_center(self):
        # Call this method after any changes that might affect the boundingRect.
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)


    ### GETTERS ###

    def get_svg_data(self, svg_file):
        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_rotation_angle(self, arrow=None):
        arrow = arrow or self
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            arrow.motion_type, arrow.rotation_direction
        )
        return quadrant_to_angle.get(arrow.quadrant, 0)

    def get_quadrant_to_angle_map(self, motion_type, rotation_direction):
        if motion_type == PRO:
            return {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})
        elif motion_type == ANTI:
            return {
                CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            }.get(rotation_direction, {})
        elif motion_type == STATIC:
            return {
                CLOCKWISE: {NORTHEAST: 0, SOUTHEAST: 0, SOUTHWEST: 0, NORTHWEST: 0},
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in ARROW_ATTRIBUTES}

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        return (
            start_end_location_mapping.get(quadrant, {})
            .get(rotation_direction, {})
            .get(motion_type, (None, None))
        )

    def get_svg_file(self, motion_type, turns):
        svg_file = f"{ARROW_DIR}{motion_type}_{turns}.svg"
        return svg_file


    ### MANIPULATION ###

    def increment_turns(self):
        self.turns += 1
        if self.turns > 2:
            self.turns = 0
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.attributes[TURNS] = self.turns
        self.graphboard.update()

    def decrement_turns(self):
        self.turns -= 1
        if self.turns < 0:
            self.turns = 2
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.attributes[TURNS] = self.turns
        self.graphboard.update()

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

    def move_wasd(self, direction):
        wasd_quadrant_mapping = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
        }
        current_quadrant = self.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(
            current_quadrant, current_quadrant
        )
        self.quadrant = new_quadrant
        (
            new_start_location,
            new_end_location,
        ) = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.turns,
        }

        updated_staff_dict = {
            COLOR: self.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update(updated_arrow_dict)
        self.staff.update(updated_staff_dict)

        self.graphboard.update()

    def rotate(self, rotation_direction):
        quadrants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        current_quadrant_index = quadrants.index(self.quadrant)
        new_quadrant_index = (
            (current_quadrant_index + 1) % 4
            if rotation_direction == RIGHT
            else (current_quadrant_index - 1) % 4
        )
        new_quadrant = quadrants[new_quadrant_index]
        (
            new_start_location,
            new_end_location,
        ) = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.turns,
        }

        updated_staff_dict = {
            COLOR: self.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update(updated_arrow_dict)
        self.staff.update(updated_staff_dict)
        self.graphboard.update()

    def mirror(self):
        if self.is_mirrored:
            self.is_mirrored = False
        elif not self.is_mirrored:
            self.is_mirrored = True

        center_x = self.boundingRect().width() / 2
        center_y = self.boundingRect().height() / 2

        if self.is_mirrored:
            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.scale(-1, 1)
            transform.translate(-center_x, -center_y)

        if not self.is_mirrored:
            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.scale(1, 1)
            transform.translate(-center_x, -center_y)

        self.setTransform(transform)
        self.mirror_transform = transform

        if self.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.rotation_direction == "None":
            new_rotation_direction = "None"

        old_start_location = self.start_location
        old_end_location = self.end_location
        new_start_location = old_end_location
        new_end_location = old_start_location

        new_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: self.quadrant,
            ROTATION_DIRECTION: new_rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.turns,
        }

        new_staff_dict = {
            COLOR: self.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update(new_arrow_dict)
        self.staff.update(new_staff_dict)

        if self.ghost_arrow:
            self.ghost_arrow.setTransform(transform)
            self.ghost_arrow.mirror_transform = transform
            self.ghost_arrow.update(self)

        self.graphboard.update()

    def swap_motion_type(self):
        if self.motion_type == ANTI:
            new_motion_type = PRO
        elif self.motion_type == PRO:
            new_motion_type = ANTI
        elif self.motion_type == STATIC:
            new_motion_type = STATIC

        if self.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.rotation_direction == "None":
            new_rotation_direction = "None"

        new_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: new_motion_type,
            QUADRANT: self.quadrant,
            ROTATION_DIRECTION: new_rotation_direction,
            START_LOCATION: self.start_location,
            END_LOCATION: self.end_location,
            TURNS: self.turns,
        }

        new_staff_dict = {
            COLOR: self.color,
            LOCATION: self.end_location,
            LAYER: 1,
        }

        self.svg_file = f"resources/images/arrows/{new_motion_type}_{self.turns}.svg"
        self._setup_svg_renderer(self.svg_file)
        self.update(new_arrow_dict)
        self.staff.update(new_staff_dict)
        self.graphboard.update()


class BlankArrow(Arrow):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self._disable_interactivity()
        self.hide()

    def _disable_interactivity(self):
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
