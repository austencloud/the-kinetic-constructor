from typing import Dict, List, Tuple
import pandas as pd
from df_generator import DataFrameGenerator
from data.Enums import Location, PropRotationDirection, SpecificPosition
from data.constants import *
from data.positions_map import positions_map
import os


class Type3_DataFrame_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        self.letters = ["W-", "X-", "θ-", "Ω-", "Σ-", "Δ-", "Y-", "Z-"]
        super.__init__(self, self.letters)
        self.rot_dirs = ["cw", "ccw"]
        self.pro_shifts = self.define_shifts("pro")
        self.anti_shifts = self.define_shifts("anti")
        self.generate_dataframes()

    def define_shifts(
        self, shift_type
    ) -> Dict[PropRotationDirection, List[Tuple[Location, Location]]]:
        if shift_type == "pro":
            return {
                "cw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
                "ccw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
            }
        else:  # anti
            return {
                "cw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
                "ccw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
            }

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
        return opposite_map.get(location, "")

    def generate_dataframes(self) -> None:
        for letter in self.letters:
            self.create_dataframe_for_letter(letter)

    def create_dataframe_for_letter(self, letter) -> None:
        data = []
        for rot_dir in self.rot_dirs:
            shift_method = (
                self.process_pro_shifts
                if letter in ["W-", "Y-", "Σ-", "θ-"]
                else self.process_anti_shifts
            )
            shift_method(letter, rot_dir, data)
        self.save_dataframe(letter, data, "Type_3")

    def process_pro_shifts(self, letter, rot_dir, data) -> None:
        for shift_start_loc, shift_end_loc in self.pro_shifts[rot_dir]:
            dash_start_loc, dash_end_loc = self.get_dash_locations(
                letter, shift_start_loc, shift_end_loc
            )
            self.add_data_point(
                letter,
                shift_start_loc,
                shift_end_loc,
                dash_start_loc,
                dash_end_loc,
                rot_dir,
                "pro",
                data,
            )

    def process_anti_shifts(self, letter, rot_dir, data) -> None:
        for shift_start_loc, shift_end_loc in self.anti_shifts[rot_dir]:
            dash_start_loc, dash_end_loc = self.get_dash_locations(
                letter, shift_start_loc, shift_end_loc
            )
            self.add_data_point(
                letter,
                shift_start_loc,
                shift_end_loc,
                dash_start_loc,
                dash_end_loc,
                rot_dir,
                "anti",
                data,
            )

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

    def add_data_point(
        self,
        letter,
        shift_start_loc,
        shift_end_loc,
        dash_start_loc,
        dash_end_loc,
        rot_dir,
        shift_motion_type,
        data,
    ) -> None:
        start_pos, end_pos = self.get_start_and_end_pos(
            shift_start_loc, shift_end_loc, dash_start_loc, dash_end_loc
        )
        if start_pos and end_pos:
            data.append(
                self.create_data_dict(
                    letter,
                    shift_start_loc,
                    shift_end_loc,
                    dash_start_loc,
                    dash_end_loc,
                    rot_dir,
                    shift_motion_type,
                    start_pos,
                    end_pos,
                    RED,
                )
            )
            data.append(
                self.create_data_dict(
                    letter,
                    shift_start_loc,
                    shift_end_loc,
                    dash_start_loc,
                    dash_end_loc,
                    rot_dir,
                    shift_motion_type,
                    start_pos,
                    end_pos,
                    BLUE,
                )
            )

    def create_data_dict(
        self,
        letter,
        shift_start_loc,
        shift_end_loc,
        dash_start_loc,
        dash_end_loc,
        rot_dir,
        shift_motion_type,
        start_pos,
        end_pos,
        dasher_color,
    ):
        if dasher_color == RED:
            return {
                "letter": letter,
                "start_position": start_pos,
                "end_position": end_pos,
                "blue_motion_type": shift_motion_type,
                "blue_rot_dir": rot_dir,
                "blue_start_location": shift_start_loc,
                "blue_end_location": shift_end_loc,
                "red_motion_type": "dash",
                "red_rot_dir": "None",
                "red_start_location": dash_start_loc,
                "red_end_location": dash_end_loc,
            }
        elif dasher_color == BLUE:
            return {
                "letter": letter,
                "start_position": start_pos,
                "end_position": end_pos,
                "blue_motion_type": "dash",
                "blue_rot_dir": "None",
                "blue_start_location": dash_start_loc,
                "blue_end_location": dash_end_loc,
                "red_motion_type": shift_motion_type,
                "red_rot_dir": rot_dir,
                "red_start_location": shift_start_loc,
                "red_end_location": shift_end_loc,
            }


Type3_DataFrame_Generator()
