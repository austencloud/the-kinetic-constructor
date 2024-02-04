from typing import TYPE_CHECKING
from constants import LOC, MOTION_TYPE, ORI, TURNS

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_motion(self, motion_dict=None) -> None:
        self.motion.end_ori = self.motion.ori_calculator.get_end_ori()

        if not self.motion.arrow.initialized:
            self.motion.arrow.setup_components()

        if motion_dict:
            self.motion.attr_manager.update_attributes(motion_dict)
        
        prop_dict = {
            LOC: self.motion.end_loc,
            ORI: self.motion.end_ori,
        }
        self.motion.prop.updater.update_prop(prop_dict)
