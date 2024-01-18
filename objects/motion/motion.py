from constants import *
from typing import TYPE_CHECKING, Dict, Union
from objects.motion.motion_attr_manager import MotionAttrManager
from objects.motion.motion_manipulator import MotionManipulator
from objects.motion.motion_ori_calculator import MotionOriCalculator
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Handpaths,
    LeadStates,
    Locations,
    MotionTypes,
    Orientations,
    PropRotDirs,
    Turns,
)

from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import PropBox


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )
from objects.motion.motion_turn_manager import MotionTurnsManager


class Motion:
    def __init__(
        self,
        scene: Union["ArrowBox", "PropBox", "Pictograph"],
        motion_dict: Dict,
    ) -> None:
        self.scene = scene
        self.manipulator = MotionManipulator(self)
        self.attr_manager = MotionAttrManager(self)
        self.ori_calculator = MotionOriCalculator(self)
        self.turns_manager = MotionTurnsManager(self)
        self.color: Colors = motion_dict.get(COLOR)
        self.turns: Turns = motion_dict.get(TURNS)
        self.init_attributes()

    def init_attributes(self) -> None:
        self.arrow: "Arrow"
        self.prop: "Prop"
        self.motion_type: MotionTypes
        self.start_loc: Locations
        self.start_ori: Orientations
        self.end_loc: Locations
        self.end_ori: Orientations
        self.prop_rot_dir: PropRotDirs
        self.lead_state: LeadStates

    ### UPDATE ###

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.attr_manager.update_attributes(motion_dict)
        arrow_dict = {
            LOC: self.arrow.arrow_location_manager.get_arrow_location(),
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
        }
        prop_dict = {
            LOC: self.end_loc,
            ORI: self.ori_calculator.get_end_ori(),
        }
        self.end_ori = self.ori_calculator.get_end_ori()
        self.arrow.update_arrow(arrow_dict)
        self.prop.update_prop(prop_dict)

    ### GETTERS ###


    def get_other_arrow(self) -> "Arrow":
        return (
            self.scene.arrows[RED]
            if self.arrow.color == BLUE
            else self.scene.arrows[BLUE]
        )

    ### FLAGS ###

    def is_shift(self) -> bool:
        return self.motion_type in [PRO, ANTI, FLOAT]

    def is_dash(self) -> bool:
        return self.motion_type == DASH

    def is_static(self) -> bool:
        return self.motion_type == STATIC

    def is_dash_or_static(self) -> bool:
        return self.motion_type in [DASH, STATIC]
