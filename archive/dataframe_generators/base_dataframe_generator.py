from typing import set, tuple
import pandas as pd
from constants import *
from data.positions_map import positions_map
import os

from Enums.Enums import (
    Location,
    PropRotDir,
    ShiftHandpaths,
    SpecificPosition,
)


class BaseDataFrameGenerator:
    def __init__(self, letters) -> None:
        self.letters = letters
        self.rot_dirs = [CLOCKWISE, COUNTER_CLOCKWISE]
        self.shift_handpaths = [CW_HANDPATH, CCW_HANDPATH]

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

    def get_start_end_poss(
        self, blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
    ) -> tuple[Location]:
        start_key = (blue_start_loc, red_start_loc)
        end_key = (blue_end_loc, red_end_loc)
        start_pos = positions_map.get(start_key)
        end_pos = positions_map.get(end_key)
        return start_pos, end_pos

    def get_prop_rot_dir(self, motion_type, handpath_rot_dir) -> PropRotDir:
        if motion_type == PRO:
            return CLOCKWISE if handpath_rot_dir == CW_HANDPATH else COUNTER_CLOCKWISE
        elif motion_type == ANTI:
            return COUNTER_CLOCKWISE if handpath_rot_dir == CW_HANDPATH else CLOCKWISE
        elif motion_type == DASH:
            return NO_ROT

    def get_static_tuple_map(self):
        return {
            (NORTH, NORTH),
            (EAST, EAST),
            (SOUTH, SOUTH),
            (WEST, WEST),
        }

    def get_dash_tuple_map(self):
        return {
            (NORTH, SOUTH),
            (EAST, WEST),
            (SOUTH, NORTH),
            (WEST, EAST),
        }

    def get_shift_tuple_map_from_handpath(
        self, handpath: ShiftHandpaths
    ) -> set[tuple[Location]]:
        if handpath == CW_HANDPATH:
            return {
                (NORTH, EAST),
                (EAST, SOUTH),
                (SOUTH, WEST),
                (WEST, NORTH),
            }
        elif handpath == CCW_HANDPATH:
            return {
                (NORTH, WEST),
                (WEST, SOUTH),
                (SOUTH, EAST),
                (EAST, NORTH),
            }

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_map.get(location, "")

    def get_opposite_rot_dir(self, rot_dir) -> PropRotDir:
        if rot_dir == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif rot_dir == COUNTER_CLOCKWISE:
            return CLOCKWISE

    def get_opposite_loc_tuple(self, red_loc_tuple) -> tuple[Location]:
        return tuple(self.get_opposite_location(loc) for loc in red_loc_tuple)

    def is_hybrid(self, letter) -> bool:
        return letter in ["C", "F", "I", "L", "O", "R", "U", "V"]

    def get_Type1_start_and_end_pos(
        self, red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
    ) -> tuple[SpecificPosition]:
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
        rot_dir_order = [
            CLOCKWISE,
            COUNTER_CLOCKWISE,
            NO_ROT,
        ]  # Include NO_ROT

        df[BLUE_MOTION_TYPE] = pd.Categorical(
            df[BLUE_MOTION_TYPE], categories=motion_type_order, ordered=True
        )
        df[BLUE_PROP_ROT_DIR] = pd.Categorical(
            df[BLUE_PROP_ROT_DIR],
            categories=rot_dir_order,
            ordered=True,
        )
        df.sort_values(
            by=[
                LETTER,
                BLUE_MOTION_TYPE,
                BLUE_PROP_ROT_DIR,
                START_POS,
            ],
            inplace=True,
        )

    def write_dataframe_to_file(self, df: pd.DataFrame, filename):
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df.to_csv(filename, index=False, na_rep=NO_ROT)
