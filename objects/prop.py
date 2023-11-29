from objects.graphical_object import GraphicalObject
from PyQt6.QtCore import Qt, QPointF
from settings.string_constants import *
import re

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from utilities.TypeChecking.TypeChecking import (
    Layers,
    Orientations,
    PropTypes,
    RotationAngles,
    PropAttributesDicts,
    Locations,
    Locations,
    RotationDirections,
    MotionTypes,
    Axes,
    Colors,
    TYPE_CHECKING,
    Dict,
    Tuple,
    ColorsHex,
)

if TYPE_CHECKING:
    from objects.arrow import Arrow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from objects.motion import Motion
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox
    from objects.arrow import StaticArrow


class Prop(GraphicalObject):
    def __init__(self, scene, attributes: Dict) -> None:
        svg_file = self.get_svg_file(attributes[PROP_TYPE])
        super().__init__(svg_file, scene)
        self._setup_attributes(scene, attributes)
        self.update_appearance()

    def _setup_attributes(self, scene, attributes: "PropAttributesDicts") -> None:
        self.scene: Pictograph | PropBox = scene
        self.motion: Motion = None
        self.prop_type: PropTypes = None

        self.drag_offset = QPointF(0, 0)
        self.previous_location: Locations = None
        self.arrow: Arrow = None
        self.static_arrow: StaticArrow = None
        self.ghost_prop: Prop = None

        self.color: Colors = attributes[COLOR]
        self.prop_location: Locations = attributes[PROP_LOCATION]
        self.layer: Layers = attributes[LAYER]
        self.orientation: Orientations = attributes[ORIENTATION]

        self.axis: Axes = self.update_axis(self.prop_location)
        self.center = self.boundingRect().center()
        self.update_rotation()

        if attributes:
            self.update_attributes(attributes)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.setSelected(True)
        if isinstance(self.scene, self.scene.__class__):
            if not self.ghost_prop:
                self.ghost_prop = self.scene.ghost_props[self.color]
            self.ghost_prop.color = self.color
            self.ghost_prop.prop_location = self.prop_location
            self.ghost_prop.layer = self.layer
            self.ghost_prop.orientation = self.orientation
            self.ghost_prop.update_appearance()
            self.scene.addItem(self.ghost_prop)
            self.ghost_prop.arrow = self.arrow
            self.scene.props.append(self.ghost_prop)
            self.scene.props.remove(self)
            self.scene.update_pictograph()
            self.scene.props.append(self)
            for item in self.scene.items():
                if item != self:
                    item.setSelected(False)
            self.previous_location = self.prop_location

    def update_location(self, new_pos: QPointF) -> None:
        new_location = self.get_closest_diamond_point(new_pos)

        if new_location != self.previous_location:
            self.prop_location = new_location
            from objects.arrow import StaticArrow

            if isinstance(self.arrow, StaticArrow):
                self.arrow.start_location = new_location
                self.arrow.end_location = new_location
                self.motion.arrow_location = new_location
                self.motion.start_location = new_location
                self.motion.end_location = new_location
            self.axis = self.update_axis(self.prop_location)
            self.update_appearance()
            self.update_arrow_location(new_location)

            self.ghost_prop.arrow.end_location, self.ghost_prop.arrow.start_location = (
                new_location,
                new_location,
            )
            self.ghost_prop.color = self.color
            self.ghost_prop.prop_location = self.prop_location
            self.ghost_prop.layer = self.layer
            self.ghost_prop.update_appearance()

            self.scene.props.remove(self)
            if self.arrow.motion_type == STATIC:
                self.arrow.start_location = new_location
                self.arrow.end_location = new_location

            self.scene.update_pictograph()
            self.scene.props.append(self)
            new_pos = new_pos - self.get_object_center()
            self.set_drag_pos(new_pos)
            self.previous_location = new_location

    def set_drag_pos(self, new_pos: QPointF) -> None:
        object_length = self.boundingRect().width()
        object_width = self.boundingRect().height()

        offset = self.get_offset(object_length, object_width)

        self.setPos(new_pos + offset)

    def get_offset(self, prop_length, prop_width) -> Tuple[int, int]:
        # Layers 1 logic
        if self.layer == 1:
            if self.orientation == IN:
                offset_map = {
                    NORTH: (prop_width, 0),
                    SOUTH: (0, prop_length),
                    WEST: (0, 0),
                    EAST: (prop_length, prop_width),
                }
            else:  # OUT
                offset_map = {
                    NORTH: (0, prop_length),
                    SOUTH: (prop_width, 0),
                    WEST: (prop_length, prop_width),
                    EAST: (0, 0),
                }

        # Layers 2 logic
        elif self.layer == 2:
            if self.orientation == CLOCKWISE:
                offset_map = {
                    NORTH: (0, 0),
                    SOUTH: (prop_length, prop_width),
                    WEST: (0, prop_length),
                    EAST: (prop_width, 0),
                }
            else:  # COUNTER_CLOCKWISE
                offset_map = {
                    NORTH: (prop_length, prop_width),
                    SOUTH: (0, 0),
                    WEST: (prop_width, 0),
                    EAST: (0, prop_length),
                }

        offset_tuple = offset_map.get(self.prop_location, (0, 0))
        return QPointF(offset_tuple[0], offset_tuple[1])

    def update_arrow_location(self, new_location: Locations) -> None:
        if self.arrow.motion_type in [PRO, ANTI]:
            shift_location_mapping: Dict[
                Tuple(Locations, RotationDirections, MotionTypes),
                Dict[Locations, Locations],
            ] = {
                ### ISO ###
                (NORTHEAST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
                (NORTHWEST, CLOCKWISE, PRO): {EAST: NORTHEAST, WEST: SOUTHWEST},
                (SOUTHWEST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
                (SOUTHEAST, CLOCKWISE, PRO): {WEST: SOUTHWEST, EAST: NORTHEAST},
                (NORTHEAST, COUNTER_CLOCKWISE, PRO): {WEST: NORTHWEST, EAST: SOUTHEAST},
                (NORTHWEST, COUNTER_CLOCKWISE, PRO): {
                    SOUTH: SOUTHWEST,
                    NORTH: NORTHEAST,
                },
                (SOUTHWEST, COUNTER_CLOCKWISE, PRO): {EAST: SOUTHEAST, WEST: NORTHWEST},
                (SOUTHEAST, COUNTER_CLOCKWISE, PRO): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                ### ANTI ###
                (NORTHEAST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
                (NORTHWEST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
                (SOUTHWEST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
                (SOUTHEAST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
                (NORTHEAST, COUNTER_CLOCKWISE, ANTI): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (NORTHWEST, COUNTER_CLOCKWISE, ANTI): {
                    WEST: SOUTHWEST,
                    EAST: NORTHEAST,
                },
                (SOUTHWEST, COUNTER_CLOCKWISE, ANTI): {
                    SOUTH: SOUTHEAST,
                    NORTH: NORTHWEST,
                },
                (SOUTHEAST, COUNTER_CLOCKWISE, ANTI): {
                    EAST: NORTHEAST,
                    WEST: SOUTHWEST,
                },
            }

            current_location = self.arrow.arrow_location
            rotation_direction = self.arrow.rotation_direction
            motion_type = self.arrow.motion_type
            new_location = shift_location_mapping.get(
                (current_location, rotation_direction, motion_type), {}
            ).get(new_location)

            if new_location:
                self.arrow.arrow_location = new_location
                start_location, end_location = self.arrow.get_start_end_locations(
                    motion_type, rotation_direction, new_location
                )
                self.arrow.start_location = start_location
                self.arrow.end_location = end_location
                self.arrow.update_appearance()
        elif self.arrow.motion_type == STATIC:
            self.arrow.arrow_location = new_location
            self.arrow.start_location = new_location
            self.arrow.end_location = new_location
            self.arrow.update_appearance()

    def mouseReleaseEvent(self, event) -> None:
        if isinstance(self.scene, self.scene.__class__):
            self.scene.removeItem(self.ghost_prop)
            self.scene.props.remove(self.ghost_prop)
            self.ghost_prop.arrow = None
            self.scene.update_pictograph()
            self.finalize_prop_drop(event)

    def finalize_prop_drop(self, event: "QGraphicsSceneMouseEvent") -> None:
        closest_handpoint = self.get_closest_handpoint(event.scenePos())
        new_location = self.get_closest_diamond_point(event.scenePos())

        self.prop_location = new_location
        self.axis = self.update_axis(self.prop_location)
        self.update_appearance()
        self.setPos(closest_handpoint)

        if self.arrow:
            self.arrow.update_appearance()
        self.previous_location = new_location
        self.scene.update_pictograph()

    ### UPDATERS ###

    def update_appearance(self) -> None:
        self.axis = self.update_axis(self.prop_location)
        super().update_appearance()

    def set_prop_transform_origin_to_center(self: "Prop") -> None:
        self.center = self.get_object_center()
        self.setTransformOriginPoint(self.center)

    def set_prop_attrs_from_arrow(self, target_arrow: "Arrow") -> None:
        self.color = target_arrow.color
        self.prop_location = target_arrow.end_location
        self.axis = self.update_axis(self.prop_location)
        self.update_appearance()

    ### GETTERS ###

    def update_axis(self, location) -> Axes:
        if self.layer == 1:
            self.axis: Axes = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis: Axes = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        return self.axis

    def get_rotation_angle(self) -> RotationAngles:
        angle_map: Dict[
            Tuple[Layers, Orientations], Dict[Locations, RotationAngles]
        ] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }

        key = (self.layer, self.orientation)
        return angle_map.get(key, {}).get(
            self.prop_location, 0
        )  # Default to 0 if not found

    def get_attributes(self) -> PropAttributesDicts:
        return {attr: getattr(self, attr) for attr in PROP_ATTRIBUTES}

    def update_rotation(self) -> None:
        rotation_angle = self.get_rotation_angle()

        if self.ghost_prop:
            self.ghost_prop.setRotation(rotation_angle)
        self.setRotation(rotation_angle)

    def get_closest_handpoint(self, mouse_pos: QPointF) -> QPointF:
        closest_distance = float("inf")
        closest_handpoint = None
        for point in self.scene.grid.handpoints.values():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_handpoint = point
        return closest_handpoint

    def get_closest_diamond_point(self, mouse_pos: QPointF) -> Locations:
        closest_distance = float("inf")
        closest_location = None
        for location, point in self.scene.grid.handpoints.items():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_location = location
        return closest_location

    def get_svg_file(self, prop_type: PropTypes) -> str:
        svg_file = f"{PROP_DIR}{prop_type}.svg"
        return svg_file

    ### HELPERS ###

    def swap_axis(self) -> None:
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.update_rotation()

    def swap_layer(self) -> None:
        if self.layer == 1:
            self.layer = 2
        else:
            self.layer = 1
        self.update_rotation()

    def set_svg_color(self, new_color: Colors) -> bytes:
        new_hex_color: ColorsHex = COLOR_MAP.get(new_color)

        with open(self.svg_file, "r") as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_hex_color: ColorsHex = match.group(1)
            svg_data = svg_data.replace(old_hex_color, new_hex_color)
        return svg_data.encode("utf-8")

    def delete(self) -> None:
        self.scene.removeItem(self)
        self.scene.props.remove(self)
        self.scene.update_pictograph()

    def _create_static_arrow(self) -> None:
        static_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            ARROW_LOCATION: self.prop_location,
            START_LOCATION: self.prop_location,
            END_LOCATION: self.prop_location,
            TURNS: 0,
        }

        self.static_arrow = StaticArrow(self.pictograph, static_arrow_dict)
        for arrow in self.pictograph.arrows[:]:
            if arrow.color == self.color:
                self.pictograph.removeItem(arrow)
                self.pictograph.arrows.remove(arrow)
        self.pictograph.addItem(self.static_arrow)
        self.pictograph.arrows.append(self.static_arrow)
        self.static_arrow.prop = self.ghost_prop
        self.static_arrow.prop.arrow = self.static_arrow

        if self.static_arrow not in self.pictograph.items():
            self.pictograph.addItem(self.static_arrow)

class Staff(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = STAFF
        super().__init__(pictograph, attributes)


class Triad(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = TRIAD
        super().__init__(pictograph, attributes)


class Hoop(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = HOOP
        super().__init__(pictograph, attributes)


class Fan(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = FAN
        super().__init__(pictograph, attributes)


class Club(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = CLUB
        super().__init__(pictograph, attributes)


class Buugeng(Prop):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = BUUGENG
        super().__init__(pictograph, attributes)
