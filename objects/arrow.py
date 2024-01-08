from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *
from objects.prop.prop import Prop

from objects.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LeadStates,
    Locations,
    MotionTypes,
    PropRotDirs,
    Turns,
    RotationAngles,
    TYPE_CHECKING,
    Optional,
    Dict,
)


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion
    from objects.ghosts.ghost_arrow import GhostArrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )


class Arrow(GraphicalObject):
    def __init__(self, scene, arrow_dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.motion = motion

        self.svg_file = self.get_svg_file(
            arrow_dict[MOTION_TYPE],
            arrow_dict[TURNS],
        )
        self.setup_svg_renderer(self.svg_file)
        self.setAcceptHoverEvents(True)
        self.update_attributes(arrow_dict)

        self.prop: Prop = None
        self.scene: Pictograph | ArrowBox = scene
        self.is_svg_mirrored: bool = False
        self.is_dragging: bool = False
        self.ghost: GhostArrow = None
        self.loc: Locations = None
        self.is_ghost: bool = False
        self.drag_offset = QPointF(0, 0)
        self.lead_state: LeadStates = None

    ### SETUP ###

    def update_svg(self, svg_file: str = None) -> None:
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.svg_file = svg_file
        super().update_svg(svg_file)
        if not self.is_ghost and self.ghost:
            self.ghost.update_svg(svg_file)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)

        self.pictograph.clear_selections()
        self.setSelected(True)

        if hasattr(self, GHOST) and self.ghost:
            self.ghost.show()

        self.update_arrow()
        self.prop.update_prop()
        self.scene.update_pictograph()

    def mouseMoveEvent(
        self: Union["Prop", "Arrow"], event: "QGraphicsSceneMouseEvent"
    ) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_location = self.scene.get_closest_layer2_point(event.scenePos())[0]
            new_pos = event.scenePos() - self.get_object_center()
            self.set_drag_pos(new_pos)
            if new_location != self.loc:
                self._update_location(new_location)

    def mouseReleaseEvent(self, event) -> None:
        self.is_dragging = False
        self.scene.arrows[self.color] = self
        self.scene.update_pictograph()
        self.ghost.hide()

    ### UPDATERS ###

    def _update_location(self) -> None:
        if not self.is_ghost and self.ghost:
            if not self.loc:
                loc = self.motion.arrow_location_manager.get_arrow_location(
                    self.motion.start_loc, self.motion.end_loc, self.motion_type
                )
                self.loc = loc
                self.ghost.loc = loc
                self.is_dragging = True

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def _update_mirror(self) -> None:
        if self.motion_type == PRO:
            rot_dir = self.motion.prop_rot_dir
            if rot_dir == CLOCKWISE:
                self.is_svg_mirrored = False
            elif rot_dir == COUNTER_CLOCKWISE:
                self.is_svg_mirrored = True
        elif self.motion_type == ANTI:
            rot_dir = self.motion.prop_rot_dir
            if rot_dir == CLOCKWISE:
                self.is_svg_mirrored = True
            elif rot_dir == COUNTER_CLOCKWISE:
                self.is_svg_mirrored = False
        elif self.motion_type == DASH:
            if self.turns > 0:
                if self.motion.prop_rot_dir == CLOCKWISE:
                    self.is_svg_mirrored = False
                elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    self.is_svg_mirrored = True
            else:
                self.is_svg_mirrored = False
        elif self.motion_type == STATIC:
            if self.turns > 0:
                if self.motion.prop_rot_dir == CLOCKWISE:
                    self.is_svg_mirrored = False
                elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    self.is_svg_mirrored = True
            else:
                self.is_svg_mirrored = False

        if self.is_svg_mirrored:
            self.mirror_svg()
            if not self.is_ghost:
                self.ghost.mirror_svg()
        else:
            self.unmirror_svg()
            if not self.is_ghost:
                self.ghost.unmirror_svg()

    def _update_rotation(self) -> None:
        if self.motion.is_shift():
            angle = self._get_shift_rotation_angle()
        elif self.motion.is_dash():
            angle = self._get_dash_rotation_angle()
        elif self.motion.is_static():
            angle = self._get_static_rotation_angle()
        self.set_arrow_transform_origin_to_center()
        self.setRotation(angle)
        if not self.is_ghost:
            self.ghost.setRotation(angle)

    def set_arrow_transform_origin_to_center(self) -> None:
        self.setTransformOriginPoint(self.boundingRect().center())

    def clear_attributes(self) -> None:
        self.motion_type = None
        self.loc = None
        self.turns = None
        self.motion = None

    ### GETTERS ###

    def _get_shift_rotation_angle(self) -> RotationAngles:
        motion = self.motion

        if motion.motion_type == PRO:
            return (
                {
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
                }
                .get(motion.prop_rot_dir)
                .get(self.loc)
            )
        elif motion.motion_type == ANTI:
            return (
                {
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
                }
                .get(motion.prop_rot_dir)
                .get(self.loc)
            )

    def _get_dash_rotation_angle(
        self, arrow: Optional["Arrow"] = None
    ) -> RotationAngles:
        arrow = arrow or self
        dash_rot_angle = self._get_rot_angle(arrow.motion)
        return dash_rot_angle

    def _get_static_rotation_angle(
        self, arrow: Optional["Arrow"] = None
    ) -> RotationAngles:
        arrow = arrow or self
        static_rot_angle = self._get_rot_angle(arrow.motion)
        return static_rot_angle

    def _get_rot_angle(
        self, motion: "Motion"
    ) -> Dict[PropRotDirs, Dict[Locations, int]]:
        from objects.pictograph.pictograph import Pictograph

        if isinstance(self.scene, Pictograph):
            other_motion = (
                self.scene.arrows[RED].motion
                if self.color == BLUE
                else self.scene.arrows[BLUE].motion
            )

        if motion.motion_type == STATIC:
            if motion.start_ori == IN:
                
                return (
                    {
                        CLOCKWISE: {
                            NORTH: 180,
                            EAST: 270,
                            SOUTH: 0,
                            WEST: 90,
                        },
                        COUNTER_CLOCKWISE: {
                            NORTH: 180,
                            EAST: 90,
                            SOUTH: 0,
                            WEST: 270,
                        },
                        NO_ROT: {
                            NORTH: 0,
                            SOUTH: 0,
                            EAST: 0,
                            WEST: 0,
                        },
                    }
                    .get(motion.prop_rot_dir, {})
                    .get(self.loc, 0)
                )
            elif motion.start_ori == OUT:
                return (
                    {
                        CLOCKWISE: {
                            NORTH: 0,
                            EAST: 90,
                            SOUTH: 180,
                            WEST: 270,
                        },
                        COUNTER_CLOCKWISE: {
                            NORTH: 0,
                            EAST: 90,
                            SOUTH: 180,
                            WEST: 270,
                        },
                        NO_ROT: {
                            NORTH: 0,
                            SOUTH: 0,
                            EAST: 0,
                            WEST: 0,
                        },
                    }
                    .get(motion.prop_rot_dir, {})
                    .get(self.loc, 0)
                )

        elif motion.motion_type == DASH:
            if motion.turns == 0:
                if self.scene.letter == "Λ-":
                    if self.loc:
                        loc_map = {
                            ((NORTH, SOUTH), (EAST, WEST)): {EAST: 90},
                            ((EAST, WEST), (NORTH, SOUTH)): {NORTH: 180},
                            ((NORTH, SOUTH), (WEST, EAST)): {WEST: 90},
                            ((WEST, EAST), (NORTH, SOUTH)): {NORTH: 0},
                            ((SOUTH, NORTH), (EAST, WEST)): {EAST: 270},
                            ((EAST, WEST), (SOUTH, NORTH)): {SOUTH: 180},
                            ((SOUTH, NORTH), (WEST, EAST)): {WEST: 270},
                            ((WEST, EAST), (SOUTH, NORTH)): {SOUTH: 0},
                        }
                        arrow_angle = loc_map.get(
                            (
                                (self.motion.start_loc, self.motion.end_loc),
                                (other_motion.start_loc, other_motion.end_loc),
                            )
                        ).get(self.loc)
                        return arrow_angle

                    else:
                        self.ghost.loc = self.loc
                        map = {
                            (NORTH, SOUTH): {EAST: 90, WEST: 90},
                            (SOUTH, NORTH): {EAST: 270, WEST: 270},
                            (EAST, WEST): {NORTH: 180, SOUTH: 180},
                            (WEST, EAST): {NORTH: 0, SOUTH: 0},
                        }

                        return map.get(
                            (self.motion.start_loc, self.motion.end_loc), {}
                        ).get(self.loc)
                elif self.scene.letter == "Φ-":
                    loc_map = {
                        ((NORTH, SOUTH), (SOUTH, NORTH)): {RED: EAST, BLUE: WEST},
                        ((SOUTH, NORTH), (NORTH, SOUTH)): {RED: EAST, BLUE: WEST},
                        ((EAST, WEST), (WEST, EAST)): {RED: NORTH, BLUE: SOUTH},
                        ((WEST, EAST), (EAST, WEST)): {RED: NORTH, BLUE: SOUTH},
                    }
                    arrow_loc = loc_map.get(
                        (
                            (self.motion.start_loc, self.motion.end_loc),
                            (other_motion.start_loc, other_motion.end_loc),
                        )
                    ).get(self.color)
                    self.loc = arrow_loc
                    self.ghost.loc = arrow_loc
                    map = {
                        (NORTH, SOUTH): {EAST: 90, WEST: 90},
                        (SOUTH, NORTH): {EAST: 270, WEST: 270},
                        (EAST, WEST): {NORTH: 180, SOUTH: 180},
                        (WEST, EAST): {NORTH: 0, SOUTH: 0},
                    }
                    return map.get(
                        (self.motion.start_loc, self.motion.end_loc), {}
                    ).get(self.loc)
                elif self.scene.letter == "Ψ-":
                    loc_map = {
                        ((NORTH, SOUTH), (NORTH, SOUTH)): {RED: EAST, BLUE: WEST},
                        ((EAST, WEST), (EAST, WEST)): {RED: NORTH, BLUE: SOUTH},
                        ((SOUTH, NORTH), (SOUTH, NORTH)): {RED: EAST, BLUE: WEST},
                        ((WEST, EAST), (WEST, EAST)): {RED: NORTH, BLUE: SOUTH},
                    }
                    arrow_loc = loc_map.get(
                        (
                            (self.motion.start_loc, self.motion.end_loc),
                            (other_motion.start_loc, other_motion.end_loc),
                        )
                    ).get(self.color)
                    self.loc = arrow_loc
                    self.ghost.loc = arrow_loc
                    rot_map = {
                        (NORTH, SOUTH): 90,
                        (SOUTH, NORTH): 270,
                        (EAST, WEST): 180,
                        (WEST, EAST): 0,
                    }
                    return rot_map.get((self.motion.start_loc, self.motion.end_loc))
                elif self.scene.letter in ["Φ", "Ψ"]:  # Type 4 Letters
                    loc_map = {
                        (NORTH, SOUTH): {RED: EAST, BLUE: WEST},
                        (SOUTH, NORTH): {RED: EAST, BLUE: WEST},
                        (EAST, WEST): {RED: NORTH, BLUE: SOUTH},
                        (WEST, EAST): {RED: NORTH, BLUE: SOUTH},
                    }
                    arrow_loc = loc_map.get(
                        (self.motion.start_loc, self.motion.end_loc)
                    ).get(self.color)
                    self.loc = arrow_loc
                    rot_map = {
                        (NORTH, SOUTH): 90,
                        (SOUTH, NORTH): 270,
                        (EAST, WEST): 180,
                        (WEST, EAST): 0,
                    }
                    return rot_map.get((self.motion.start_loc, self.motion.end_loc))
                else:  # Letters is Λ
                    loc_map = {
                        ((NORTH, SOUTH), WEST): EAST,
                        ((EAST, WEST), SOUTH): NORTH,
                        ((NORTH, SOUTH), EAST): WEST,
                        ((WEST, EAST), SOUTH): NORTH,
                        ((SOUTH, NORTH), WEST): EAST,
                        ((EAST, WEST), NORTH): SOUTH,
                        ((SOUTH, NORTH), EAST): WEST,
                        ((WEST, EAST), NORTH): SOUTH,
                    }
                    self.loc = loc_map.get(
                        (
                            (self.motion.start_loc, self.motion.end_loc),
                            other_motion.end_loc,
                        )
                    )

                    rot_map = {
                        (NORTH, SOUTH): 90,
                        (SOUTH, NORTH): 270,
                        (EAST, WEST): 180,
                        (WEST, EAST): 0,
                    }
                    return rot_map.get((self.motion.start_loc, self.motion.end_loc))
            elif motion.turns > 0:
                if motion.prop_rot_dir == CLOCKWISE:
                    rot_map = {
                        (NORTH, SOUTH): 90,
                        (SOUTH, NORTH): 270,
                        (EAST, WEST): 180,
                        (WEST, EAST): 0,
                    }
                    return rot_map.get((self.motion.start_loc, self.motion.end_loc))
                elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    rot_map = {
                        (NORTH, SOUTH): 90,
                        (SOUTH, NORTH): 270,
                        (EAST, WEST): 0,
                        (WEST, EAST): 180,
                    }
                    return rot_map.get((self.motion.start_loc, self.motion.end_loc))

    def assign_Λ_dash_arrow_loc(self):
        other_motion = (
            self.scene.arrows[RED].motion
            if self.color == BLUE
            else self.scene.arrows[BLUE].motion
        )

        loc_map = {
            ((NORTH, SOUTH), (EAST, WEST)): EAST,
            ((EAST, WEST), (NORTH, SOUTH)): NORTH,
            ((NORTH, SOUTH), (WEST, EAST)): WEST,
            ((WEST, EAST), (NORTH, SOUTH)): NORTH,
            ((SOUTH, NORTH), (EAST, WEST)): EAST,
            ((EAST, WEST), (SOUTH, NORTH)): SOUTH,
            ((SOUTH, NORTH), (WEST, EAST)): WEST,
            ((WEST, EAST), (SOUTH, NORTH)): SOUTH,
        }

        arrow_loc = loc_map.get(
            (
                (self.motion.start_loc, self.motion.end_loc),
                (other_motion.start_loc, other_motion.end_loc),
            )
        )
        self.loc = arrow_loc
        self.ghost.loc = arrow_loc

    def get_attributes(self) -> Dict[str, Union[Colors, Locations, MotionTypes, Turns]]:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        return {attr: getattr(self, attr) for attr in arrow_attributes}

    def get_svg_file(self, motion_type: MotionTypes, turns: Turns) -> str:
        svg_file = f"resources/images/arrows/{self.pictograph.main_widget.grid_mode}/{motion_type}/{motion_type}_{float(turns)}.svg"
        return svg_file

    def _change_arrow_to_static(self) -> None:
        motion_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            TURNS: 0,
            START_LOC: self.motion.prop.loc,
            END_LOC: self.motion.prop.loc,
        }
        self.motion.update_motion(motion_dict)

        self.motion[COLOR] = self.color
        self.motion[MOTION_TYPE] = STATIC
        self.motion[TURNS] = 0
        self.motion[PROP_ROT_DIR] = None
        self.motion[START_LOC] = self.motion.prop.loc
        self.motion[END_LOC] = self.motion.prop.loc
        self.loc = self.motion.prop.loc

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.update_attributes(arrow_dict)
            if not self.is_ghost and self.ghost:
                self.ghost.update_attributes(arrow_dict)

        if not self.is_ghost:
            self.ghost.transform = self.transform
        self.update_svg()
        self._update_mirror()
        self._update_color()
        self._update_location()
        self._update_rotation()

    def mirror_svg(self) -> None:
        self.center_x = self.boundingRect().center().x()
        self.center_y = self.boundingRect().center().y()
        self.set_arrow_transform_origin_to_center()
        transform = QTransform()
        transform.translate(self.center_x, self.center_y)
        transform.scale(-1, 1)
        transform.translate(-self.center_x, -self.center_y)
        self.setTransform(transform)
        if not self.is_ghost and self.ghost:
            self.ghost.setTransform(transform)
            self.ghost.is_svg_mirrored = True
        self.is_svg_mirrored = True

    def unmirror_svg(self) -> None:
        self.center_x = self.boundingRect().center().x()
        self.center_y = self.boundingRect().center().y()
        transform = QTransform()
        transform.translate(self.center.x(), self.center.y())
        transform.scale(1, 1)
        transform.translate(-self.center.x(), -self.center.y())
        self.setTransform(transform)
        if hasattr(self, GHOST) and self.ghost:
            self.ghost.setTransform(transform)
            self.ghost.is_svg_mirrored = False
        self.is_svg_mirrored = False

    def adjust_position(self, adjustment):
        self.setPos(self.pos() + QPointF(*adjustment))

    ### DELETION ###

    def delete_arrow(self, keep_prop: bool = False) -> None:
        if self in self.scene.arrows.values():
            self.scene.removeItem(self)
            self.scene.removeItem(self.ghost)
            self.motion.clear_attributes()
            self.prop.clear_attributes()
            self.ghost.clear_attributes()
            self.prop.clear_attributes()
        if keep_prop:
            self._change_arrow_to_static()
        else:
            self.scene.removeItem(self.prop)

        self.scene.update_pictograph()
