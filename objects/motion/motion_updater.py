from typing import TYPE_CHECKING
from constants import LOC, MOTION_TYPE, ORI, TURNS

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.motion.attr_manager.update_attributes(motion_dict)
        arrow_dict = {
            LOC: self.motion.arrow.location_calculator.get_arrow_location(),
            MOTION_TYPE: self.motion.motion_type,
            TURNS: self.motion.turns,
        }
        prop_dict = {
            LOC: self.motion.end_loc,
            ORI: self.motion.ori_calculator.get_end_ori(),
        }
        self.motion.end_ori = self.motion.ori_calculator.get_end_ori()
        self.motion.arrow.update_arrow(arrow_dict)
        self.motion.prop.update_prop(prop_dict)
