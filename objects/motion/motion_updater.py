from typing import TYPE_CHECKING
from constants import LOC, MOTION_TYPE, ORI, TURNS

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.m = motion

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.m.attr_manager.update_attributes(motion_dict)
        arrow_dict = {
            LOC: self.m.arrow.location_calculator.get_arrow_location(),
            MOTION_TYPE: self.m.motion_type,
            TURNS: self.m.turns,
        }
        prop_dict = {
            LOC: self.m.end_loc,
            ORI: self.m.ori_calculator.get_end_ori(),
        }
        self.m.end_ori = self.m.ori_calculator.get_end_ori()
        self.m.arrow.updater.update_arrow(arrow_dict)
        self.m.prop.update_prop(prop_dict)
        self.m.arrow.ghost.updater.update_arrow(arrow_dict)
        self.m.prop.ghost.update_prop(prop_dict)
