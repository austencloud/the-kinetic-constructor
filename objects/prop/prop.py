from typing import TYPE_CHECKING, Dict, Tuple, Union
from Enums import PropAttribute

from data.start_end_loc_map import get_start_end_locs
from objects.graphical_object import GraphicalObject
from PyQt6.QtCore import QPointF, Qt
from constants import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from utilities.TypeChecking.TypeChecking import (
    Axes,
    Colors,
    Locations,
    MotionTypes,
    Orientations,
    PropRotDirs,
    RotationAngles,
)
from utilities.TypeChecking.prop_types import PropTypes


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from objects.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import (
        PropBox,
    )


class Prop(GraphicalObject):
    def __init__(self, scene, prop_dict: Dict, motion: "Motion") -> None:
        self.motion = motion
        self.arrow: Arrow = None

        self.prop_type = prop_dict[PROP_TYPE]
        self.svg_file = self.get_svg_file(self.prop_type)
        self.ghost: Prop = None
        super().__init__(scene)
        self._setup_attributes(scene, prop_dict)
        self.setup_svg_renderer(self.svg_file)
        self.setZValue(10)

    def _setup_attributes(self, scene, prop_dict: Dict) -> None:
        self.scene: Pictograph | PropBox = scene
        self.drag_offset = QPointF(0, 0)
        self.previous_location: Locations = None
        self.is_ghost: bool = False
        self.axis: Axes = None
        self.color: Colors = prop_dict[COLOR]
        self.loc: Locations = prop_dict[LOC]
        self.ori: Orientations = prop_dict[ORIENTATION]
        self.center = self.boundingRect().center()

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.setSelected(True)
        if isinstance(self.scene, self.scene.__class__):
            if not self.ghost:
                self.ghost = self.scene.ghost_props[self.color]
            self.ghost.color = self.color
            self.ghost.loc = self.loc
            self.ghost.ori = self.ori
            self.ghost.update_prop()
            self.ghost.show()
            self.scene.props[self.ghost.color] = self.ghost
            self.scene.props[self.color] = self.ghost
            self.scene.update_pictograph()
            self.scene.props[self.color] = self
            for item in self.scene.items():
                if item != self:
                    item.setSelected(False)
            self.previous_location = self.loc

    def mouseMoveEvent(
        self: Union["Prop", "Arrow"], event: "QGraphicsSceneMouseEvent"
    ) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.get_object_center()
            self.set_drag_pos(new_pos)
            self.update_ghost_prop_location(event.scenePos())
            self.update_arrow_location(self.loc)

    def mouseReleaseEvent(self, event) -> None:
        if isinstance(self.scene, self.scene.__class__):
            self.ghost.hide()
            self.scene.update_pictograph()
            self.finalize_prop_drop(event)

    ### UPDATERS ###

    def set_prop_transform_origin_to_center(self: "Prop") -> None:
        self.center = self.get_object_center()
        self.setTransformOriginPoint(self.center)

    def clear_attributes(self) -> None:
        self.loc = None
        self.layer = None
        self.ori = None
        self.axis = None
        self.motion = None
        self.update_prop()

    ### GETTERS ###

    def get_axis_from_ori(self) -> None:
        if self.is_radial():
            axis: Axes = VERTICAL if self.loc in [NORTH, SOUTH] else HORIZONTAL
        elif self.is_antiradial():
            axis: Axes = HORIZONTAL if self.loc in [NORTH, SOUTH] else VERTICAL
        else:
            axis: Axes = None
        return axis

    def swap_ori(self) -> None:
        ori_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        self.ori = ori_map[self.ori]

    def get_rotation_angle(self) -> RotationAngles:
        angle_map: Dict[Orientations, Dict[Locations, RotationAngles]] = {
            IN: {
                NORTH: 90,
                SOUTH: 270,
                WEST: 0,
                EAST: 180,
            },
            OUT: {
                NORTH: 270,
                SOUTH: 90,
                WEST: 180,
                EAST: 0,
            },
            CLOCK: {
                NORTH: 0,
                SOUTH: 180,
                WEST: 270,
                EAST: 90,
            },
            COUNTER: {
                NORTH: 180,
                SOUTH: 0,
                WEST: 90,
                EAST: 270,
            },
        }

        key = self.ori
        rotation_angle = angle_map.get(key, {}).get(self.loc, 0)
        return rotation_angle

    def get_attributes(self) -> Dict[str, Union[Colors, Locations, Orientations]]:
        prop_attributes = [attr.value for attr in PropAttribute]
        return {attr: getattr(self, attr) for attr in prop_attributes}

    def _update_prop_rotation_angle(self) -> None:
        prop_rotation_angle = self.get_rotation_angle()
        if self.ghost:
            self.ghost.setRotation(prop_rotation_angle)
        self.setRotation(prop_rotation_angle)

    def update_prop(
        self, prop_dict: Dict[str, Union[Colors, Locations, Orientations]] = None
    ) -> None:
        if prop_dict:
            for key, value in prop_dict.items():
                setattr(self, key, value)
        self.motion.update_prop_ori()
        self.update_svg()
        self._update_color()
        self._update_prop_rotation_angle()

    def update_svg(self) -> None:
        self.svg_file = self.get_svg_file(self.prop_type)
        super().update_svg(self.svg_file)

    def get_svg_file(self, prop_type: PropTypes) -> str:
        svg_file = f"{PROP_DIR}{prop_type}.svg"
        return svg_file

    ### UPDATERS ###

    def update_prop_type(self, prop_type: PropTypes) -> None:
        self.prop_type = prop_type
        self.update_svg()
        self.update_prop()

    def update_ghost_prop_location(self, new_pos: QPointF) -> None:
        new_location = self.pictograph.get_closest_hand_point(new_pos)[0][0]

        if new_location != self.previous_location:
            self.loc = new_location

            if self.motion.motion_type == STATIC:
                self.motion.arrow.loc = new_location
                self.motion.start_loc = new_location
                self.motion.end_loc = new_location

            self.axis = self.get_axis_from_ori()
            self.update_prop()
            self.update_arrow_location(new_location)

            self.ghost.color = self.color
            self.ghost.loc = self.loc
            self.ghost.update_prop()
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
        if self.ori == IN:
            offset_map = {
                NORTH: (prop_width, 0),
                SOUTH: (0, prop_length),
                WEST: (0, 0),
                EAST: (prop_length, prop_width),
            }
        elif self.ori == OUT:
            offset_map = {
                NORTH: (0, prop_length),
                SOUTH: (prop_width, 0),
                WEST: (prop_length, prop_width),
                EAST: (0, 0),
            }
        elif self.ori == CLOCK:
            offset_map = {
                NORTH: (0, 0),
                SOUTH: (prop_length, prop_width),
                WEST: (0, prop_length),
                EAST: (prop_width, 0),
            }
        elif self.ori == COUNTER:
            offset_map = {
                NORTH: (prop_length, prop_width),
                SOUTH: (0, 0),
                WEST: (prop_width, 0),
                EAST: (0, prop_length),
            }

        offset_tuple = offset_map.get(self.loc, (0, 0))
        return QPointF(offset_tuple[0], offset_tuple[1])

    def update_arrow_location(self, new_arrow_location: Locations) -> None:
        if self.motion.motion_type in [PRO, ANTI]:
            shift_location_map: Dict[
                Tuple(Locations, PropRotDirs, MotionTypes),
                Dict[Locations, Locations],
            ] = {
                ### ISO ###
                (NORTHEAST, CLOCKWISE, PRO): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (NORTHWEST, CLOCKWISE, PRO): {
                    EAST: NORTHEAST,
                    WEST: SOUTHWEST,
                },
                (SOUTHWEST, CLOCKWISE, PRO): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (SOUTHEAST, CLOCKWISE, PRO): {
                    WEST: SOUTHWEST,
                    EAST: NORTHEAST,
                },
                (
                    NORTHEAST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    WEST: NORTHWEST,
                    EAST: SOUTHEAST,
                },
                (
                    NORTHWEST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    SOUTH: SOUTHWEST,
                    NORTH: NORTHEAST,
                },
                (
                    SOUTHWEST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (
                    SOUTHEAST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                ### ANTI ###
                (NORTHEAST, CLOCKWISE, ANTI): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (NORTHWEST, CLOCKWISE, ANTI): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                (SOUTHWEST, CLOCKWISE, ANTI): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (SOUTHEAST, CLOCKWISE, ANTI): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                (
                    NORTHEAST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (
                    NORTHWEST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    WEST: SOUTHWEST,
                    EAST: NORTHEAST,
                },
                (
                    SOUTHWEST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    SOUTH: SOUTHEAST,
                    NORTH: NORTHWEST,
                },
                (
                    SOUTHEAST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    EAST: NORTHEAST,
                    WEST: SOUTHWEST,
                },
            }

            current_arrow_location = self.motion.arrow.loc
            rot_dir = self.motion.prop_rot_dir
            motion_type = self.motion.motion_type
            new_arrow_location = shift_location_map.get(
                (current_arrow_location, rot_dir, motion_type), {}
            ).get(new_arrow_location)

            if new_arrow_location:
                start_loc, end_loc = get_start_end_locs(
                    motion_type, rot_dir, new_arrow_location
                )

                self.motion.arrow.loc = new_arrow_location
                self.motion.arrow.ghost.loc = new_arrow_location
                self.motion.start_loc = start_loc
                self.motion.end_loc = end_loc
                self.motion.arrow.update_arrow()
                self.motion.arrow.ghost.update_arrow()
                self.pictograph.update_pictograph()

        elif self.motion.motion_type == STATIC:
            self.motion.arrow.loc = new_arrow_location
            self.motion.start_loc = new_arrow_location
            self.motion.end_loc = new_arrow_location
            self.motion.arrow.update_arrow()

    def finalize_prop_drop(self, event: "QGraphicsSceneMouseEvent") -> None:
        (
            closest_hand_point,
            closest_hand_point_coord,
        ) = self.pictograph.get_closest_hand_point(event.scenePos())

        self.loc = closest_hand_point
        self.axis = self.get_axis_from_ori()
        self.update_prop()
        self.setPos(closest_hand_point_coord)

        if self.motion.arrow:
            self.motion.arrow.update_arrow()
        self.previous_location = closest_hand_point
        self.scene.update_pictograph()

    def is_radial(self) -> bool:
        return self.ori in [IN, OUT]

    def is_antiradial(self) -> bool:
        return self.ori in [CLOCK, COUNTER]
