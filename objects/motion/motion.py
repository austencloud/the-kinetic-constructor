from typing import TYPE_CHECKING, Dict

from objects.motion.motion_checker import MotionChecker

from .motion_attr_manager import MotionAttrManager
from .motion_manipulator import MotionManipulator
from .motion_ori_calculator import MotionOriCalculator
from .motion_updater import MotionUpdater
from .motion_turn_manager import MotionTurnsManager

from utilities.TypeChecking.TypeChecking import (
    Colors,
    LeadStates,
    Locations,
    MotionTypes,
    Orientations,
    PropRotDirs,
    Turns,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class Motion:
    def __init__(self, pictograph: "Pictograph", motion_dict: Dict) -> None:
        self.pictograph = pictograph
        self.motion_dict = motion_dict
        self.ori_calculator = MotionOriCalculator(self)
        self.manipulator = MotionManipulator(self)
        self.attr_manager = MotionAttrManager(self)
        self.turns_manager = MotionTurnsManager(self)
        self.updater = MotionUpdater(self)
        self.check = MotionChecker(self)

    color: Colors
    turns: Turns
    arrow: "Arrow"
    prop: "Prop"
    motion_type: MotionTypes
    start_loc: Locations
    start_ori: Orientations
    end_loc: Locations
    end_ori: Orientations
    prop_rot_dir: PropRotDirs
    lead_state: LeadStates
