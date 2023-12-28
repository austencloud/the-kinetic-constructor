from typing import Dict, List, Tuple
import pandas as pd
from data.Enums import Location, PropRotationDirection, SpecificPosition
from data.constants import *
from data.positions_map import positions_map
import os


class DataFrameGenerator:
    def __init__(self, letters) -> None:
        self.letters = letters
        self.rot_dirs = [CLOCKWISE, COUNTER_CLOCKWISE]
        self.handpath_rot_dirs = [CW_HANDPATH, CCW_HANDPATH]

    def change_red_handpath_map_to(self, handpath_rot_dir):
        if handpath_rot_dir == CCW_HANDPATH:
            self.red_handpath_map = [
                (NORTH, WEST),
                (WEST, SOUTH),
                (SOUTH, EAST),
                (EAST, NORTH),
            ]
        elif handpath_rot_dir == CW_HANDPATH:
            self.red_handpath_map = [
                (NORTH, EAST),
                (EAST, SOUTH),
                (SOUTH, WEST),
                (WEST, NORTH),
            ]

    def get_prop_rot_dir(self, motion_type, handpath_rot_dir) -> PropRotationDirection:
        if motion_type == PRO:
            return CLOCKWISE if handpath_rot_dir == CW_HANDPATH else COUNTER_CLOCKWISE
        else:  # motion_type == "anti"
            return COUNTER_CLOCKWISE if handpath_rot_dir == CW_HANDPATH else CLOCKWISE

    def get_prop_rot_dir(
        self, red_motion_type, red_handpath_rot_dir
    ) -> PropRotationDirection:
        self.change_red_handpath_map_to(red_handpath_rot_dir)
        if red_handpath_rot_dir == CW_HANDPATH:
            if red_motion_type == PRO:
                red_prop_rot_dir = CLOCKWISE
            elif red_motion_type == ANTI:
                red_prop_rot_dir = COUNTER_CLOCKWISE
        elif red_handpath_rot_dir == CCW_HANDPATH:
            if red_motion_type == PRO:
                red_prop_rot_dir = COUNTER_CLOCKWISE
            elif red_motion_type == ANTI:
                red_prop_rot_dir = CLOCKWISE
        return red_prop_rot_dir

    def get_handpath_tuple_map_collection(self):
        return {
            CW_HANDPATH: [
                (NORTH, EAST),
                (EAST, SOUTH),
                (SOUTH, WEST),
                (WEST, NORTH),
            ],
            CCW_HANDPATH: [
                (NORTH, WEST),
                (WEST, SOUTH),
                (SOUTH, EAST),
                (EAST, NORTH),
            ],
        }

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_map.get(location, "")

    def get_opposite_rot_dir(self, rot_dir) -> PropRotationDirection:
        if rot_dir == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif rot_dir == COUNTER_CLOCKWISE:
            return CLOCKWISE

    def get_opposite_loc_tuple(self, red_loc_tuple) -> Tuple[Location, Location]:
        return tuple(self.get_opposite_location(loc) for loc in red_loc_tuple)

    def is_hybrid(self, letter) -> bool:
        return letter in ["C", "F", "I", "L", "O", "R", "U", "V"]

    def get_Type1_start_and_end_pos(
        self, red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
    ) -> Tuple[SpecificPosition, SpecificPosition]:
        start_key = (blue_start_loc, red_start_loc)
        end_key = (blue_end_loc, red_end_loc)
        start_pos = positions_map.get(start_key)
        end_pos = positions_map.get(end_key)
        return start_pos, end_pos

    def save_dataframe(self, letter, data, type_name) -> None:
        df = pd.DataFrame(data)
        self.prepare_dataframe(df)
        self.write_dataframe_to_file(
            df, f"dataframes/{type_name}/{letter}_DataFrame.csv"
        )

    def prepare_dataframe(self, df: pd.DataFrame) -> None:
        motion_type_order = [PRO, "anti", "dash", "static"]
        rot_dir_order = [CLOCKWISE, COUNTER_CLOCKWISE]
        df["blue_motion_type"] = pd.Categorical(
            df["blue_motion_type"], categories=motion_type_order, ordered=True
        )
        df["blue_rot_dir"] = pd.Categorical(
            df["blue_rot_dir"],
            categories=rot_dir_order,
            ordered=True,
        )
        df.sort_values(
            by=[
                "letter",
                "blue_motion_type",
                "blue_rot_dir",
                "start_position",
            ],
            inplace=True,
        )

    def write_dataframe_to_file(self, df: pd.DataFrame, filename):
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df.to_csv(filename, index=False)

