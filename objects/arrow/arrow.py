from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *
from objects.arrow.arrow_attr_manager import ArrowAttrManager
from objects.arrow.arrow_mirror_manager import ArrowMirrorManager
from .arrow_location_manager import ArrowLocationCalculator
from .arrow_rot_angle_manager import ArrowRotAngleCalculator
from ..prop.prop import Prop

from ..graphical_object.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
    Turns,
    TYPE_CHECKING,
    Dict,
)


if TYPE_CHECKING:
    from ..motion.motion import Motion
    from .ghost_arrow import GhostArrow
    from ..prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )
    from widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    svg_cache = {}

    def __init__(self, scene, arrow_dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.scene: Pictograph | ArrowBox = scene
        self.motion: Motion = motion
        self.rot_angle_calculator = ArrowRotAngleCalculator(self)
        self.location_calculator = ArrowLocationCalculator(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        self.motion_type: MotionTypes = None
        self.ghost: GhostArrow = None
        self.is_svg_mirrored: bool = False
        self.color = arrow_dict[COLOR]
        self.prop: Prop = None
        self.is_ghost: bool = False
        self.loc: Locations = None

    def setup_arrow(self, arrow_dict) -> None:
        self.motion_type = arrow_dict[MOTION_TYPE]
        self.turns = arrow_dict[TURNS]

        self.svg_file = self.svg_manager.get_arrow_svg_file(
            arrow_dict[MOTION_TYPE],
            arrow_dict[TURNS],
        )
        self.svg_manager.setup_svg_renderer(self.svg_file)
        self.setAcceptHoverEvents(True)
        self.attr_manager.update_attributes(arrow_dict)
        self.drag_offset = QPointF(0, 0)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)

        self.pictograph.clear_selections()
        self.setSelected(True)

        if hasattr(self, GHOST) and self.ghost:
            self.ghost.show()

        self.scene.state_updater.update_pictograph()

    def mouseMoveEvent(
        self: Union["Prop", "Arrow"], event: "QGraphicsSceneMouseEvent"
    ) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_location = self.scene.grid.get_closest_layer2_point(event.scenePos())[0]
            new_pos = event.scenePos() - self.get_center()
            self.set_drag_pos(new_pos)
            if new_location != self.loc:
                self.location_calculator.update_location(new_location)

    def mouseReleaseEvent(self, event) -> None:
        self.scene.arrows[self.color] = self
        self.scene.state_updater.update_pictograph()
        self.ghost.hide()

    ### UPDATERS ###

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def set_arrow_transform_origin_to_center(self) -> None:
        self.setTransformOriginPoint(self.boundingRect().center())

    ### GETTERS ###

    def _change_arrow_to_static(self) -> None:
        motion_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            TURNS: 0,
            START_LOC: self.motion.prop.loc,
            END_LOC: self.motion.prop.loc,
        }
        self.motion.updater.update_motion(motion_dict)

        self.motion[COLOR] = self.color
        self.motion[MOTION_TYPE] = STATIC
        self.motion[TURNS] = 0
        self.motion[PROP_ROT_DIR] = None
        self.motion[START_LOC] = self.motion.prop.loc
        self.motion[END_LOC] = self.motion.prop.loc
        self.loc = self.motion.prop.loc

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.attr_manager.update_attributes(arrow_dict)
            if not self.is_ghost and self.ghost:
                self.ghost.attr_manager.update_attributes(arrow_dict)

        if not self.is_ghost:
            self.ghost.transform = self.transform
        self.svg_manager.update_arrow_svg()
        self.mirror_manager.update_mirror()
        self.svg_manager.update_color()
        self.location_calculator.update_location()
        self.rot_angle_calculator.update_rotation()

    def adjust_position(self, adjustment) -> None:
        self.setPos(self.pos() + QPointF(*adjustment))

    ### DELETION ###

    def delete_arrow(self, keep_prop: bool = False) -> None:
        if self in self.scene.arrows.values():
            self.scene.removeItem(self)
            self.scene.removeItem(self.ghost)
            self.prop.clear_attributes()
            self.ghost.clear_attributes()
            self.prop.clear_attributes()
        if keep_prop:
            self._change_arrow_to_static()
        else:
            self.scene.removeItem(self.prop)

        self.scene.state_updater.update_pictograph()
