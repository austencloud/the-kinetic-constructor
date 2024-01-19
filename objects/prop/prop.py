from typing import TYPE_CHECKING, Dict, Tuple, Union
from Enums import PropAttribute

from objects.graphical_object.graphical_object import GraphicalObject
from PyQt6.QtCore import QPointF
from constants import *
from objects.prop.prop_attr_manager import PropAttrManager
from objects.prop.prop_mouse_event_handler import PropMouseEventHandler
from objects.prop.prop_rot_angle_manager import PropRotAngleManager
from utilities.TypeChecking.TypeChecking import (
    Axes,
    Colors,
    Locations,
    Orientations,
)
from utilities.TypeChecking.prop_types import PropTypes


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import (
        PropBox,
    )


class Prop(GraphicalObject):
    loc: Locations
    ori: Orientations

    def __init__(self, scene, prop_dict: Dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.motion = motion
        self.scene: Pictograph | PropBox = scene
        self.arrow: Arrow
        self.ghost: Prop = None
        self.is_ghost: bool = False
        self.previous_location: Locations
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.mouse_event_handler = PropMouseEventHandler(self)
        self.attr_manager.update_attributes(prop_dict)
        self.svg_file = self.svg_manager.get_prop_svg_file(self.prop_type)
        self.svg_manager.setup_svg_renderer(self.svg_file)
        self.setZValue(10)
        self.center = self.boundingRect().center()

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press()

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)

    ### GETTERS ###

    def update_prop(
        self, prop_dict: Dict[str, Union[Colors, Locations, Orientations]] = None
    ) -> None:
        if prop_dict:
            self.attr_manager.update_attributes(prop_dict)
        self.svg_manager.update_prop_svg()
        self.svg_manager.update_color()
        self.rot_angle_manager.update_prop_rotation_angle()

    ### UPDATERS ###

    def update_prop_type(self, prop_type: PropTypes) -> None:
        self.prop_type = prop_type
        self.svg_manager.update_prop_svg()
        self.update_prop()

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

    def is_radial(self) -> bool:
        return self.ori in [IN, OUT]

    def is_antiradial(self) -> bool:
        return self.ori in [CLOCK, COUNTER]
