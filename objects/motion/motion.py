from constants import *
from typing import TYPE_CHECKING, Dict, Union
from objects.motion.motion_manipulator import MotionManipulator
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Handpaths,
    Locations,
    MotionTypes,
    Orientations,
    PropRotDirs,
    Turns,
)

from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import PropBox


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )


class Motion:
    def __init__(
        self,
        scene: Union["ArrowBox", "PropBox", "Pictograph"],
        motion_dict,
    ) -> None:
        self.scene = scene
        self.init_attributes()
        self.update_attributes(motion_dict)

    def init_attributes(self) -> None:
        self.color: Colors = None
        self.arrow: "Arrow" = None
        self.prop: "Prop" = None
        self.prop_rot_dir: PropRotDirs = None
        self.motion_type: MotionTypes = None
        self.turns: Turns = None
        self.start_loc: Locations = None
        self.start_ori: Orientations = None
        self.end_loc: Locations = None
        self.end_ori: Orientations = None

    ### SETUP ###

    def update_attributes(self, motion_dict: Dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self, attribute, value)
        if self.motion_type:
            self.end_ori: Orientations = self.get_end_ori()
            self.manipulator = MotionManipulator(self)

    ### UPDATE ###

    def update_prop_ori(self) -> None:
        if hasattr(self, PROP) and self.prop:
            if not self.end_ori:
                self.end_ori = self.get_end_ori()
            self.prop.ori = self.end_ori
            self.prop.loc = self.end_loc
            self.prop.axis = self.prop.get_axis_from_ori()

    def clear_attributes(self) -> None:
        self.start_loc = None
        self.end_loc = None
        self.turns = None
        self.motion_type = None

        self.prop_rot_dir = None
        self.start_ori = None
        self.end_ori = None

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.update_attributes(motion_dict)
        self.arrow.loc = self.arrow.arrow_location_manager.get_arrow_location()
        arrow_dict = {
            LOC: self.arrow.arrow_location_manager.get_arrow_location(),
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
        }
        prop_dict = {
            LOC: self.end_loc,
            ORI: self.get_end_ori(),
        }
        if arrow_dict[LOC]:
            self.arrow.loc = arrow_dict[LOC]
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

    def get_end_ori(self) -> Orientations:
        def switch_orientation(ori) -> Orientations:
            if ori == IN:
                return OUT
            elif ori == OUT:
                return IN
            elif ori == CLOCK:
                return COUNTER
            elif ori == COUNTER:
                return CLOCK

        def calculate_whole_turn_orientation(
            motion_type, turns, start_ori
        ) -> Orientations:
            if motion_type in [PRO, STATIC]:
                return start_ori if turns % 2 == 0 else switch_orientation(start_ori)
            elif motion_type in [ANTI, DASH]:
                return switch_orientation(start_ori) if turns % 2 == 0 else start_ori

        def calculate_half_turn_orientation(
            motion_type, turns, start_ori
        ) -> Orientations:
            if start_ori in [IN, OUT]:
                if self.prop_rot_dir == CLOCKWISE:
                    return (
                        COUNTER
                        if (turns % 2 == 0.5 and motion_type in [PRO, STATIC])
                        or (turns % 2 != 0.5 and motion_type in [ANTI, DASH])
                        else CLOCK
                    )
                elif self.prop_rot_dir == COUNTER_CLOCKWISE:
                    return (
                        CLOCK
                        if (turns % 2 == 0.5 and motion_type in [PRO, STATIC])
                        or (turns % 2 != 0.5 and motion_type in [ANTI, DASH])
                        else COUNTER
                    )
            elif start_ori in [CLOCK, COUNTER]:
                if self.prop_rot_dir == CLOCKWISE:
                    return (
                        OUT
                        if (turns % 2 == 0.5 and motion_type in [PRO, STATIC])
                        or (turns % 2 != 0.5 and motion_type in [ANTI, DASH])
                        else IN
                    )
                elif self.prop_rot_dir == COUNTER_CLOCKWISE:
                    return (
                        IN
                        if (turns % 2 == 0.5 and motion_type in [PRO, STATIC])
                        or (turns % 2 != 0.5 and motion_type in [ANTI, DASH])
                        else OUT
                    )

        def calculate_float_orientation(start_ori, handpath_direction) -> Orientations:
            if start_ori in [IN, OUT]:
                return COUNTER if handpath_direction == CW_HANDPATH else CLOCK
            elif start_ori in [CLOCK, COUNTER]:
                return OUT if handpath_direction == CW_HANDPATH else IN

        def get_handpath_direction(start_loc, end_loc) -> Handpaths:
            cw_handpaths = [(NORTH, EAST), (EAST, SOUTH), (SOUTH, WEST), (WEST, NORTH)]
            ccw_handpaths = [(NORTH, WEST), (WEST, SOUTH), (SOUTH, EAST), (EAST, NORTH)]
            dash_handpaths = [
                (NORTH, SOUTH),
                (EAST, WEST),
                (SOUTH, NORTH),
                (WEST, EAST),
            ]
            if (start_loc, end_loc) in cw_handpaths:
                return CW_HANDPATH
            elif (start_loc, end_loc) in ccw_handpaths:
                return CCW_HANDPATH
            elif start_loc == end_loc:
                return STATIC_HANDPATH
            elif (start_loc, end_loc) in dash_handpaths:
                return DASH_HANDPATH
            else:
                print("Unrecognized handpath direction")

        handpath_direction = get_handpath_direction(self.start_loc, self.end_loc)
        if self.motion_type == FLOAT:
            return calculate_float_orientation(self.start_ori, handpath_direction)

        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]

        if self.turns in valid_turns:
            if self.turns in [0, 1, 2, 3]:
                return calculate_whole_turn_orientation(
                    self.motion_type, self.turns, self.start_ori
                )
            else:  # self.turns in [0.5, 1.5, 2.5]
                return calculate_half_turn_orientation(
                    self.motion_type, self.turns, self.start_ori
                )

    def get_start_ori_from_end_ori(self) -> Orientations:
        def switch_orientation(ori) -> Orientations:
            if ori == IN:
                return OUT
            elif ori == OUT:
                return IN
            elif ori == CLOCK:
                return COUNTER
            elif ori == COUNTER:
                return CLOCK

        def calculate_whole_turn_orientation(
            motion_type, turns, end_ori
        ) -> Orientations:
            if motion_type in [PRO, STATIC]:
                return end_ori if turns % 2 == 0 else switch_orientation(end_ori)
            elif motion_type in [ANTI, DASH]:
                return switch_orientation(end_ori) if turns % 2 == 0 else end_ori

        def calculate_half_turn_orientation(
            motion_type, turns, end_ori
        ) -> Orientations:
            if end_ori in [IN, OUT]:
                return (
                    COUNTER
                    if (turns % 2 == 0.5 and motion_type == ANTI)
                    or (turns % 2 != 0.5 and motion_type == PRO)
                    else CLOCK
                )
            elif end_ori in [CLOCK, COUNTER]:
                return (
                    OUT
                    if (turns % 2 == 0.5 and motion_type == ANTI)
                    or (turns % 2 != 0.5 and motion_type == PRO)
                    else IN
                )

        def calculate_float_orientation(end_ori, handpath_direction) -> Orientations:
            if end_ori in [IN, OUT]:
                return COUNTER if handpath_direction == CW_HANDPATH else CLOCK
            elif end_ori in [CLOCK, COUNTER]:
                return OUT if handpath_direction == CW_HANDPATH else IN

        def get_handpath_direction(start_loc, end_loc) -> Handpaths:
            cw_handpaths = [(NORTH, EAST), (EAST, SOUTH), (SOUTH, WEST), (WEST, NORTH)]
            ccw_handpaths = [(NORTH, WEST), (WEST, SOUTH), (SOUTH, EAST), (EAST, NORTH)]
            dash_handpaths = [
                (NORTH, SOUTH),
                (EAST, WEST),
                (SOUTH, NORTH),
                (WEST, EAST),
            ]
            if (start_loc, end_loc) in cw_handpaths:
                return CW_HANDPATH
            elif (start_loc, end_loc) in ccw_handpaths:
                return CCW_HANDPATH
            elif start_loc == end_loc:
                return STATIC_HANDPATH
            elif (start_loc, end_loc) in dash_handpaths:
                return DASH_HANDPATH
            else:
                print("Unrecognized handpath direction")

        handpath_direction = get_handpath_direction(self.start_loc, self.end_loc)
        if self.motion_type == FLOAT:
            return calculate_float_orientation(self.end_ori, handpath_direction)

        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        self.turns = (
            float(self.turns) if self.turns in [0.5, 1.5, 2.5] else int(self.turns)
        )

        if self.turns in valid_turns:
            if self.turns.is_integer():
                return calculate_whole_turn_orientation(
                    self.motion_type, self.turns, self.end_ori
                )
            else:
                return calculate_half_turn_orientation(
                    self.motion_type, self.turns, self.end_ori
                )

    def get_other_arrow(self) -> "Arrow":
        return (
            self.scene.arrows[RED]
            if self.arrow.color == BLUE
            else self.scene.arrows[BLUE]
        )

    def update_turns(self, turns: Turns) -> None:
        self.turns = turns
        self.arrow.turns = turns

    def adjust_turns(self, adjustment: float) -> None:
        new_turns = max(0, min(3, self.arrow.turns + adjustment))

        if new_turns != self.arrow.turns:
            self.turns = new_turns
            self.arrow.turns = new_turns

    def add_half_turn(self) -> None:
        self.adjust_turns(0.5)

    def subtract_half_turn(self) -> None:
        self.adjust_turns(-0.5)

    def add_turn(self) -> None:
        self.adjust_turns(1)

    def subtract_turn(self) -> None:
        self.adjust_turns(-1)

    ### FLAGS ###

    def is_shift(self) -> bool:
        return self.motion_type in [PRO, ANTI, FLOAT]

    def is_dash(self) -> bool:
        return self.motion_type == DASH

    def is_static(self) -> bool:
        return self.motion_type == STATIC

    def is_dash_or_static(self) -> bool:
        return self.motion_type in [DASH, STATIC]

    def set_turns(self, turns: Turns) -> None:
        self.turns = turns
        self.arrow.turns = turns
        self.arrow.ghost.turns = turns
