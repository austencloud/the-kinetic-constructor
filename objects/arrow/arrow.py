from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *
from objects.arrow.arrow_location_manager import ArrowLocationManager
from objects.arrow.arrow_rot_angle_manager import ArrowRotAngleManager
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
    from objects.arrow.ghost_arrow import GhostArrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )


class Arrow(GraphicalObject):
    def __init__(self, scene, arrow_dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.svg_cache = {}
        self.attribute_cache = {}
        self.motion = motion
        self._initialize_attributes(scene)
        self.update_attributes(arrow_dict)
        self.setAcceptHoverEvents(True)
        self.set_arrow_transform_origin_to_center()

    def _initialize_attributes(self, scene):
        self.svg_file = None
        self.arrow_rot_angle_manager = ArrowRotAngleManager(self)
        self.arrow_location_manager = ArrowLocationManager(self)
        self.prop: Optional[Prop] = None
        self.scene: Union[Pictograph, ArrowBox] = scene
        self.is_svg_mirrored: bool = False
        self.is_dragging: bool = False
        self.ghost: Optional[GhostArrow] = None
        self.loc: Optional[Locations] = None
        self.is_ghost: bool = False
        self.drag_offset = QPointF(0, 0)
        self.lead_state: Optional[LeadStates] = None

    ### SETUP ###

    def update_arrow_svg(self) -> None:
        svg_file = self.get_arrow_svg_file(self.motion_type, self.turns)
        if self.svg_file != svg_file:
            self.update_svg(svg_file)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)

        self.pictograph.clear_selections()
        self.setSelected(True)

        if hasattr(self, GHOST) and self.ghost:
            self.ghost.show()

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

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def _update_mirror(self) -> None:
        new_mirror_state = False
        if self.motion_type in [PRO, STATIC]:
            new_mirror_state = self.motion.prop_rot_dir == COUNTER_CLOCKWISE
        elif self.motion_type == ANTI:
            new_mirror_state = self.motion.prop_rot_dir == CLOCKWISE
        elif self.motion_type == DASH and self.turns > 0:
            new_mirror_state = self.motion.prop_rot_dir == COUNTER_CLOCKWISE

        # Update only if mirror state has changed
        if new_mirror_state != self.is_svg_mirrored:
            if new_mirror_state:
                self.mirror_svg()
            else:
                self.unmirror_svg()

    def set_arrow_transform_origin_to_center(self) -> None:
        self.setTransformOriginPoint(self.boundingRect().center())

    def clear_attributes(self) -> None:
        self.motion_type = None
        self.loc = None
        self.turns = None
        self.motion = None

    ### GETTERS ###

    def get_attributes(self) -> Dict[str, Union[Colors, Locations, MotionTypes, Turns]]:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        return {attr: getattr(self, attr) for attr in arrow_attributes}

    def get_arrow_svg_file(self, motion_type: MotionTypes, turns: Turns) -> str:
        cache_key = f"{motion_type}_{float(turns)}"
        if cache_key not in self.svg_cache:
            file_path = f"resources/images/arrows/{self.pictograph.main_widget.grid_mode}/{motion_type}/{motion_type}_{float(turns)}.svg"
            self.svg_cache[cache_key] = file_path
        return self.svg_cache[cache_key]

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
        self.update_arrow_svg()
        self._update_mirror()
        self.arrow_location_manager.update_location()
        self.arrow_rot_angle_manager.update_rotation()

    def mirror_svg(self) -> None:
        # self.set_arrow_transform_origin_to_center()
        self.center_x = self.boundingRect().center().x()
        self.center_y = self.boundingRect().center().y()
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
        # self.set_arrow_transform_origin_to_center()
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

    def adjust_position(self, adjustment) -> None:
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
