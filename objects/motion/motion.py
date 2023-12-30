from Enums import (
    Color,
    Handpath,
    Location,
    MotionAttributesDicts,
    MotionType,
    Orientation,
    PropRotationDirection,
    Turns,
)

from constants import *
from typing import TYPE_CHECKING, Dict, Union
from objects.motion.motion_manipulator import MotionManipulator

from widgets.graph_editor_tab.object_panel.propbox.propbox import PropBox


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


class Motion:
    def __init__(
        self,
        scene: Union["ArrowBox", "PropBox", "Pictograph"],
        motion_dict: MotionAttributesDicts,
    ) -> None:
        self.scene = scene
        self.update_attributes(motion_dict)

    ### SETUP ###

    def update_attributes(self, motion_dict: Dict) -> None:
        self.color: Color = motion_dict[COLOR]
        self.arrow: Arrow = motion_dict[ARROW]
        self.prop: Prop = motion_dict[PROP]

        self.motion_type: MotionType = motion_dict[MOTION_TYPE]
        self.turns: Turns = motion_dict[TURNS]
        self.prop_rot_dir: PropRotationDirection = motion_dict[PROP_ROT_DIR]
        self.start_loc: Location = motion_dict[START_LOC]
        self.end_loc: Location = motion_dict[END_LOC]
        self.start_or: Orientation = motion_dict[START_OR]

        if self.motion_type:
            self.manipulator = MotionManipulator(self)
            self.assign_attributes_to_arrow()
            self.end_ori: Orientation = self.get_end_or()

    def assign_attributes_to_arrow(self) -> None:
        if hasattr(self, ARROW) and self.arrow:
            self.arrow.location = self.get_arrow_location(self.start_loc, self.end_loc)
            self.arrow.motion_type = self.motion_type

    ### UPDATE ###

    def update_prop_ori(self) -> None:
        if hasattr(self, PROP) and self.prop:
            if not self.end_ori:
                self.end_ori = self.get_end_or()
            self.prop.ori = self.end_ori
            self.prop.loc = self.end_loc
            self.prop.axis = self.prop.get_axis_from_ori()

    def clear_attributes(self) -> None:
        self.start_loc = None
        self.end_loc = None
        self.turns = None
        self.motion_type = None

        self.motion.prop_rot_dir = None
        self.start_or = None
        self.end_ori = None

    def update_motion(self, motion_dict: MotionAttributesDicts = None) -> None:
        if motion_dict:
            self.update_attributes(motion_dict)
        self.arrow.update_arrow()
        self.prop.update_prop()
        
    ### GETTERS ###

    def get_attributes(self) -> MotionAttributesDicts:
        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
            PROP_ROT_DIR: self.motion.prop_rot_dir,
            START_LOC: self.start_loc,
            END_LOC: self.end_loc,
            START_OR: self.start_or,
            END_OR: self.end_ori,
        }

    def get_end_or(self) -> Orientation:
        whole_turn_orientation_map = {
            (PRO, 0, IN): IN,
            (PRO, 1, IN): OUT,
            (PRO, 2, IN): IN,
            (PRO, 3, IN): OUT,
            (PRO, 0, OUT): OUT,
            (PRO, 1, OUT): IN,
            (PRO, 2, OUT): OUT,
            (PRO, 3, OUT): IN,
            (ANTI, 0, IN): OUT,
            (ANTI, 1, IN): IN,
            (ANTI, 2, IN): OUT,
            (ANTI, 3, IN): IN,
            (ANTI, 0, OUT): IN,
            (ANTI, 1, OUT): OUT,
            (ANTI, 2, OUT): IN,
            (ANTI, 3, OUT): OUT,
            (PRO, 0, CLOCK): CLOCK,
            (PRO, 1, CLOCK): COUNTER,
            (PRO, 2, CLOCK): CLOCK,
            (PRO, 3, CLOCK): COUNTER,
            (PRO, 0, COUNTER): COUNTER,
            (PRO, 1, COUNTER): CLOCK,
            (PRO, 2, COUNTER): COUNTER,
            (PRO, 3, COUNTER): CLOCK,
            (ANTI, 0, CLOCK): COUNTER,
            (ANTI, 1, CLOCK): CLOCK,
            (ANTI, 2, CLOCK): COUNTER,
            (ANTI, 3, CLOCK): CLOCK,
            (ANTI, 0, COUNTER): CLOCK,
            (ANTI, 1, COUNTER): COUNTER,
            (ANTI, 2, COUNTER): CLOCK,
            (ANTI, 3, COUNTER): COUNTER,
        }

        cw_handpath_half_turns_map = {
            (PRO, 0.5, IN): COUNTER,
            (PRO, 1.5, IN): CLOCK,
            (PRO, 2.5, IN): COUNTER,
            (PRO, 0.5, OUT): CLOCK,
            (PRO, 1.5, OUT): COUNTER,
            (PRO, 2.5, OUT): CLOCK,
            (ANTI, 0.5, IN): CLOCK,
            (ANTI, 1.5, IN): COUNTER,
            (ANTI, 2.5, IN): CLOCK,
            (ANTI, 0.5, OUT): COUNTER,
            (ANTI, 1.5, OUT): CLOCK,
            (ANTI, 2.5, OUT): COUNTER,
            (PRO, 0.5, CLOCK): IN,
            (PRO, 1.5, CLOCK): OUT,
            (PRO, 2.5, CLOCK): IN,
            (PRO, 0.5, COUNTER): OUT,
            (PRO, 1.5, COUNTER): IN,
            (PRO, 2.5, COUNTER): OUT,
            (ANTI, 0.5, CLOCK): OUT,
            (ANTI, 1.5, CLOCK): IN,
            (ANTI, 2.5, CLOCK): OUT,
            (ANTI, 0.5, COUNTER): IN,
            (ANTI, 1.5, COUNTER): OUT,
            (ANTI, 2.5, COUNTER): IN,
        }

        ccw_handpath_half_turns_map = {
            (PRO, 0.5, IN): CLOCK,
            (PRO, 1.5, IN): COUNTER,
            (PRO, 2.5, IN): CLOCK,
            (PRO, 0.5, OUT): COUNTER,
            (PRO, 1.5, OUT): CLOCK,
            (PRO, 2.5, OUT): COUNTER,
            (ANTI, 0.5, IN): COUNTER,
            (ANTI, 1.5, IN): CLOCK,
            (ANTI, 2.5, IN): COUNTER,
            (ANTI, 0.5, OUT): CLOCK,
            (ANTI, 1.5, OUT): COUNTER,
            (ANTI, 2.5, OUT): CLOCK,
            (PRO, 0.5, CLOCK): OUT,
            (PRO, 1.5, CLOCK): IN,
            (PRO, 2.5, CLOCK): OUT,
            (PRO, 0.5, COUNTER): IN,
            (PRO, 1.5, COUNTER): OUT,
            (PRO, 2.5, COUNTER): IN,
            (ANTI, 0.5, CLOCK): IN,
            (ANTI, 1.5, CLOCK): OUT,
            (ANTI, 2.5, CLOCK): IN,
            (ANTI, 0.5, COUNTER): OUT,
            (ANTI, 1.5, COUNTER): IN,
            (ANTI, 2.5, COUNTER): OUT,
        }

        float_map = {
            (IN, CW_HANDPATH): CLOCK,
            (IN, CCW_HANDPATH): COUNTER,
            (OUT, CW_HANDPATH): COUNTER,
            (OUT, CCW_HANDPATH): CLOCK,
            (CLOCK, CW_HANDPATH): OUT,
            (CLOCK, CCW_HANDPATH): IN,
            (COUNTER, CW_HANDPATH): IN,
            (COUNTER, CCW_HANDPATH): OUT,
        }

        def get_handpath_direction(start_loc, end_loc) -> Handpath:
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
            key = (self.start_or, handpath_direction)
            return float_map.get(key)
        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        self.turns = (
            float(self.turns) if self.turns in [0.5, 1.5, 2.5] else int(self.turns)
        )

        if self.turns in valid_turns:
            if self.turns.is_integer():
                if self.motion_type in [PRO, ANTI]:
                    key = (self.motion_type, self.turns, self.start_or)
                    return whole_turn_orientation_map.get(key)
                if self.motion_type == STATIC:
                    key = (PRO, self.turns, self.start_or)
                    return whole_turn_orientation_map.get(key)
                if self.motion_type == DASH:
                    key = (ANTI, self.turns, self.start_or)
                    return whole_turn_orientation_map.get(key)
            else:
                if handpath_direction == CW_HANDPATH:
                    map_to_use = cw_handpath_half_turns_map
                else:
                    map_to_use = ccw_handpath_half_turns_map

                if self.motion_type in [PRO, ANTI]:
                    key = (self.motion_type, self.turns, self.start_or)
                    return map_to_use.get(key)

                if self.motion_type == STATIC:
                    key = (PRO, self.turns, self.start_or)
                    return map_to_use.get(key)

                elif self.motion_type == DASH:
                    key = (ANTI, self.turns, self.start_or)
                    return map_to_use.get(key)

    def get_arrow_location(self, start_loc: str, end_loc: str) -> str:
        if self.arrow:
            if start_loc == end_loc:
                return start_loc

            direction_map = {
                (NORTH, EAST): NORTHEAST,
                (EAST, SOUTH): SOUTHEAST,
                (SOUTH, WEST): SOUTHWEST,
                (WEST, NORTH): NORTHWEST,
                (NORTH, WEST): NORTHWEST,
                (WEST, SOUTH): SOUTHWEST,
                (SOUTH, EAST): SOUTHEAST,
                (EAST, NORTH): NORTHEAST,
            }

            return direction_map.get((start_loc, end_loc)) or direction_map.get(
                (end_loc, start_loc)
            )

    ### MANIPULATORS ###

    def adjust_turns(self, adjustment: float) -> None:
        potential_new_turns = self.arrow.turns + adjustment
        new_turns_float: float = max(0, min(3, potential_new_turns))

        if new_turns_float % 1 == 0:
            new_turns_int: int = int(new_turns_float)
            if new_turns_int != self.arrow.turns:
                self.update_turns(new_turns_int)
        else:
            if new_turns_float != self.arrow.turns:
                self.update_turns(new_turns_float)

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
