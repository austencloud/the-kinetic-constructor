from typing import Dict, List, Tuple

import pandas as pd
from dataframes.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)

from constants import *
from utilities.TypeChecking.Letters import Type3_letters
from utilities.TypeChecking.TypeChecking import Locations


class Type3Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type3_letters)
        self.create_Type3_dataframes()

    def create_Type3_dataframes(self) -> pd.DataFrame:
        all_data = []
        for letter in self.letters:
            data = self.create_dataframe(letter)
            all_data.extend(data)
            print("Generated dataframes for letter:", letter)
        return pd.DataFrame(all_data)

    def create_dataframe(self, letter) -> List[Dict]:
        if letter in ["W-", "Y-", "Σ-", "θ-"]:
            data = self.create_dataframes_for_letter(letter, PRO, DASH)
            data += self.create_dataframes_for_letter(letter, DASH, PRO)
        else:  # letter in ["X-", "Z-", "Δ-", "Ω-"]
            data = self.create_dataframes_for_letter(letter, ANTI, DASH)
            data += self.create_dataframes_for_letter(letter, DASH, ANTI)
        return data

    def create_dataframes_for_letter(self, letter, red_motion_type, blue_motion_type):
        data = []
        for shift_handpath in self.shift_handpaths:
            shift_tuple_map = self.get_shift_tuple_map_from_handpath(shift_handpath)
            for start_loc, end_loc in shift_tuple_map:
                if red_motion_type in [PRO, ANTI]:
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, shift_handpath
                    )
                else:
                    red_prop_rot_dir = "no_rot"  # Explicitly indicating no rotation

                if blue_motion_type in [PRO, ANTI]:
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, shift_handpath
                    )
                else:
                    blue_prop_rot_dir = "no_rot"  # Explicitly indicating no rotation

                if red_motion_type == DASH:
                    red_start_loc, red_end_loc = self.get_dash_locations(
                        letter, start_loc, end_loc
                    )
                    blue_start_loc, blue_end_loc = start_loc, end_loc
                elif blue_motion_type == DASH:
                    blue_start_loc, blue_end_loc = self.get_dash_locations(
                        letter, start_loc, end_loc
                    )
                    red_start_loc, red_end_loc = start_loc, end_loc
                else:
                    red_start_loc, red_end_loc = start_loc, end_loc
                    blue_start_loc, blue_end_loc = start_loc, end_loc

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )
                data.append(
                    {
                        LETTER: letter,
                        START_POS: start_pos,
                        END_POS: end_pos,
                        BLUE_MOTION_TYPE: blue_motion_type,
                        BLUE_PROP_ROT_DIR: blue_prop_rot_dir,
                        BLUE_START_LOC: blue_start_loc,
                        BLUE_END_LOC: blue_end_loc,
                        RED_MOTION_TYPE: red_motion_type,
                        RED_PROP_ROT_DIR: red_prop_rot_dir,
                        RED_START_LOC: red_start_loc,
                        RED_END_LOC: red_end_loc,
                    }
                )
        return data

    def get_dash_locations(
        self, letter, shift_start_loc, shift_end_loc
    ) -> Tuple[Locations]:
        if letter in ["W-", "X-"]:  # Dash starts at shift_end_loc
            dash_start_loc = shift_end_loc
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        elif letter in ["Y-", "Z-"]:  # Dash ends at shift_end_loc
            dash_start_loc = self.get_opposite_location(shift_end_loc)
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        elif letter in ["θ-", "Ω-"]:  # Dash ends at shift_start_loc
            dash_end_loc = shift_start_loc
            dash_start_loc = self.get_opposite_location(dash_end_loc)
        elif letter in ["Σ-", "Δ-"]:  # Dash starts at shift_start_loc
            dash_start_loc = shift_start_loc
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        return dash_start_loc, dash_end_loc


Type3Generator()
