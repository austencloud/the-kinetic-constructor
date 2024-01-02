from Enums import (
    Color,
    Handpath,
    Location,
    MotionAttributesDicts,
    MotionType,
    Orientation,
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

        self.init_attributes()
        self.update_attributes(motion_dict)

    def init_attributes(self):
        self.color: Color = None
        self.arrow: "Arrow" = None
        self.prop: "Prop" = None
        self.motion_type: MotionType = None
        self.turns: Turns = None
        self.start_loc: Location = None
        self.start_ori: Orientation = None
        self.end_loc: Location = None
        self.end_ori: Orientation = None

    ### SETUP ###

    def update_attributes(self, motion_dict: Dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self, attribute, value)
        if self.motion_type:
            self.end_ori: Orientation = self.get_end_ori()
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

    def update_motion(self, motion_dict: MotionAttributesDicts = None) -> None:
        if motion_dict:
            self.update_attributes(motion_dict)
        arrow_dict = {
            LOC: self.get_arrow_location(
                self.start_loc, self.end_loc, self.motion_type
            ),
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
        }
        prop_dict = {
            LOC: self.end_loc,
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
            START_ORI: self.start_ori,
            END_ORI: self.end_ori,
        }

    def get_end_ori(self) -> Orientation:
        def switch_orientation(ori) -> Orientation:
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
        ) -> Orientation:
            if motion_type in [PRO, STATIC]:
                return start_ori if turns % 2 == 0 else switch_orientation(start_ori)
            elif motion_type in [ANTI, DASH]:
                return switch_orientation(start_ori) if turns % 2 == 0 else start_ori

        def calculate_half_turn_orientation(
            motion_type, turns, start_ori
        ) -> Orientation:
            if start_ori in [IN, OUT]:
                return (
                    COUNTER
                    if (turns % 2 == 0.5 and motion_type == PRO)
                    or (turns % 2 != 0.5 and motion_type == ANTI)
                    else CLOCK
                )
            elif start_ori in [CLOCK, COUNTER]:
                return (
                    OUT
                    if (turns % 2 == 0.5 and motion_type == PRO)
                    or (turns % 2 != 0.5 and motion_type == ANTI)
                    else IN
                )

        def calculate_float_orientation(start_ori, handpath_direction) -> Orientation:
            if start_ori in [IN, OUT]:
                return COUNTER if handpath_direction == CW_HANDPATH else CLOCK
            elif start_ori in [CLOCK, COUNTER]:
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
            return calculate_float_orientation(self.start_ori, handpath_direction)

        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        self.turns = (
            float(self.turns)
            if self.turns in ["0.5", "1.5", "2.5"]
            else int(self.turns)
        )

        if self.turns in valid_turns:
            if self.turns.is_integer():
                return calculate_whole_turn_orientation(
                    self.motion_type, self.turns, self.start_ori
                )
            else:
                return calculate_half_turn_orientation(
                    self.motion_type, self.turns, self.start_ori
                )

    def get_start_ori_from_end_ori(self) -> Orientation:
        def switch_orientation(ori) -> Orientation:
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
        ) -> Orientation:
            if motion_type in [PRO, STATIC]:
                return end_ori if turns % 2 == 0 else switch_orientation(end_ori)
            elif motion_type in [ANTI, DASH]:
                return switch_orientation(end_ori) if turns % 2 == 0 else end_ori

        def calculate_half_turn_orientation(motion_type, turns, end_ori) -> Orientation:
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

        def calculate_float_orientation(end_ori, handpath_direction) -> Orientation:
            if end_ori in [IN, OUT]:
                return COUNTER if handpath_direction == CW_HANDPATH else CLOCK
            elif end_ori in [CLOCK, COUNTER]:
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

    def get_arrow_location(
        self, start_loc: str, end_loc: str, motion_type: MotionType
    ) -> Location:
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

        elif self.motion_type == DASH and other_motion_type == DASH:  # Type5 Letter
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
                if not self.arrow.loc:
                    loc_map = {
                        ((NORTH, SOUTH), WEST): EAST,
                        ((EAST, WEST), SOUTH): NORTH,
                        ((NORTH, SOUTH), EAST): WEST,
                        ((WEST, EAST), SOUTH): NORTH,
                        ((SOUTH, NORTH), WEST): EAST,
                        ((EAST, WEST), NORTH): SOUTH,
                        ((SOUTH, NORTH), EAST): WEST,
                        ((WEST, EAST), NORTH): SOUTH,
                    }
                    self.arrow.loc = loc_map.get(
                        (
                            (self.start_loc, self.end_loc),
                            other_motion_end_loc,
                        )
                    )
                    return color_direction_map.get(self.color).get(self.arrow.loc)
                else:
                    return color_direction_map.get(self.color).get(self.arrow.loc)

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

    def get_other_arrow(self) -> "Arrow":
        return (
            self.scene.arrows[RED]
            if self.arrow.color == BLUE
            else self.scene.arrows[BLUE]
        )

    def update_turns(self, turns: Turns) -> None:
        self.turns = turns

    def adjust_turns(self, adjustment: float) -> None:
        potential_new_turns = self.arrow.turns + adjustment
        new_turns_float: float = max(0, min(3, potential_new_turns))

        if new_turns_float % 1 == 0:
            new_turns_int: int = int(new_turns_float)
            if new_turns_int != self.arrow.turns:
                self.turns = new_turns_int
        else:
            if new_turns_float != self.arrow.turns:
                self.turns = new_turns_float

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
