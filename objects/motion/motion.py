from re import L
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
            self.end_ori: Orientation = self.get_end_or()
            self.manipulator = MotionManipulator(self)

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

        self.prop_rot_dir = None
        self.start_or = None
        self.end_ori = None

    def update_motion(self, motion_dict: MotionAttributesDicts = None) -> None:
        if motion_dict:
            self.update_attributes(motion_dict)
        arrow_dict = {
            LOCATION: self.get_arrow_location(
                self.start_loc, self.end_loc, self.motion_type
            ),
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
        }
        prop_dict = {
            LOCATION: self.end_loc,
            ORIENTATION: self.end_ori,
        }
        self.arrow.update_arrow(arrow_dict)
        self.prop.update_prop(prop_dict)

    ### GETTERS ###

    def get_attributes(self) -> MotionAttributesDicts:
        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
            PROP_ROT_DIR: self.prop_rot_dir,
            START_LOC: self.start_loc,
            END_LOC: self.end_loc,
            START_OR: self.start_or,
            END_OR: self.end_ori,
        }

    def get_end_or(self) -> Orientation:
        def switch_orientation(orientation):
            if orientation == IN:
                return OUT
            elif orientation == OUT:
                return IN
            elif orientation == CLOCK:
                return COUNTER
            elif orientation == COUNTER:
                return CLOCK

        def calculate_whole_turn_orientation(
            motion_type, turns, start_orientation
        ) -> Orientation:
            if motion_type in [PRO, STATIC]:
                return (
                    start_orientation
                    if turns % 2 == 0
                    else switch_orientation(start_orientation)
                )
            elif motion_type in [ANTI, DASH]:
                return (
                    switch_orientation(start_orientation)
                    if turns % 2 == 0
                    else start_orientation
                )

        def calculate_half_turn_orientation(
            motion_type, turns, start_orientation
        ) -> Orientation:
            if start_orientation in [IN, OUT]:
                return (
                    COUNTER
                    if (turns % 2 == 0.5 and motion_type == PRO)
                    or (turns % 2 != 0.5 and motion_type == ANTI)
                    else CLOCK
                )
            elif start_orientation in [CLOCK, COUNTER]:
                return (
                    OUT
                    if (turns % 2 == 0.5 and motion_type == PRO)
                    or (turns % 2 != 0.5 and motion_type == ANTI)
                    else IN
                )

        def calculate_float_orientation(
            start_orientation, handpath_direction
        ) -> Orientation:
            if start_orientation in [IN, OUT]:
                return COUNTER if handpath_direction == CW_HANDPATH else CLOCK
            elif start_orientation in [CLOCK, COUNTER]:
                return OUT if handpath_direction == CW_HANDPATH else IN

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
            return calculate_float_orientation(self.start_or, handpath_direction)

        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        self.turns = (
            float(self.turns) if self.turns in [0.5, 1.5, 2.5] else int(self.turns)
        )

        if self.turns in valid_turns:
            if self.turns.is_integer():
                return calculate_whole_turn_orientation(
                    self.motion_type, self.turns, self.start_or
                )
            else:
                return calculate_half_turn_orientation(
                    self.motion_type, self.turns, self.start_or
                )

    def get_arrow_location(
        self, start_loc: str, end_loc: str, motion_type: MotionType
    ) -> str:
        if motion_type in [PRO, ANTI, FLOAT]:
            return self.get_shift_location(start_loc, end_loc)
        elif motion_type == DASH:
            return self.get_dash_location()
        elif motion_type == STATIC:
            return start_loc
        else:
            print("ERROR: Arrow motion type not found")
            return None

    def get_shift_location(self, start_loc: str, end_loc: str) -> str:
        # Simplified by using a single lookup that covers both directions
        direction_map = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
        }
        return direction_map.get(frozenset({start_loc, end_loc}))

    def get_dash_location(self) -> str:
        if self.color == BLUE:
            other_color = RED
        else:  # self.color is red
            other_color = BLUE

        other_motion_start_loc = self.scene.pictograph_dict[f"{other_color}_start_loc"]
        other_motion_end_loc = self.scene.pictograph_dict[f"{other_color}_end_loc"]
        other_motion_type = self.scene.pictograph_dict[f"{other_color}_motion_type"]
        other_arrow_loc: Location = None

        if other_motion_type in [PRO, ANTI, FLOAT]:
            vertical_map = {
                SOUTHEAST: WEST,
                NORTHEAST: WEST,
                SOUTHWEST: EAST,
                NORTHWEST: EAST,
            }
            horizontal_map = {
                SOUTHEAST: NORTH,
                SOUTHWEST: NORTH,
                NORTHEAST: SOUTH,
                NORTHWEST: SOUTH,
            }
            other_arrow_loc = self.get_arrow_location(
                other_motion_start_loc, other_motion_end_loc, other_motion_type
            )
            if self.end_loc in [NORTH, SOUTH]:
                return vertical_map.get(other_arrow_loc)
            elif self.end_loc in [EAST, WEST]:
                return horizontal_map.get(other_arrow_loc)

        elif self.motion_type == DASH and other_motion_type == DASH:
            direction_map = {
                NORTH: SOUTH,
                SOUTH: NORTH,
                EAST: WEST,
                WEST: EAST,
            }

            color_direction_map = {
                BLUE: {
                    NORTH: WEST,
                    EAST: NORTH,
                    SOUTH: EAST,
                    WEST: SOUTH,
                },
                RED: {
                    NORTH: EAST,
                    EAST: SOUTH,
                    SOUTH: WEST,
                    WEST: NORTH,
                },
            }

            if other_arrow_loc:
                return direction_map.get(other_arrow_loc)
            else:
                return color_direction_map.get(self.color, {}).get(self.arrow.loc)
                    
        elif other_motion_type == STATIC:
            other_arrow_loc = self.scene.pictograph_dict[f"{other_color}_start_loc"]
            if self.scene.pictograph_dict[LETTER] == "Λ":
                if other_arrow_loc == NORTH:
                    return SOUTH
                elif other_arrow_loc == SOUTH:
                    return NORTH
                elif other_arrow_loc == EAST:
                    return WEST
                elif other_arrow_loc == WEST:
                    return EAST
            elif self.scene.pictograph_dict[LETTER] in ["Φ", "Ψ"]:
                if other_arrow_loc in [NORTH, SOUTH]:
                    if self.color == BLUE:
                        return WEST
                    else:
                        return EAST
                elif other_arrow_loc in [EAST, WEST]:
                    if self.color == BLUE:
                        return SOUTH
                    else:
                        return NORTH

    def get_other_arrow(self):
        return (
            self.scene.arrows[RED]
            if self.arrow.color == BLUE
            else self.scene.arrows[BLUE]
        )

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
