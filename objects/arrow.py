from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem
from Enums import *
from constants import (
    ANTI,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    END_LOC,
    LOCATION,
    MOTION_TYPE,
    NORTHEAST,
    NORTHWEST,
    PRO,
    PROP_ROT_DIR,
    SOUTHEAST,
    SOUTHWEST,
    START_LOC,
    STATIC,
    TURNS,
)
from objects.motion.motion_manipulator import MotionManipulator
from objects.grid import GridItem
from objects.prop.prop import Prop

from objects.graphical_object import GraphicalObject
from data.start_end_loc_map import get_start_end_locs
from utilities.TypeChecking.TypeChecking import (
    Turns,
    RotationAngles,
    TYPE_CHECKING,
    Optional,
    Dict,
)

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from objects.pictograph.pictograph import Pictograph
    from objects.ghosts.ghost_arrow import GhostArrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


class Arrow(GraphicalObject):
    def __init__(self, scene, arrow_dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.motion = motion
        self.prop: Prop = None
        self.svg_file = self.get_svg_file(
            arrow_dict[MOTION_TYPE],
            arrow_dict[TURNS],
        )
        self.setup_svg_renderer(self.svg_file)
        self.setAcceptHoverEvents(True)
        self._setup_attributes(scene, arrow_dict)

    ### SETUP ###

    def _setup_attributes(self, scene, arrow_dict: "ArrowAttributesDicts") -> None:
        self.scene: Pictograph | ArrowBox = scene
        self.drag_offset = QPointF(0, 0)
        self.is_svg_mirrored: bool = False
        self.is_dragging: bool = False
        self.ghost: GhostArrow = None
        self.location: Location = None
        self.is_ghost: bool = False
        self.turns: Turns = arrow_dict[TURNS]

        self.center_x = self.boundingRect().width() / 2
        self.center_y = self.boundingRect().height() / 2

        if arrow_dict:
            self.update_attributes(arrow_dict)
            self.arrow_dict = arrow_dict

        if self.motion:
            self.update_arrow()
            self.center = self.boundingRect().center()

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
            if new_location != self.location:
                self.update_location(new_location)

    def mouseReleaseEvent(self, event) -> None:
        self.is_dragging = False
        self.scene.arrows[self.color] = self
        self.scene.update_pictograph()
        self.ghost.hide()

    ### UPDATERS ###

    def update_location(self, location):
        self.location = location
        self.ghost.location = location

        self.motion.prop.update_prop()
        self.update_arrow()

        self.scene.ghost_arrows[self.color] = self.ghost
        self.scene.props[self.color] = self.motion.prop
        self.is_dragging = True
        self.scene.update_pictograph()
        self.motion.update_prop_ori()

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def update_mirror(self) -> None:
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

        if self.is_svg_mirrored:
            self.mirror_svg()
        else:
            self.unmirror_svg()

    def update_rotation(self) -> None:
        angle = self.get_arrow_rotation_angle()
        self.setRotation(angle)

    def update_prop_during_drag(self) -> None:
        for prop in self.scene.props.values():
            if prop.color == self.color:
                if prop not in self.scene.props:
                    self.scene.props[prop.color] = prop

                prop.update_attributes(
                    {
                        COLOR: self.color,
                        LOCATION: self.motion.end_loc,
                    }
                )

                prop.show()
                prop.update_prop()
                self.scene.update_pictograph()

    def set_arrow_transform_origin_to_center(self) -> None:
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    def clear_attributes(self) -> None:
        self.motion_type = None
        self.location = None
        self.turns = None
        self.motion = None

    ### GETTERS ###

    def get_svg_data(self, svg_file: str) -> bytes:
        with open(svg_file, "r") as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_arrow_rotation_angle(
        self, arrow: Optional["Arrow"] = None
    ) -> RotationAngles:
        arrow = arrow or self
        location_to_angle = self.get_location_to_angle_map(
            arrow.motion.motion_type, arrow.motion.prop_rot_dir
        )
        return location_to_angle.get(self.location, 0)

    def get_location_to_angle_map(
        self, motion_type: MotionType, prop_rot_dir: PropRotationDirection
    ) -> Dict[PropRotationDirection, Dict[Location, int]]:
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
            }.get(prop_rot_dir, {})
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
            }.get(prop_rot_dir, {})
        elif motion_type == STATIC:
            return {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
            }.get(prop_rot_dir, {})
        elif motion_type == DASH:
            return {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
            }.get(prop_rot_dir, {})

    def get_attributes(self) -> ArrowAttributesDicts:
        arrow_attributes = [COLOR, LOCATION, MOTION_TYPE, TURNS]
        return {attr: getattr(self, attr) for attr in arrow_attributes}

    def get_svg_file(self, motion_type: MotionType, turns: Turns) -> str:
        svg_file = f"{image_path}arrows/{self.pictograph.main_widget.grid_mode}/{motion_type}/{motion_type}_{float(turns)}.svg"
        return svg_file

    def _change_arrow_to_static(self) -> None:
        static_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            TURNS: 0,
        }

        self.update_attributes(static_arrow_dict)
        self.motion[COLOR] = self.color
        self.motion[MOTION_TYPE] = STATIC
        self.motion[TURNS] = 0
        self.motion[PROP_ROT_DIR] = None
        self.motion[START_LOC] = self.motion.prop.loc
        self.motion[END_LOC] = self.motion.prop.loc
        self.location = self.motion.prop.loc

    def update_turns(self) -> None:
        self.turns = self.motion.turns

    def update_arrow(self, arrow_dict: ArrowAttributesDicts = None) -> None:
        self.update_turns()
        self.update_svg()
        self.update_mirror()
        self.update_color()
        self.update_rotation()
        if arrow_dict:
            self.update_attributes(arrow_dict)

        if not self.is_ghost and self.ghost:
            self.ghost.update_arrow(arrow_dict if arrow_dict else None)
            self.ghost.transform = self.transform

    def mirror_svg(self) -> None:
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
        transform = QTransform()
        transform.translate(self.center.x(), self.center.y())
        transform.scale(1, 1)
        transform.translate(-self.center.x(), -self.center.y())
        self.setTransform(transform)
        if hasattr(self, GHOST) and self.ghost:
            self.ghost.setTransform(transform)
            self.ghost.is_svg_mirrored = False
        self.is_svg_mirrored = False

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
