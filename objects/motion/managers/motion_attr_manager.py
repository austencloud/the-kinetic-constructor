from typing import TYPE_CHECKING
from Enums.Enums import Letter
from data.constants import *


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionAttrManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.motion.color = self.motion.motion_dict.get(COLOR)
        self.motion.turns = self.motion.motion_dict.get(TURNS)
        self.motion.start_loc = None
        self.motion.end_loc = None
        self.motion.motion_type = None

    def update_attributes(self, motion_dict: dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self.motion, attribute, value)
        if self.motion.check.is_shift():
            if "prefloat_motion_type" not in motion_dict:
                self.motion.prefloat_motion_type = self.motion.motion_type
            # if "prefloat_prop_rot_dir" not in motion_dict:
            #     self.motion.prefloat_prop_rot_dir = self.motion.prop_rot_dir
        if self.motion.pictograph.letter in [
            Letter.S,
            Letter.T,
            Letter.U,
            Letter.V,
        ]:
            self.assign_lead_states()

    def update_prop_ori(self) -> None:
        if hasattr(self.motion, PROP) and self.motion.prop:
            if not self.motion.end_ori:
                self.motion.end_ori = self.motion.ori_calculator.get_end_ori()
            self.motion.prop.ori = self.motion.end_ori
            self.motion.prop.loc = self.motion.end_loc
            self.motion.prop.axis = self.motion.prop.attr_manager.get_axis_from_ori()

    def get_attributes(self) -> dict[str, str]:
        return {
            COLOR: self.motion.color,
            MOTION_TYPE: self.motion.motion_type,
            TURNS: self.motion.turns,
            PROP_ROT_DIR: self.motion.prop_rot_dir,
            START_LOC: self.motion.start_loc,
            END_LOC: self.motion.end_loc,
            START_ORI: self.motion.start_ori,
            END_ORI: self.motion.end_ori,
        }


    def assign_lead_states(self) -> None:
        leading_motion = self.motion.pictograph.get.leading_motion()
        trailing_motion = self.motion.pictograph.get.trailing_motion()
        if self.motion.pictograph.get.leading_motion():
            leading_motion.arrow.motion.lead_state = LEADING
            trailing_motion.arrow.motion.lead_state = TRAILING
