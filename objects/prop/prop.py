from typing import Union
from data.start_end_location_map import get_start_end_locations
from objects.graphical_object import GraphicalObject
from PyQt6.QtCore import QPointF, Qt
from constants.string_constants import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from objects.prop.prop_manipulator import PropManipulator
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
)

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from objects.motion import Motion
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox


class Prop(GraphicalObject):
    def __init__(self, scene, prop_dict: Dict, motion: "Motion") -> None:
        self.motion = motion
        self.prop_type = prop_dict[PROP_TYPE]
        self.svg_file = self.get_svg_file(self.prop_type)
        super().__init__(scene)
        self.setup_svg_renderer(self.svg_file)
        self._setup_attributes(scene, prop_dict)

    def _setup_attributes(self, scene, prop_dict: "PropAttributesDicts") -> None:
        self.scene: Pictograph | PropBox = scene
        self.manipulator = PropManipulator(self)
        self.drag_offset = QPointF(0, 0)
        self.previous_location: Locations = None
        self.ghost: Prop = None
        self.color: Colors = prop_dict[COLOR]
        self.location: Locations = prop_dict[LOCATION]
        self.layer: Layers = prop_dict[LAYER]
        self.orientation: Orientations = prop_dict[ORIENTATION]
        self.center = self.boundingRect().center()

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.setSelected(True)
        if isinstance(self.scene, self.scene.__class__):
            if not self.ghost:
                self.ghost = self.scene.ghost_props[self.color]
            self.ghost.color = self.color
            self.ghost.location = self.location
            self.ghost.layer = self.layer
            self.ghost.orientation = self.orientation
            self.ghost.update_appearance()
            self.scene.addItem(self.ghost)
            self.scene.props[self.ghost.color] = self.ghost
            self.scene.props[self.color] = self.ghost
            self.scene.update_pictograph()
            self.scene.props[self.color] = self
            for item in self.scene.items():
                if item != self:
                    item.setSelected(False)
            self.previous_location = self.location

    def mouseReleaseEvent(self, event) -> None:
        if isinstance(self.scene, self.scene.__class__):
            self.scene.removeItem(self.ghost)
            self.ghost.arrow = None
            self.scene.update_pictograph()
            self.finalize_prop_drop(event)

    ### UPDATERS ###

    def set_prop_transform_origin_to_center(self: "Prop") -> None:
        self.center = self.get_object_center()
        self.setTransformOriginPoint(self.center)

    def set_prop_attrs_from_arrow(self, target_arrow: "Arrow") -> None:
        self.color = target_arrow.color
        self.location = target_arrow.motion.end_location
        self.axis = self.update_axis_from_layer(self.location)
        self.update_appearance()

    def clear_attributes(self) -> None:
        self.location = None
        self.layer = None
        self.orientation = None
        self.axis = None
        self.update_appearance()

    ### GETTERS ###

    def update_axis_from_layer(self, location) -> None:
        if self.layer == 1:
            self.axis: Axes = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis: Axes = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL

    def swap_orientation(self, orientation) -> None:
        if orientation == IN:
            orientation = OUT
        elif orientation == OUT:
            orientation = IN
        elif orientation == CLOCKWISE:
            orientation = COUNTER_CLOCKWISE
        elif orientation == COUNTER_CLOCKWISE:
            orientation = CLOCKWISE

        self.update_rotation()
        return orientation

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
        rotation_angle = angle_map.get(key, {}).get(self.location, 0)
        return rotation_angle

    def get_attributes(self) -> PropAttributesDicts:
        return {attr: getattr(self, attr) for attr in PROP_ATTRIBUTES}

    def update_rotation(self) -> None:
        rotation_angle = self.get_rotation_angle()

        if self.ghost:
            self.ghost.setRotation(rotation_angle)
        self.setRotation(rotation_angle)

    def get_svg_file(self, prop_type: PropTypes) -> str:
        svg_file = f"{PROP_DIR}{prop_type}.svg"
        return svg_file

    ### UPDATERS ###

    def update_prop_type(self, prop_type: PropTypes) -> None:
        self.prop_type = prop_type
        self.update_svg(self.get_svg_file(prop_type))
        self.update_appearance()

    def update_ghost_prop_location(self, new_pos: QPointF) -> None:
        new_location = self.pictograph.get_closest_hand_point(new_pos)[0]

        if new_location != self.previous_location:
            self.location = new_location

            if self.motion.motion_type == STATIC:
                self.motion.arrow_location = new_location
                self.motion.start_location = new_location
                self.motion.end_location = new_location

            self.axis = self.update_axis_from_layer(self.location)
            self.update_appearance()
            self.update_arrow_location(new_location)

            self.ghost.color = self.color
            self.ghost.location = self.location
            self.ghost.layer = self.layer
            self.ghost.update_appearance()
            self.scene.props[self.ghost.color] = self.ghost
            self.scene.update_pictograph()
            self.scene.props[self.color] = self
            new_pos = new_pos - self.get_object_center()
            self.set_drag_pos(new_pos)
            self.previous_location = new_location

    ### HELPERS ###

    def set_drag_pos(self, new_pos: QPointF) -> None:
        object_length = self.boundingRect().width()
        object_width = self.boundingRect().height()

        offset = self.get_offset(object_length, object_width)

        self.setPos(new_pos + offset)

    ### GETTERS ###

    def get_offset(self, prop_length, prop_width) -> Tuple[int, int]:
        # Layer 1 logic
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

        # Layer 2 logic
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

        offset_tuple = offset_map.get(self.location, (0, 0))
        return QPointF(offset_tuple[0], offset_tuple[1])

    def update_arrow_location(self, new_arrow_location: Locations) -> None:
        if self.motion.motion_type in [PRO, ANTI]:
            shift_location_map: Dict[
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

            current_arrow_location = self.motion.arrow_location
            rotation_direction = self.motion.rotation_direction
            motion_type = self.motion.motion_type
            new_arrow_location = shift_location_map.get(
                (current_arrow_location, rotation_direction, motion_type), {}
            ).get(new_arrow_location)

            if new_arrow_location:
                start_location, end_location = get_start_end_locations(
                    motion_type, rotation_direction, new_arrow_location
                )
                self.motion.arrow.update_appearance()
                self.motion.arrow.ghost.update_appearance()
                self.motion.arrow.motion.arrow_location = new_arrow_location
                self.motion.arrow.motion.start_location = start_location
                self.motion.arrow.motion.end_location = end_location
                self.pictograph.update_pictograph()

        elif self.motion.arrow.motion_type == STATIC:
            self.motion.arrow.motion.arrow_location = new_arrow_location
            self.motion.arrow.motion.start_location = new_arrow_location
            self.motion.arrow.motion.end_location = new_arrow_location
            self.motion.arrow.update_appearance()

    def finalize_prop_drop(self, event: "QGraphicsSceneMouseEvent") -> None:
        (
            closest_hand_point,
            closest_hand_point_coord,
        ) = self.pictograph.get_closest_hand_point(event.scenePos())

        self.location = closest_hand_point
        self.axis = self.update_axis_from_layer(self.location)
        self.update_appearance()
        self.setPos(closest_hand_point_coord)

        if self.motion.arrow:
            self.motion.arrow.update_appearance()
        self.previous_location = closest_hand_point
        self.scene.update_pictograph()

    def mouseMoveEvent(
        self: Union["Prop", "Arrow"], event: "QGraphicsSceneMouseEvent"
    ) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.get_object_center()
            self.set_drag_pos(new_pos)
            self.update_ghost_prop_location(event.scenePos())
            self.update_arrow_location(self.location)
