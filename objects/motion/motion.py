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
        self.init_attributes()
        self.color = motion_dict.get(COLOR)
        self.turns = motion_dict.get(TURNS)

    def init_attributes(self) -> None:
        self.color: Colors = None
        self.arrow: "Arrow" = None
        self.prop: "Prop" = None
        self.motion_type: MotionTypes = None
        self.turns: Turns = None
        self.start_loc: Locations = None
        self.start_ori: Orientations = None
        self.end_loc: Locations = None
        self.end_ori: Orientations = None
        self.prop_rot_dir: PropRotDirs = None
        self.lead_state: LeadStates = None

    ### SETUP ###

    def update_attributes(self, motion_dict: Dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self, attribute, value)
        if self.motion_type:
            self.end_ori: Orientations = self.ori_calculator.get_end_ori()

    ### UPDATE ###


    def clear_attributes(self) -> None:
        self.start_loc = None
        self.end_loc = None
        self.turns = None
        self.motion_type = None
        self.start_ori = None
        self.end_ori = None

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.update_attributes(motion_dict)
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

    def get_attributes(self) -> Dict[str, str]:
        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
            PROP_ROT_DIR: self.prop_rot_dir,
            START_LOC: self.start_loc,
            END_LOC: self.end_loc,
            START_ORI: self.start_ori,
            END_ORI: self.end_ori,
        }

    def get_other_arrow(self) -> "Arrow":
        return (
            self.scene.arrows[RED]
            if self.arrow.color == BLUE
            else self.scene.arrows[BLUE]
        )

    def set_motion_turns(self, turns: Turns) -> None:
        self.turns = turns
        self.arrow.turns = turns

    def adjust_motion_turns(self, adjustment: float) -> None:
        new_turns = max(0, min(3, self.arrow.turns + adjustment))

        if new_turns != self.arrow.turns:
            self.turns = new_turns
            self.arrow.turns = new_turns

    def add_half_turn(self) -> None:
        self.adjust_motion_turns(0.5)

    def subtract_half_turn(self) -> None:
        self.adjust_motion_turns(-0.5)

    def add_turn(self) -> None:
        self.adjust_motion_turns(1)

    def subtract_turn(self) -> None:
        self.adjust_motion_turns(-1)

    ### FLAGS ###

    def is_shift(self) -> bool:
        return self.motion_type in [PRO, ANTI, FLOAT]

    def is_dash(self) -> bool:
        return self.motion_type == DASH

    def is_static(self) -> bool:
        return self.motion_type == STATIC

    def is_dash_or_static(self) -> bool:
        return self.motion_type in [DASH, STATIC]

    def set_motion_turns(self, turns: Turns) -> None:
        self.turns = turns
        self.arrow.turns = turns
        self.arrow.ghost.turns = turns
