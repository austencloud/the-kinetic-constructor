import re
from typing import Dict, List, Tuple
from df_generator import DataFrameGenerator
from Enums import Location, PropRotationDirection
from constants import *
from utilities.TypeChecking.Letters import Type3_letters


class Type3Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type3_letters)
        self.create_Type3_dataframes()

    def create_Type3_dataframes(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_3")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter in ["W-", "Y-", "Σ-", "θ-"]:
            data = self.create_dataframes_for_letter(letter, PRO, DASH)
            data += self.create_dataframes_for_letter(letter, DASH, PRO)
        else:  # letter in ["X-", "Z-", "Δ-", "Ω-"]
            data = self.create_dataframes_for_letter(letter, ANTI, DASH)
            data += self.create_dataframes_for_letter(letter, DASH, ANTI)
        return data

    def create_dataframes_for_letter(self, letter, red_motion_type, blue_motion_type):
        shift_handpath_tuple_map_collection = self.get_handpath_tuple_map_collection()
        data = []
        for shift_handpath, tuples in shift_handpath_tuple_map_collection.items():
            if red_motion_type in [PRO, ANTI]:
                red_prop_rot_dir = self.get_prop_rot_dir(
                    red_motion_type, shift_handpath
                )
            else:
                red_prop_rot_dir = "None"  # Explicitly indicating no rotation

            if blue_motion_type in [PRO, ANTI]:
                blue_prop_rot_dir = self.get_prop_rot_dir(
                    blue_motion_type, shift_handpath
                )
            else:
                blue_prop_rot_dir = "None"  # Explicitly indicating no rotation

            for start_loc, end_loc in tuples:
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
                        "letter": letter,
                        "start_position": start_pos,
                        "end_position": end_pos,
                        "blue_motion_type": blue_motion_type,
                        "blue_prop_rot_dir": blue_prop_rot_dir,
                        "blue_start_loc": blue_start_loc,
                        "blue_end_loc": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_prop_rot_dir": red_prop_rot_dir,
                        "red_start_loc": red_start_loc,
                        "red_end_loc": red_end_loc,
                    }
                )
        return data

    def get_dash_locations(
        self, letter, shift_start_loc, shift_end_loc
    ) -> Tuple[Location, Location]:
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
