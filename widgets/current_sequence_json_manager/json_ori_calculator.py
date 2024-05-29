from typing import TYPE_CHECKING
from Enums.Enums import Handpaths
from Enums.MotionAttributes import Color, Location
from data.constants import (
    ANTI,
    CCW_HANDPATH,
    CLOCK,
    CLOCKWISE,
    COUNTER,
    COUNTER_CLOCKWISE,
    CW_HANDPATH,
    DASH,
    DASH_HANDPATH,
    EAST,
    IN,
    NORTH,
    OUT,
    PRO,
    SOUTH,
    STATIC,
    STATIC_HANDPATH,
    WEST,
)
if TYPE_CHECKING:
    from widgets.json_manager import JSON_Manager


class JsonOriCalculator:
    def __init__(self, json_manager: "JSON_Manager"):
        self.main_widget = json_manager.main_widget

    def calculate_end_orientation(self, pictograph_dict, color: Color):
        motion_type = pictograph_dict[f"{color}_attributes"]["motion_type"]
        turns = float(pictograph_dict[f"{color}_attributes"]["turns"])
        start_ori = pictograph_dict[f"{color}_attributes"]["start_ori"]
        prop_rot_dir = pictograph_dict[f"{color}_attributes"]["prop_rot_dir"]

        if motion_type == "float":
            handpath_direction = self.get_handpath_direction(
                pictograph_dict[f"{color}_attributes"]["start_loc"],
                pictograph_dict[f"{color}_attributes"]["end_loc"],
            )
            return self.calculate_float_orientation(start_ori, handpath_direction)
        else:
            return self.calculate_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir
            )

    def calculate_turn_orientation(self, motion_type, turns, start_ori, prop_rot_dir):
        if turns in [0, 1, 2, 3]:
            return self.calculate_whole_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir
            )
        else:
            return self.calculate_half_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir
            )

    def calculate_whole_turn_orientation(
        self, motion_type, turns, start_ori, prop_rot_dir
    ):
        if motion_type in ["pro", "static"]:
            if turns % 2 == 0:
                return start_ori
            else:
                return self.switch_orientation(start_ori)
        elif motion_type in ["anti", "dash"]:
            if turns % 2 == 0:
                return self.switch_orientation(start_ori)
            else:
                return start_ori

    def calculate_half_turn_orientation(
        self, motion_type, turns, start_ori, prop_rot_dir
    ):
        if motion_type in [ANTI, DASH]:
            orientation_map = {
                (IN, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (IN, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (CLOCK, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (CLOCK, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
            }
        elif motion_type in [PRO, STATIC]:
            orientation_map = {
                (IN, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (IN, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (CLOCK, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (CLOCK, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
            }

        return orientation_map.get((start_ori, prop_rot_dir))

    def calculate_float_orientation(self, start_ori, handpath_direction):
        orientation_map = {
            (IN, CW_HANDPATH): COUNTER,
            (IN, CCW_HANDPATH): CLOCK,
            (OUT, CW_HANDPATH): CLOCK,
            (OUT, CCW_HANDPATH): COUNTER,
            (CLOCK, CW_HANDPATH): OUT,
            (CLOCK, CCW_HANDPATH): IN,
            (COUNTER, CW_HANDPATH): IN,
            (COUNTER, CCW_HANDPATH): OUT,
        }
        return orientation_map.get((start_ori, handpath_direction), start_ori)

    def get_handpath_direction(
        self, start_loc: Location, end_loc: Location
    ) -> Handpaths:
        handpaths = {
            (NORTH, EAST): CW_HANDPATH,
            (EAST, SOUTH): CW_HANDPATH,
            (SOUTH, WEST): CW_HANDPATH,
            (WEST, NORTH): CW_HANDPATH,
            (NORTH, WEST): CCW_HANDPATH,
            (WEST, SOUTH): CCW_HANDPATH,
            (SOUTH, EAST): CCW_HANDPATH,
            (EAST, NORTH): CCW_HANDPATH,
            (NORTH, SOUTH): DASH_HANDPATH,
            (SOUTH, NORTH): DASH_HANDPATH,
            (EAST, WEST): DASH_HANDPATH,
            (WEST, EAST): DASH_HANDPATH,
            (NORTH, NORTH): STATIC_HANDPATH,
            (SOUTH, SOUTH): STATIC_HANDPATH,
            (EAST, EAST): STATIC_HANDPATH,
            (WEST, WEST): STATIC_HANDPATH,
        }
        return handpaths.get((start_loc, end_loc), STATIC_HANDPATH)

    def switch_orientation(self, ori):
        switch_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        return switch_map.get(ori, ori)
