from typing import List
import pandas as pd
from dataframe_generation.data.Type1_generators.ABC_generator import ABC_Generator
from dataframe_generation.data.Type1_generators.DEF_generator import DEF_Generator
from df_generator import DataFrameGenerator
from data.Enums import Location, RotationDirection, SpecificPosition
from data.constants import *
from data.positions_map import positions_map
import os


class Type1_DataFrame_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        self.letters_ABC = ["A", "B", "C"]
        super().__init__(self.letters_ABC)
        self.generate_dataframes()

    def generate_dataframes(self) -> None:
        for letter in self.letters_ABC:
            data = getattr(self, f"create_dataframe_for_{letter}")()
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe_for_A(self) -> List[dict]:
        data = []
        for direction in self.rotation_directions:
            for loc_pair in self.define_shifts("pro")[direction]:
                data.extend(
                    self.create_data_points_for_ABC(
                        "A", loc_pair, direction, "pro", "pro"
                    )
                )
        return data

    def create_dataframe_for_B(self) -> List[dict]:
        data = []
        for direction in self.rotation_directions:
            for loc_pair in self.define_shifts("anti")[direction]:
                data.extend(
                    self.create_data_points_for_ABC(
                        "B", loc_pair, direction, "anti", "anti"
                    )
                )
        return data

    def create_dataframe_for_C(self) -> List[dict]:
        data = []
        for direction in self.rotation_directions:
            for loc_pair in self.define_shifts("pro")[direction]:
                data.extend(
                    self.create_data_points_for_ABC(
                        "C", loc_pair, direction, "pro", "anti"
                    )
                )

        for direction in self.rotation_directions:
            for loc_pair in self.define_shifts("anti")[direction]:
                data.extend(
                    self.create_data_points_for_ABC(
                        "C", loc_pair, direction, "anti", "pro"
                    )
                )
        return data

    def create_data_points_for_ABC(
        self, letter, loc_pair, direction, blue_motion, red_motion
    ):
        shift_start_loc, shift_end_loc = loc_pair
        opposite_start_loc = self.get_opposite_location(shift_start_loc)
        opposite_end_loc = self.get_opposite_location(shift_end_loc)
        start_pos = positions_map.get((shift_start_loc, BLUE, opposite_start_loc, RED))
        end_pos = positions_map.get((shift_end_loc, BLUE, opposite_end_loc, RED))

        return [
            {
                "letter": letter,
                "start_position": start_pos,
                "end_position": end_pos,
                "blue_motion_type": blue_motion,
                "blue_rotation_direction": direction,
                "blue_start_location": shift_start_loc,
                "blue_end_location": shift_end_loc,
                "red_motion_type": red_motion,
                "red_rotation_direction": direction,
                "red_start_location": opposite_start_loc,
                "red_end_location": opposite_end_loc,
            }
        ]

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
        return opposite_map.get(location, "")


Type1_DataFrame_Generator()


class Type1_Master_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=[])  # Initialize with an empty list
        self.type_name = "Type_1"

    def generate_dataframes(self, letter_group) -> None:
        self.ABC_Generator = ABC_Generator()
        self.DEF_Generator = DEF_Generator()

# Instantiate and generate dataframes
Type1_Master_Generator().generate_dataframes()
