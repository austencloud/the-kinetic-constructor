from typing import TYPE_CHECKING
from data.constants import *


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionAttrManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.motion.color = self.motion.motion_data.get(COLOR)
        self.motion.turns = self.motion.motion_data.get(TURNS)
        self.motion.start_loc = None
        self.motion.end_loc = None
        self.motion.motion_type = None

    def update_attributes(self, motion_data: dict[str, str]) -> None:
        # print the dict
        # if motion_data has "turns", set motion.turns directly to it
        if TURNS in motion_data:
            self.motion.turns = motion_data[TURNS]
        for attribute, value in motion_data.items():
            if value is not None:
                setattr(self.motion, attribute, value)
                # print the motion attribute and value
                print(f"Setting {attribute} to {value} for {self.motion}")
                self.motion.motion_data[attribute] = value  # Sync to motion_data
        if self.motion.check.is_shift():
            if "prefloat_motion_type" not in motion_data:
                if self.motion.motion_type != FLOAT:
                    self.motion.prefloat_motion_type = self.motion.motion_type
            if "prefloat_motion_type" in motion_data:
                if motion_data["prefloat_motion_type"] == FLOAT:
                    print("Warning: prefloat_motion_type cannot be 'float'")
                else:
                    prefloat_motion_type = motion_data["prefloat_motion_type"]
                    self.motion.prefloat_motion_type = prefloat_motion_type
            if "prefloat_prop_rot_dir" in motion_data:
                if motion_data["prefloat_prop_rot_dir"] == NO_ROT:
                    print("Warning: prefloat_prop_rot_dir cannot be 'no_rot'")
                else:
                    self.motion.prefloat_prop_rot_dir = motion_data[
                        "prefloat_prop_rot_dir"
                    ]

    def update_prop_ori(self) -> None:
        if hasattr(self.motion, PROP) and self.motion.prop:
            if not self.motion.end_ori:
                self.motion.end_ori = self.motion.ori_calculator.get_end_ori()
            self.motion.prop.ori = self.motion.end_ori
            self.motion.prop.loc = self.motion.end_loc

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
